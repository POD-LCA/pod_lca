
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from pathlib import Path

from ..impacts import Emissions
from ..impacts import EOLImpactsDatabase
from ..impacts import Impacts
from ..impacts import ImpactsDatabase
from ..transportation import EOLTransportDataset
from ...utilities import config


class EndOfLifeMixins:

    # ================================
    # Database Methods
    # ================================    
    def set_eol_process_impact_database(self, file_path=None, **kwargs):
        """ Set the impact database for end-of-life impacts. If file path not given, default database will be used.
        
        Parameters
        ----------
        file_path : str
            Filepath of the csv file containing impact data.

        Other Parameters
        ----------------
        primary_key : str
            Header of the primary identifier column in the csv file. Default is 'Material'.
        process_key : str
            Header of the process identifier column in the csv file. Default is 'Process'.
        lc_stage_key : str
            Header of the life cycle stage identifier column in the csv file. Default is 'LCA Stage'.
        transport_dataset : ~pod_lca.transportation.TransportDataset
            Transportation dataset corresponding to the end-of-life impacts.
        """
        if file_path is None:
            file_path = config['file_paths']['eol']['EOL_PROCESS_IMPACTS']
        
        if isinstance(file_path, (str, Path)):
            primary_key = kwargs['primary_key'] if 'primary_key' in kwargs else 'Material'
            process_key = kwargs['process_key'] if 'process_key' in kwargs else 'Process'
            lc_stage_key = kwargs['lc_stage_key'] if 'lc_stage_key' in kwargs else 'LCA Stage'

            eol_impact_database = EOLImpactsDatabase.new("EOL database")

            eol_impact_database.set_primary_key(primary_key)
            eol_impact_database.set_process_key(process_key)
            eol_impact_database.set_life_cycle_stage_key(lc_stage_key)
            eol_impact_database.set_data(file_path)

            self.eol_impact_database = eol_impact_database

        else:
            raise TypeError("Database input not recognized")
        
        return self
    
    def set_eol_demolition_impact_database(self, file_path=None, **kwargs):
        """ Set the demolition impact database for end-of-life impacts. If file path not given, default database will be used.
        
        Parameters
        ----------
        file_path : str
            Filepath of the csv file containing impact data.

        Other Parameters
        ----------------
        primary_key : str
            Header of the primary identifier column in the csv file. Default is 'Material'.
        """
        if file_path is None:
            file_path = config['file_paths']['eol']['EOL_DEMOLITION_IMPACTS']

        if isinstance(file_path, (str, Path)):
            primary_key = kwargs['primary_key'] if 'primary_key' in kwargs else 'Material'

            demolition_impact_database = ImpactsDatabase.new("demolition database")

            demolition_impact_database.set_primary_key(primary_key)
            demolition_impact_database.set_data(file_path)

            self.eol_demolition_impact_database = demolition_impact_database
        else:
            raise TypeError("Database input not recognized")
        
        return self
    
    def set_eol_transport_dataset(self, dataset=None):
        """ Set transportation dataset for the end-of-life impacts.

        Parameters
        ----------
        dataset : ~pod_lca.transportation.TransportDataset
            End-of-life transportation dataset.
        """
        if dataset is None:
            dataset = EOLTransportDataset()

        self.eol_transport_dataset = dataset

        return self
    
    def get_transportation_impact_database(self):
        """ Set the impact database for end-of-life impacts.
        
        Returns
        -------
        ~pod_lca.impacts.ImpactsDatabase
            End-of-Life impacts database.
        """
        return self.transport_impact_database
    
    def get_eol_process_impact_database(self):
        """ Get the impact database for end-of-life impacts.
        
        Returns
        -------
        ~pod_lca.impacts.ImpactsDatabase
            End-of-Life impacts database.
        """
        return self.eol_impact_database
    
    def get_eol_demolition_database(self):
        """ Get the demolition impact database for end-of-life impacts.
        
        Returns
        -------
        ~pod_lca.impacts.ImpactsDatabase
            End-of-Life demolition impacts database.
        """
        return self.eol_demolition_impact_database

    def get_eol_transport_dataset(self):
        """ Get transportation dataset for the end-of-life impacts.

        Returns
        -------
        ~pod_lca.transportation.TransportDataset
            End-of-life transportation dataset.
        """
        return self.eol_transport_dataset

    # ================================
    # Inventory Records Methods
    # ================================ 
    def get_eol_impacts(self, lc_stage=None):
        """ Get C2-C4 impacts of the building.

        Parameters
        ----------
        lc_stage: {'C1', 'C2', 'C3', 'C4', None}
            Life cycle stage for which the impacts to be calculated. 
            If None, gives impacts for all the relevant life cycle stages. 
            Default is None.
        
        Returns
        -------
        ~pod_lca.impacts.Impacts
            C2-C4 impacts of the building.
        """
        impacts = Impacts.from_parent(self)
        for assembly in self.get_assemblies():
            for material in assembly.get_materials():
                if lc_stage is None:
                    for impact_lst in material.get_waste_product().get_impacts().values():
                        if isinstance(impact_lst, Impacts):
                            impacts += impact_lst
                            continue
                        for impact in impact_lst:
                            impacts += impact
                else:
                    impact_lst = material.get_waste_product().get_impacts()[lc_stage]
                    if isinstance(impact_lst, Impacts):
                        impacts += impact_lst
                        continue
                    for impact in impact_lst:
                        impacts += impact      
        # TODO: test with the envelope assemblies

        return impacts

    def get_eol_emissions(self, lc_stage=None):
        """ Get C2-C4 emissions of the building.
        
        Parameters
        ----------
        lc_stage: {'C1', 'C2', 'C3', 'C4', None}
            Life cycle stage for which the emissions to be calculated. 
            If None, gives emissions for all the relevant life cycle stages. 
            Default is None.

        Returns
        -------
        ~pod_lca.impacts.Emissions
            C2-C4 emissions of the building.
        """        
        emissions = Emissions.from_parent(self)
        for assembly in self.get_assemblies():
            for material in assembly.get_materials():
                if lc_stage is None:
                    for emission_lst in material.get_waste_product().get_emissions().values():
                        if isinstance(emission_lst, Emissions):
                            emissions += emission_lst
                            continue
                        for emission in emission_lst:
                            emissions += emission
                else:
                    emission_lst = material.get_waste_product().get_emissions()[lc_stage]
                    if isinstance(emission_lst, Emissions):
                        emissions += emission_lst
                        continue
                    for emission in emission_lst:
                        emissions += emission  
                        
        # TODO: test with the envelope assemblies

        return emissions


if __name__ == '__main__':
    pass
