# This cell calculates dynamic characterization factors (DCFs) as described in 
# Levasseur et. al., 2010 : 
# DCF_inst = inst. rad. forcing from (t-1) to t
# DCF_cumulative = cumulative rad. forcing from 0 to t

# CH4 values w/o oxidation are appropriate for biogenic methane (see note in IPCC AR5 Ch8 Table 8.A.1)
# Ch4 oxidation to CO2 accounted for according to Boucher et. al. 2009 lower limit (50% CH4 oxidized to CO2, 50% deposited as formaldehyde)
# Link: https://iopscience.iop.org/article/10.1088/1748-9326/4/4/044007
# Alternatively, immediate full oxidation of CH4 to CO2 may be modelled, as in Levasseur's Dyn CO2 tool (https://ciraig.org/index.php/project/dynco2-dynamic-carbon-footprinter/)
# To align with IPCC AR4 fossil methane rf calculation, set alpha = 0.5 ; To align with Levasseur's Dyn CO2 tool, set alpha = 1.0


#--- Import python modules ---
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# --- Time settings ---
t_max = 500 #set the time horizon in years
k = 18
n_points = 2**k + 1 #required number of points to use romb numerical integration method (could use romb instead of Riemann sum integration)
t = np.linspace(0, t_max, n_points)
dt = t[1] - t[0]

# Create list of delayed emissions times, 0-500 yrs
t_yrs_list = range(t_max+1)

# Find t index for 20, 100, and 500 years
yr100_index = np.nonzero(t >= 100)[0][0]

# --- Decay function for all GHGs other than CO2 (first order exponential decay) ---
# Lifetime of GHGs in atmosphere, [years]
tau_CH4, tau_N2O = 12.4, 121

# Define decay functions for fraction of GHG 'i' in atmosphere, y_i
y_CH4 = np.exp(-t/tau_CH4)
y_N2O = np.exp(-t/tau_N2O)                

# --- Decay function for CO2 (Bern model) ---
# Define constants
a0, a1, a2, a3, tau1, tau2, tau3 = 0.2173, 0.2240, 0.2824, 0.2763, 394.4, 36.54, 4.304

#Define the Bern function
y_CO2 = a0 + a1*np.exp(-t/tau1) + a2*np.exp(-t/tau2) + a3*np.exp(-t/tau3)

# --- Define radiative efficiencies for GHGs from IPCC AR5 (RE_i) ---
RE_CO2, RE_CH4, RE_N2O = 1.37e-5, 3.63e-4, 3.00e-3
# RE_CO2, RE_CH4, RE_N2O = 1.7517e-15, 1.63e-13, 5.34e-13 #W/m2/kg

# See IPCC, "Anthropogenic and Natural Radiative Forcing" Chapter 8 Supp. Material section 8.SM.11
# "To convert the RE values given per ppbv values to per kg, they must be multiplied by (M_A/M_i)*(10^9/T_M) 
# where M_A is the mean molecular weight of air (28.97 kg kmol−1), M_i is the molecular weight of species i and 
# T_M is the total mass of the atmosphere, 5.1352 × 10^18 kg"
M_A = 28.97
M_CO2 = 44.01
M_CH4 = 16.04
M_N2O = 44.013
T_M = 5.1352e18

# The RE of CO2 is calculated as defined in the report section noted above; alternatively, a value of 1.7517e-15 W/m2/kg is provided
# A_CO2 = RE_CO2 * (M_A / M_CO2) * (1e9/T_M)
A_CO2 = 1.7517e-15
# "The RE of CH4 is scaled to include effects on ozone and stratospheric H2O," so that the A_CH4 becomes (1+f1+f2)*RE_CH4
f1, f2 = 0.5, 0.15
A_CH4 = (1+f1+f2)*(RE_CH4 * (M_A / M_CH4) * (1e9/T_M))
# "The indirect effect of increased N2O abundance on CH4 changes via stratospheric ozone, UV fluxes and OH levels is included in GWP... The reduction in CH4 (–36 molecules per +100 molecules N2O) offsets some of the climate impact from N2O emissions. A_N2O becomes:
A_N2O = (1-0.36*(1+f1+f2)*(RE_CH4/RE_N2O))*(RE_N2O * (M_A / M_N2O) * (1e9/T_M))
# print("Radiative Efficiencies of CO2, CH4, and N2O [W/m2/kg]:",A_CO2, A_CH4, A_N2O)

print(A_N2O)

# --- Calculate instantaneous radiative forcing for CO2, CH4, and N2O (IRF_CO2, CH4, N2O) ---
IRF_CO2 = A_CO2 * y_CO2
IRF_CH4 = A_CH4 * y_CH4
IRF_N2O = A_N2O * y_N2O


# --- Calculate the IRF of fossil CH4, including subsequent oxidation to CO2 (IRF_CH4fossil) ---
alpha = 1.0 # Fraction of CH4 assumed to be oxidized to CO2 (0.5 - 1.0) : Boucher 2009

#Calculate convolution of y_CO2 and y_CH4
convolution = np.convolve(y_CH4, y_CO2)[:len(t)] * dt

#Calculate IRF_CH4fossil
IRF_CH4fossil = IRF_CH4 + A_CO2 * ((alpha * M_CO2 / M_CH4)/tau_CH4) * convolution


#Initialize lists for time-adjusted warming potential (TAWP) dynamic characterization factor (DCF) results
DCFi_results_CO2 = []
DCFi_results_CH4 = []
DCFi_results_CH4fossil = []
DCFi_results_N2O = []
DCFc_results_CO2 = []
DCFc_results_CH4 = []
DCFc_results_CH4fossil = []
DCFc_results_N2O = []

# --- Integrate IRF from t = t-1 to t to calculate DCFinst. for CO2, CH4, N2O ---
for t_yr in t_yrs_list: #Start for loop at year 1, otherwise DCF inst will run into index error at year 0 - 1
    
    #initialize integral value at 0 for evaluation of DCFinst at each year
    DCFinst_CO2 = 0
    DCFinst_CH4 = 0
    DCFinst_CH4fossil = 0
    DCFinst_N2O = 0

    #Find the t_years and t_years_minus1 index in t list (upper and lower limits of integration) - skip if yr 0
    if not t_yr == 0:
        t_years_index = np.nonzero(t >= t_yr)[0][0]
        t_years_minus1 = np.nonzero(t >= (t_yr - 1))[0][0]

        #Riemann sum (left) evaluate integral from t-1 to t
        for i in range(t_years_minus1, t_years_index-1): #For left Riemann sum, stop iteration at second-to-last value
            #Add the IRF at index i
            DCFinst_CO2 += IRF_CO2[i] * dt
            DCFinst_CH4 += IRF_CH4[i] * dt
            DCFinst_CH4fossil += IRF_CH4fossil[i] * dt
            DCFinst_N2O += IRF_N2O[i] * dt

    else:
        DCFinst_CO2 = IRF_CO2[0]
        DCFinst_CH4 = IRF_CH4[0]
        DCFinst_CH4fossil = IRF_CH4fossil[0]
        DCFinst_N2O = IRF_N2O[0]

    # Once integral done, append result to result list
    DCFi_results_CO2.append(DCFinst_CO2)
    DCFi_results_CH4.append(DCFinst_CH4)
    DCFi_results_CH4fossil.append(DCFinst_CH4fossil)
    DCFi_results_N2O.append(DCFinst_N2O)

# --- Integrate IRF from t = 0 to t to calculate cumulative radiative forcing of pulse of CO2, CH4, N2O at yr 0 ---
CRF_CO2 = [0] #Initialize CRF first value at 0 b/c ~integral(n) = left riemann sum(n-1)
CRF_CH4 = [0]
CRF_CH4fossil = [0]
CRF_N2O = [0]
CRF_CO2_val = 0
CRF_CH4_val = 0
CRF_CH4fossil_val = 0
CRF_N2O_val = 0

# Use Riemann sum (left) to evaluate integral
for i in range(len(t)-1): #For left Riemann sum, stop iteration at second-to-last value
    #Calculate CRF at index i
    CRF_CO2_val += IRF_CO2[i] * dt
    CRF_CH4_val += IRF_CH4[i] * dt
    CRF_CH4fossil_val += IRF_CH4fossil[i] * dt
    CRF_N2O_val += IRF_N2O[i] * dt
    #Append value to CRF list
    CRF_CO2.append(CRF_CO2_val)
    CRF_CH4.append(CRF_CH4_val)
    CRF_CH4fossil.append(CRF_CH4fossil_val)
    CRF_N2O.append(CRF_N2O_val)

# --- Get DCF100c_results_i at yearly intervals --- 
for t_yr in t_yrs_list:
   
    #Find the t_years index in t list
    t_yr_index = np.nonzero(t >= t_yr)[0][0] 

    #Set the DCFc result equal to the CRF results at yearly intervals 
    DCFc_results_CO2.append(CRF_CO2[t_yr_index])
    DCFc_results_CH4.append(CRF_CH4[t_yr_index])
    DCFc_results_CH4fossil.append(CRF_CH4fossil[t_yr_index])
    DCFc_results_N2O.append(CRF_N2O[t_yr_index])
    
#Create dataframe with results
df = pd.DataFrame()
df['Year of Emission'] = t_yrs_list
df['DCF_inst CO2 [W/m2]'] =  DCFi_results_CO2
df['DCF_inst CH4 [W/m2]'] =  DCFi_results_CH4
df['DCF_inst CH4fossil [W/m2]'] =  DCFi_results_CH4fossil
df['DCF_inst N2O [W/m2]'] =  DCFi_results_N2O
df['DCF_cumul CO2 [W/m2]'] = DCFc_results_CO2
df['DCF_cumul CH4 [W/m2]'] = DCFc_results_CH4
df['DCF_cumul CH4fossil [W/m2]'] = DCFc_results_CH4fossil
df['DCF_cumul N2O [W/m2]'] = DCFc_results_N2O

#Print dataframe and export to CSV
print(df)
save_path = '/Users/etel5501/POD_LCA_Tool_2025/Dynamic Radiative Forcing methods/Levasseur_DCFs500_CH4fossil_5_27_25.csv'
df.to_csv(save_path, index=False)

# --- Plot DCF100inst results for CO2, CH4, and N2O ---
plt.plot(t_yrs_list, DCFi_results_CO2, label=f'DCF_inst CO2', color = 'blue')
plt.plot(t_yrs_list, DCFi_results_CH4, label=f'DCF_inst CH4', color = 'red')
plt.plot(t_yrs_list, DCFi_results_CH4fossil, label=f'DCF_inst CH4fossil', color = 'darkred')
plt.plot(t_yrs_list, DCFi_results_N2O, label=f'DCF_inst N2O', color = 'green')

# Add labels and title
plt.xlabel("time [years]")
plt.ylabel("DCF_inst (IRF) [W/m2]")

# Display the plot
plt.grid(True) # Add grid lines
plt.legend() # Add legend
plt.grid(visible=False) # Remove gridlines
plt.xlim(0, t_max)  # Set x-axis from 0 to t_max
plt.axhline(0, color='black', linewidth=1) # show horizonal axis
plt.show()

# --- Plot DCF100cumul results for CO2, CH4, and N2O ---
plt.plot(t_yrs_list, DCFc_results_CO2, label=f'DCF_cumul CO2', color = 'blue')
plt.plot(t_yrs_list, DCFc_results_CH4, label=f'DCF_cumul CH4', color = 'red')
plt.plot(t_yrs_list, DCFc_results_CH4fossil, label=f'DCF_cumul CH4fossil', color = 'darkred')
plt.plot(t_yrs_list, DCFc_results_N2O, label=f'DCF_cumul N2O', color = 'green')


# Add labels and title 
plt.xlabel("time [years]")
plt.ylabel("DCF_cumul (CRF) [W/m2]")

# Display the plot 
plt.grid(True) # Add grid lines
plt.legend() # Add legend
plt.grid(visible=False) # Remove gridlines
plt.xlim(0, t_max)  # Set x-axis from 0 to t_max
plt.axhline(0, color='black', linewidth=1) # show horizonal axis
plt.show()

