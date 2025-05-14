
from pod_lca.lca_modules.dynamic_radiative_forcing import DynamicRadiativeForcing

print(DynamicRadiativeForcing.get_pertubation_lifetime("CO2"))
print(DynamicRadiativeForcing.get_radiative_efficiency("CO2", ref_unit='Wm-2kg-1'))
