
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


class PedigreeScore:
    """
    PedigreeScore object contains background data for data quality scores.

    Attributes
    ----------
    parent : Master Obj.
        Product/Process object for which the data quality is related.
    <indicators> : float
        Data Quality Indicators are dynamically set based on the Data Quality Analysis (DQA) used.
    """

    def __init__(self, parent, indicators):
        self.parent = parent
        if parent is not None:
            for impact in indicators:
                setattr(self, impact, 5)

    def calculate_DQS(self):
        """ Calculate the Data Quality Score of the pedigree score object.

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

        return DQS

class DataQualityAnalysis:
    """
    DataQualityAnalysis object carries out data quality analysis and stores pedigree data.

    Attributes
    ----------
    project : Project Obj.
        Project on which the calculator operates.
    indicators : list of str.
        List of data quality indicators.
    max_score : int
        Maximum possible score for an indicator.
    min_score : int
        Minimum possible score for an indicator.
    pedigreeScores : dict of dict of list
        {model_name (str): {master_product (Master Obj): pedigree_score (PedigreeScore Obj)} .
    """
    def __init__(self, project):
        self.project =  project
        self.indicators = ['reliability', 'completeness', 'temporal correlation', 'geographical correlation', 'technological representativeness']
        self.max_score = 5
        self.min_score = 1
        self.pedigreeScores = dict.fromkeys(project.get_model_names(), [])

        project.DataQualityAnalysis = self

    def get_indicators(self):
        """ Get a list of data quality indicators.
        
            Returns
            -------
            list of str.
                List of data quality indicators.
        """

        return self.indicators
    
    def setPedigreeScores(self, model_name):
        """ Set pedigree scores for all products/processes in a model.
        
            Partameters
            -----------
            model_name : str
                Name of the model.
        """

        model = self.project.get_model(model_name)
        self.pedigreeScores[model_name] = {}
        for obj in model.get_processes() + model.get_products():
            pedigree_score = PedigreeScore(obj, self.get_indicators())
            self.pedigreeScores[model_name][obj] = pedigree_score
        
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

    def update_pedigree_scores(self, model_name, obj, *args):
        """ Update the pedigree score of an object.

            Parameters
            ----------
            model_name : str
                Name of the model.
            obj : Master obj
                Master object for which the pedigree score is being updated.
            *args : tuple or dict
                An (indicator, score) pair or a dictionary of indicator-score pairs.

            Raises
            ------
            ValueError
                If the scores are not within the score ranges specified.
                If the input are not in expected format.

        """

        pedigree_score = self.pedigreeScores[model_name][obj]

        if len(args) == 1 and isinstance(args[0], dict):
            for indicator, score in args[0].items():
                if score >= self.min_score and score <= self.max_score:
                    if hasattr(pedigree_score, indicator):
                        setattr(pedigree_score, indicator, score)
                    else:
                        raise KeyError(f"{indicator} is not an valid indicator. Valid indicators are: {self.indicators}")
                else:
                    raise ValueError(f"Pedigree score should be between {self.min_score} and {self.max_score}.")
        elif len(args) == 2:
            if args[1] >= self.min_score and args[1] <= self.max_score:
                setattr(pedigree_score, args[0], args[1])
            else:
                raise ValueError(f"Pedigree score should be between {self.min_score} and {self.max_score}.")
        else:
            raise ValueError("Invalid input. Provide a (indicator, score) pair or a dictionary of indicator-score pairs.")

        return pedigree_score

    def calculate_DQS(self, model_name, impact_cat='weighted', printout=True):
        """ Calculate the Data Quality Score.

            Parameters
            ----------
            model_name : str
                Name of the model for which the Data Quality Score is calculated.
            impact_cat : str
                Impact category considered for weighing individual pedigree scores.
            Printout : bool
                Print the output, if True.
        """

        DQS_tmp = 0.0
        impact_sum = 0.0
        for obj in self.pedigreeScores[model_name]:
            impact = obj.get_impacts().get_weighted_impact() if impact_cat=='weighted' else obj.get_impacts().get_impact(impact_cat) 
            if impact is not None:
                DQS_tmp += self.pedigreeScores[model_name][obj].calculate_DQS() * impact
                impact_sum += impact
            else:
                print(f"{obj.get_name()} has no impacts.")

        DQS = DQS_tmp / impact_sum
        n = len(self.indicators)
        normalized_DQS = 100 * (n * self.max_score - DQS)/(n * (self.max_score - self.min_score))

        if printout:
            print("*"*50 + "\nDATA QUALITY ASSESSMENT\n" + "*"*50)
            print(f"Data Quality Score: {DQS:.2f}")
            print(f"Normalised Data Quality Score (0-100 scale): {normalized_DQS:.0f}")

        return normalized_DQS
