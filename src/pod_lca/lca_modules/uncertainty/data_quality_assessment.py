
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from ...utilities import config
from ...utilities import log


class PedigreeScore:
    """ PedigreeScore object contains background data for data quality scores.

    Attributes
    ----------
    parent : Master Obj.
        Product/Process object for which the data quality is related.
    DQS : float
        Data quality score of the object.
    <indicators> : float
        Data Quality Indicators are dynamically set based on the Data Quality Analysis (DQA) used.
    """

    def __init__(self):
        self.parent = None
        self.DQS = 0.0

    def __str__(self):
        string = ("*"*50 + "\nPEDIGREE SCORE\n" + "*"*50)
        string += f"\nPedigree score for {self.get_parent().get_name()}"
        for attr in vars(self):
            if not attr in ['DQS', 'parent']:
                string += f"\n{attr}: {getattr(self, attr)}"

        return string
    
    # ================================
    # Constructors
    # ================================
    @classmethod
    def from_parent(cls, parent):
        """ Create pedigree score object from parent. 
        
        Parameters
        ----------
        obj.
            Parent object.
        """
        pedigree_score = cls()
        pedigree_score.set_parent(parent)
        if parent is not None:
            for indicator in config['setup']['uncertainty']['DATA_QUALITY_INDICATORS']:
                setattr(pedigree_score, indicator, 5)

        parent.set_pedigree_score(pedigree_score)

        return pedigree_score

    # ================================
    # Setters and Getters
    # ================================
    def set_parent(self, obj):
        """ Set parent of the pedigree score.

        Parameters
        ----------
        obj : Master Obj.
            Object to which the pedigree score correspond.
        """ 
        self.parent = obj
        
        return self

    def set_item_DQS(self):
        """ Calculate and set the Data Quality Score of the pedigree score object.

        Returns
        -------
        int
            Data Quality Score.
        """
        DQS = 0.0
        ignore_list = ['parent', 'DQS']
        for attr in vars(self):
            if attr not in ignore_list:
                DQS += getattr(self, attr)

        self.DQS = DQS

        return DQS
    
    def get_parent(self):
        """ Get parent of the pedigree score.

        Returns
        ----------
        Master Obj.
            Object to which the pedigree score correspond.
        """ 
        return self.parent

    def get_item_DQS(self):
        """ Get the Data Quality Score of the object.
        
        Returns
        ----------
        float
            Data quality score of the object.
        """
        return self.DQS

    def update_pedigree_scores(self, *args):
        """ Update the pedigree score.

        Parameters
        ----------
        *args : tuple or dict
            An (indicator, score) pair or a dictionary of indicator-score pairs.

        Raises
        ------
        ValueError
            If the scores are not within the score ranges specified.
            If the input are not in expected format.
        """
        max = config['setup']['uncertainty']['MAX_DQS']
        min = config['setup']['uncertainty']['MIN_DQS']
        if len(args) == 1 and isinstance(args[0], dict):
            for indicator, score in args[0].items():
                if score >= min and score <= max:
                    if hasattr(self, indicator):
                        setattr(self, indicator, score)
                    else:
                        raise KeyError(f"{indicator} is not an valid indicator. Valid indicators are: {config['setup']['uncertainty']['DATA_QUALITY_INDICATORS']}")
                else:
                    raise ValueError(f"Pedigree score should be between {min} and {max}.")
        elif len(args) == 2:
            if args[1] >= min and args[1] <= max:
                setattr(self, args[0], args[1])
            else:
                raise ValueError(f"Pedigree score should be between {min} and {max}.")
        else:
            raise ValueError("Invalid input. Provide a (indicator, score) pair or a dictionary of indicator-score pairs.")

        return self
    

class DataQualityAnalysis:
    """ DataQualityAnalysis object carries out data quality analysis and stores pedigree data.

    Attributes
    ----------
    model : Model Obj.
        Model on which the hotspot analysis is performed.
    DQS : float
        Data Quality Score of the model.
    normalised_DQS : float
        Normalised Data Quality Score of the model
    """

    def __init__(self):
        self.model = None
        self.DQS = None
        self.normalised_DQS = None
        
    @classmethod
    def from_model(cls, model):
        data_quality_analysis = cls()
        data_quality_analysis.set_model(model)
        
        data_quality_analysis.setPedigreeScores()

        model.data_quality = data_quality_analysis

        return data_quality_analysis
    
    def set_model(self, model):
        """ Set a model to the Analyser.
        
        Parameters
        ----------
        model : Model Obj.
            Model on which the Data Quality Analysis is performed.        
        """
        self.model = model

    def set_model_DQS(self, DQS):
        """ Set Data Quality Score of the model.
        
        Parameters
        ----------
        DQS : float
            Data Quality Score.
        """
        self.DQS = DQS

    def set_normalised_DQS(self, nDQS):
        """ Set normalised Data Quality Score of the model.
        
        Parameters
        ----------
        nDQS : float
            Normalised Data Quality Score.
        """
        self.normalised_DQS = nDQS        

    def get_model(self):
        """ Get the model for which the analysis will be run.
        
        Returns
        ----------
        Model Obj.
            Model on which the Data Quality Analysis is performed.        
        """
        return self.model

    def get_model_DQS(self):
        """ Get Data Quality Score of the model.
        
        Returns
        -------
        float
            Data Quality Score.
        """
        return self.DQS

    def get_normalised_DQS(self):
        """ Get the normalised Data Quality Score of the model.
        
        Returns
        -------
        float
            Normalised Data Quality Score.
        """
        return self.normalised_DQS

    def setPedigreeScores(self):
        """ Set pedigree scores for all products/processes in a model.
        """
        for obj in self.model.get_all_items():
            PedigreeScore.from_parent(obj)
        
        self.setTemporalCorrelationScores()
        self.setGeographicalCorrelationScores()

        return self
    
    def setTemporalCorrelationScores(self):
        """ Update all Temporal Correlation scores.
        """
        pass 

    def setGeographicalCorrelationScores(self):
        """ Update all Temporal Correlation scores.
        """
        pass

    def calculate_model_DQS(self, impact_cat='GWP'):
        """ Calculate the Data Quality Score.

        Parameters
        ----------
        impact_cat : str
            Impact category considered for weighing individual pedigree scores.
        """
        DQS_tmp = 0.0
        impact_sum = 0.0
        for obj in self.model.get_all_items():
            impact = obj.get_impacts().get_weighted_impact() if impact_cat=='weighted' else obj.get_impacts().get_record(impact_cat) 
            if impact is not None:
                obj.get_pedigree_score().set_item_DQS()
                DQS_tmp += obj.get_pedigree_score().get_item_DQS() * impact
                impact_sum += impact
            else:
                log(f"{obj.get_name()} has no impacts.", "Info")

        DQS = DQS_tmp / impact_sum
        n = len(config['setup']['uncertainty']['DATA_QUALITY_INDICATORS'])
        max = config['setup']['uncertainty']['MAX_DQS']
        min = config['setup']['uncertainty']['MIN_DQS']
        normalized_DQS = 100 * (n * max - DQS)/(n * (max- min))

        self.set_model_DQS(DQS)
        self.set_normalised_DQS(normalized_DQS)

        return DQS, normalized_DQS
    
    def print_results(self):
        """ Print results of the hotspot analysis.
        """
        print("*"*50 + "\nDATA QUALITY ASSESSMENT\n" + "*"*50)
        print(f"Data Quality Score: {self.get_model_DQS():.2f}")
        print(f"Normalised Data Quality Score (0-100 scale): {self.get_normalised_DQS():.0f}")


if __name__ == '__main__':
    pass
