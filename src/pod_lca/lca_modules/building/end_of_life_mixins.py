
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from ..impacts import Emissions
from ..impacts import EOLImpactsDatabase
from ..impacts import Impacts
from ..transportation import EOLTransportDataset


class EndOfLifeMixins:

    # ================================
    # Database Methods
    # ================================    
    def set_eol_database(self, file_path, **kwargs):
        """ Set the impact database for end-of-life impacts.
        
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
        primary_key = kwargs['primary_key'] if 'primary_key' in kwargs else 'Material'
        process_key = kwargs['process_key'] if 'process_key' in kwargs else 'Process'
        lc_stage_key = kwargs['lc_stage_key'] if 'lc_stage_key' in kwargs else 'LCA Stage'
        transport_dataset = kwargs['transport_dataset'] if 'transport_dataset' in kwargs else EOLTransportDataset()

        eol_impact_database = EOLImpactsDatabase.new("EOL database")

        eol_impact_database.set_primary_key(primary_key)
        eol_impact_database.set_process_key(process_key)
        eol_impact_database.set_life_cycle_stage_key(lc_stage_key)
        eol_impact_database.set_data(file_path)

        self.eol_impact_database = eol_impact_database

        self.set_eol_transport_dataset(transport_dataset)

        return self
    
    def set_eol_transport_dataset(self, dataset):
        """ Set transportation dataset for the end-of-life impacts.

        Parameters
        ----------
        dataset : ~pod_lca.transportation.TransportDataset
            End-of-life transportation dataset.
        """
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
    
    def get_eol_database(self):
        """ Get the impact database for end-of-life impacts.
        
        Returns
        -------
        ~pod_lca.impacts.ImpactsDatabase
            End-of-Life impacts database.
        """
        return self.eol_impact_database

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
                        for impact in impact_lst:
                            impacts += impact
                else:
                    for impact in material.get_waste_product().get_impacts()[lc_stage]:
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
                    for emission_lst in material.get_waste_product().get_impacts().values():
                        for emission in emission_lst:
                            emissions += emission
                else:
                    for emission in material.get_waste_product().get_impacts()[lc_stage]:
                        emissions += emission  
                        
        # TODO: test with the envelope assemblies

        return emissions


if __name__ == '__main__':
    pass
