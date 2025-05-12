# POD|LCA Data Files

This folder contains data files (CSV and JSON) required by the POD|LCA Python framework.

## File naming convention

The following file naming convention is used:

> \<pod lca module name\>\_\<data source abbrevation\>\_\<data descriptor>\.\<file extension\>

## Data record

| # | File name | Module name | Data descriptor | Notes |
|---|-----------|-------------|-----------------|-------|
| 1 | location_netl_ferc-ba-mapping.csv | location | maps FERC regions to Balancing Areas via zip codes |  |
| 2 | impacts_podlca_material-data.csv | impacts | |  |
| 3 | transportation_podlca_emission.csv | transportation |  |  |
| 4 | transportation_cfaf_dataset.csv | transportation |  |  |
| 5 | transportation_cfs_dataset.csv | transportation |  |  |
| 6 | transportation_cfs_state-code.csv | transportation |  |  |
| 7 | transportation_faf_dataset.csv | transportation |  |  |
| 8 | transportation_faf_domestic-region.json | transportation |  |  |
| 9 | transportation_faf_foreign-region.json | transportation |  |  |
| 10 | transportation_faf_foreign-region-countries.json | transportation |  |  |
| 11 | transportation_podlca_dist-fr.csv | transportation |  |  |
| 12 | transportation_podlca_faf-city-representation.json | transportation |  |  |
| 13 | transportation_podlca_faf-dist-band.csv | transportation |  |  |
| 14 | transportation_podlca_marine.csv | transportation |  |  |
| 15 | transportation_podlca_material.csv | transportation |  |  |
| 16 | transportation_podlca_sensitive-material.csv | transportation |  |  |
| 17 | transportation_podlca_us-coast.json | transportation |  |  |
| 18 | impacts_podlca_eol-impacts.csv | impacts |  |  |
| 19 | electricity_netl_national-consumption-impacts-by-technology.csv | electricity | impacts of electricity generation by technology type - US average |  |
| 20 | electricity_netl_regional-consumption-impacts-by-technology.csv | electricity | impacts of electricity generation by technology type and FERC region |  |
| 21 | impacts_flcac_categorized-data.csv | impacts |  |  |
| 22 | impacts_flcac_categories.json | impacts |  |  |
| 23 | impacts_nist_weighting-factors.json | impacts |  |  |
| 24 | impacts_epa_weighting-factors.json | impacts |  |  |
| 25 | impacts_clf_normalization-factors.json | impacts |  |  |
| 26 | impacts_ecoinvent391_categorized-data.csv | impacts |  |  |
| 27 | impacts_ecoinvent391_categories.json | impacts |  |  |
| 28 | impacts_ecoinvent391_electricity-group.csv| impacts |  |  |
| 29 | impacts_ecoinvent391_emission-inventories.json| impacts |  |  |
| 30 | impacts_ecoinvent391_heating-values.csv| impacts |  |  |
| 31 | impacts_ecoinvent391_nonrenewable-fuels-group.csv| impacts |  |  |
| 32 | impacts_ecoinvent391_renewable-fuels-group.csv| impacts |  |  |
| 33 | impacts_ecoinvent391_renewable-fuels-group-no-wood-chips.csv| impacts |  |  |
| 34 | impacts_ecoinvent391_uuid-list-with-wood-chips.csv| impacts |  |  |
| 35 | impacts_flcac_emission-inventories.json| impacts |  |  |
| 36 | impacts_flcac_heating-values.csv| impacts |  |  |
| 37 | impacts_flcac_nonrenewable-fuels-group.csv| impacts |  |  |
| 38 | impacts_flcac_renewable-fuels-group.csv| impacts |  |  |
| 39 | electricity_netl_electricity-technologies.csv| electricity | list of electricity technologies classification categories used by NETL |  |
| 40 | electricity_cambium_consumption-local.csv| electricity | electricity consumption predictions for USA, by ReEDS Balancing Areas | https://scenarioviewer.nrel.gov/|
| 41 | electricity_cambium_consumption-national.csv| electricity | electricity consumption predictions for USA | https://scenarioviewer.nrel.gov/ |
| 42 | electricity_cambium_consumption-regional.csv| electricity | electricity consumption predictions for USA, by GEA regions | https://scenarioviewer.nrel.gov/ |
| 43 | electricity_cambium_regions-map.json| electricity | mapping of ReEDS Balancing Areas to GEA regions |  |
| 44 | electricity_cambium_technology-headers.json| electricity | mapping of electricity technologies from Cambium to the headers in Cambium electricity consumption predictions |  |
| 45 | electricity_cambium_technology-map.json| electricity | mapping of electricity technologies from Cambium to NETL |  |
| 46 | eol_podlca_default-mixes.csv| end-of-life | default end-of-life fate mixes for materials |  |
| 47 | impacts_uslci_electricity.csv| impacts | impact and emission data for electricity | https://www.lcacommons.gov/lca-collaboration/Federal_LCA_Commons/US_electricity_baseline/datasets |
| 48 | location_cambium_gea-reeds-zip-mapping.csv| location | mapping of US zip codes to GEA regions and ReEDS balancing areas | https://catalog.data.gov/dataset/long-run-marginal-co2-emission-rates-workbooks-for-2020-standard-scenarios-cambium-data-24bbb/resource/12cee2ee-a20e-415c-9de8-4d6ac8ea8064 |
| 49 | location_doe_ba-zip-mapping.csv| location | mapping of US zip codes to balancing area | https://www.energy.gov/femp/balancing-authority-lookup-tool |
