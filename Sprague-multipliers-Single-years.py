import os
import pandas as pd
import numpy as np

## Loading the data we obtained from the QGIS routine

os.chdir("C:\\Users\\g.vargas\\BOX\\IIEP_MyProjects\\MP_01000298_RND_SDA\\WorkFiles_Experts\\298-Issue-Papers\\298-Issue-Paper-Sprague\\Replication files\\Data\\Tables\\Bangladesh") ## Replace this be your own folder
data = pd.read_csv("Administrative boundaries - Level 4 - Untreated.csv") ## Note that 
PopulationEstimates = pd.DataFrame(data, columns = ['ADM4_PCODE', 'F_0_to_1sum', 'F_1_to_4sum', 'F_5_to_9sum', 'F_10_to_14sum', 'F_15_to_19sum', 'F_20_to_24sum', 'F_25_to_29sum', 'F_30_to_34sum', 'F_35_to_39sum', 'M_0_to_1sum', 'M_1_to_4sum', 'M_5_to_9sum', 'M_10_to_14sum', 'M_15_to_19sum', 'M_20_to_24sum', 'M_25_to_29sum', 'M_30_to_34sum', 'M_35_to_39sum'])

## We first create the variable for the groups 0 to 4 years

PopulationEstimates['M_0_to_4sum'] = PopulationEstimates['M_0_to_1sum'] + PopulationEstimates['M_1_to_4sum']
PopulationEstimates['F_0_to_4sum'] = PopulationEstimates['F_0_to_1sum'] + PopulationEstimates['F_1_to_4sum']

## We proceed to create the groups population by single years of age using the Sprague multipliers

# Male

PopulationEstimates['Y_M_0'] = 0.3616*PopulationEstimates['M_0_to_4sum'] - 0.2768*PopulationEstimates['M_5_to_9sum'] + 0.1488*PopulationEstimates['M_10_to_14sum'] - 0.0336*PopulationEstimates['M_15_to_19sum'] 
PopulationEstimates['Y_M_1'] = 0.2640*PopulationEstimates['M_0_to_4sum'] - 0.0960*PopulationEstimates['M_5_to_9sum'] + 0.0400*PopulationEstimates['M_10_to_14sum'] - 0.0080*PopulationEstimates['M_15_to_19sum'] 
PopulationEstimates['Y_M_2'] = 0.1840*PopulationEstimates['M_0_to_4sum'] + 0.0400*PopulationEstimates['M_5_to_9sum'] - 0.0320*PopulationEstimates['M_10_to_14sum'] + 0.0080*PopulationEstimates['M_15_to_19sum'] 
PopulationEstimates['Y_M_3'] = 0.1200*PopulationEstimates['M_0_to_4sum'] + 0.1360*PopulationEstimates['M_5_to_9sum'] - 0.0720*PopulationEstimates['M_10_to_14sum'] + 0.0160*PopulationEstimates['M_15_to_19sum'] 
PopulationEstimates['Y_M_4'] = PopulationEstimates['M_0_to_4sum'] - PopulationEstimates['Y_M_0'] - PopulationEstimates['Y_M_1'] - PopulationEstimates['Y_M_2'] - PopulationEstimates['Y_M_3']
PopulationEstimates['Y_M_5'] = 0.0336*PopulationEstimates['M_0_to_4sum'] + 0.2272*PopulationEstimates['M_5_to_9sum'] - 0.0752*PopulationEstimates['M_10_to_14sum'] + 0.0144*PopulationEstimates['M_15_to_19sum'] 
PopulationEstimates['Y_M_6'] = 0.0080*PopulationEstimates['M_0_to_4sum'] + 0.2320*PopulationEstimates['M_5_to_9sum'] - 0.0480*PopulationEstimates['M_10_to_14sum'] + 0.0080*PopulationEstimates['M_15_to_19sum'] 
PopulationEstimates['Y_M_7'] = -0.0080*PopulationEstimates['M_0_to_4sum'] + 0.2160*PopulationEstimates['M_5_to_9sum'] - 0.0080*PopulationEstimates['M_10_to_14sum'] + 0.0000*PopulationEstimates['M_15_to_19sum']
PopulationEstimates['Y_M_8'] = -0.0160*PopulationEstimates['M_0_to_4sum'] + 0.1840*PopulationEstimates['M_5_to_9sum'] + 0.0400*PopulationEstimates['M_10_to_14sum'] - 0.0080*PopulationEstimates['M_15_to_19sum']
PopulationEstimates['Y_M_9'] = PopulationEstimates['M_5_to_9sum'] - PopulationEstimates['Y_M_5'] - PopulationEstimates['Y_M_6'] - PopulationEstimates['Y_M_7'] - PopulationEstimates['Y_M_8']
PopulationEstimates['Y_M_10'] = -0.0128*PopulationEstimates['M_0_to_4sum'] + 0.0848*PopulationEstimates['M_5_to_9sum'] + 0.1504*PopulationEstimates['M_10_to_14sum'] - 0.0240*PopulationEstimates['M_15_to_19sum'] + 0.0016*PopulationEstimates['M_20_to_24sum']
PopulationEstimates['Y_M_11'] = -0.0016*PopulationEstimates['M_0_to_4sum'] + 0.0144*PopulationEstimates['M_5_to_9sum'] + 0.2224*PopulationEstimates['M_10_to_14sum'] - 0.0416*PopulationEstimates['M_15_to_19sum'] + 0.0064*PopulationEstimates['M_20_to_24sum']
PopulationEstimates['Y_M_12'] = 0.0064*PopulationEstimates['M_0_to_4sum'] - 0.0336*PopulationEstimates['M_5_to_9sum'] + 0.2544*PopulationEstimates['M_10_to_14sum'] - 0.0336*PopulationEstimates['M_15_to_19sum'] + 0.0064*PopulationEstimates['M_20_to_24sum']
PopulationEstimates['Y_M_13'] = 0.0064*PopulationEstimates['M_0_to_4sum'] - 0.0416*PopulationEstimates['M_5_to_9sum'] + 0.2224*PopulationEstimates['M_10_to_14sum'] + 0.0144*PopulationEstimates['M_15_to_19sum'] - 0.0016*PopulationEstimates['M_20_to_24sum']
PopulationEstimates['Y_M_14'] = PopulationEstimates['M_10_to_14sum'] - PopulationEstimates['Y_M_10'] - PopulationEstimates['Y_M_11'] - PopulationEstimates['Y_M_12'] - PopulationEstimates['Y_M_13']
PopulationEstimates['Y_M_15'] = -0.0128*PopulationEstimates['M_5_to_9sum'] + 0.0848*PopulationEstimates['M_10_to_14sum'] + 0.1504*PopulationEstimates['M_15_to_19sum'] - 0.0240*PopulationEstimates['M_20_to_24sum'] + 0.0016*PopulationEstimates['M_25_to_29sum']
PopulationEstimates['Y_M_16'] = -0.0016*PopulationEstimates['M_5_to_9sum'] + 0.0144*PopulationEstimates['M_10_to_14sum'] + 0.2224*PopulationEstimates['M_15_to_19sum'] - 0.0416*PopulationEstimates['M_20_to_24sum'] + 0.0064*PopulationEstimates['M_25_to_29sum']
PopulationEstimates['Y_M_17'] = 0.0064*PopulationEstimates['M_5_to_9sum'] - 0.0336*PopulationEstimates['M_10_to_14sum'] + 0.2544*PopulationEstimates['M_15_to_19sum'] - 0.0336*PopulationEstimates['M_20_to_24sum'] + 0.0064*PopulationEstimates['M_25_to_29sum']
PopulationEstimates['Y_M_18'] = 0.0064*PopulationEstimates['M_5_to_9sum'] - 0.0416*PopulationEstimates['M_10_to_14sum'] + 0.2224*PopulationEstimates['M_15_to_19sum'] + 0.0144*PopulationEstimates['M_20_to_24sum'] - 0.0016*PopulationEstimates['M_25_to_29sum']
PopulationEstimates['Y_M_19'] = PopulationEstimates['M_15_to_19sum'] - PopulationEstimates['Y_M_15'] - PopulationEstimates['Y_M_16'] - PopulationEstimates['Y_M_17'] - PopulationEstimates['Y_M_18']
PopulationEstimates['Y_M_20'] = -0.0128*PopulationEstimates['M_10_to_14sum'] + 0.0848*PopulationEstimates['M_15_to_19sum'] + 0.1504*PopulationEstimates['M_20_to_24sum'] - 0.0240*PopulationEstimates['M_25_to_29sum'] + 0.0016*PopulationEstimates['M_30_to_34sum']
PopulationEstimates['Y_M_21'] = -0.0016*PopulationEstimates['M_10_to_14sum'] + 0.0144*PopulationEstimates['M_15_to_19sum'] + 0.2224*PopulationEstimates['M_20_to_24sum'] - 0.0416*PopulationEstimates['M_25_to_29sum'] + 0.0064*PopulationEstimates['M_30_to_34sum']
PopulationEstimates['Y_M_22'] = 0.0064*PopulationEstimates['M_10_to_14sum'] - 0.0336*PopulationEstimates['M_15_to_19sum'] + 0.2544*PopulationEstimates['M_20_to_24sum'] - 0.0336*PopulationEstimates['M_25_to_29sum'] + 0.0064*PopulationEstimates['M_30_to_34sum']
PopulationEstimates['Y_M_23'] = 0.0064*PopulationEstimates['M_10_to_14sum'] - 0.0416*PopulationEstimates['M_15_to_19sum'] + 0.2224*PopulationEstimates['M_20_to_24sum'] + 0.0144*PopulationEstimates['M_25_to_29sum'] - 0.0016*PopulationEstimates['M_30_to_34sum']
PopulationEstimates['Y_M_24'] = PopulationEstimates['M_20_to_24sum'] - PopulationEstimates['Y_M_20'] - PopulationEstimates['Y_M_21'] - PopulationEstimates['Y_M_22'] - PopulationEstimates['Y_M_23']
PopulationEstimates['Y_M_25'] = -0.0128*PopulationEstimates['M_15_to_19sum'] + 0.0848*PopulationEstimates['M_20_to_24sum'] + 0.1504*PopulationEstimates['M_25_to_29sum'] - 0.0240*PopulationEstimates['M_30_to_34sum'] + 0.0016*PopulationEstimates['M_35_to_39sum']
PopulationEstimates['Y_M_26'] = -0.0016*PopulationEstimates['M_15_to_19sum'] + 0.0144*PopulationEstimates['M_20_to_24sum'] + 0.2224*PopulationEstimates['M_25_to_29sum'] - 0.0416*PopulationEstimates['M_30_to_34sum'] + 0.0064*PopulationEstimates['M_35_to_39sum']
PopulationEstimates['Y_M_27'] = 0.0064*PopulationEstimates['M_15_to_19sum'] - 0.0336*PopulationEstimates['M_20_to_24sum'] + 0.2544*PopulationEstimates['M_25_to_29sum'] - 0.0336*PopulationEstimates['M_30_to_34sum'] + 0.0064*PopulationEstimates['M_35_to_39sum']
PopulationEstimates['Y_M_28'] = 0.0064*PopulationEstimates['M_15_to_19sum'] - 0.0416*PopulationEstimates['M_20_to_24sum'] + 0.2224*PopulationEstimates['M_25_to_29sum'] + 0.0144*PopulationEstimates['M_30_to_34sum'] - 0.0016*PopulationEstimates['M_35_to_39sum']
PopulationEstimates['Y_M_29'] = PopulationEstimates['M_25_to_29sum'] - PopulationEstimates['Y_M_25'] - PopulationEstimates['Y_M_26'] - PopulationEstimates['Y_M_27'] - PopulationEstimates['Y_M_28']

# Female

PopulationEstimates['Y_F_0'] = 0.3616*PopulationEstimates['F_0_to_4sum'] - 0.2768*PopulationEstimates['F_5_to_9sum'] + 0.1488*PopulationEstimates['F_10_to_14sum'] - 0.0336*PopulationEstimates['F_15_to_19sum'] 
PopulationEstimates['Y_F_1'] = 0.2640*PopulationEstimates['F_0_to_4sum'] - 0.0960*PopulationEstimates['F_5_to_9sum'] + 0.0400*PopulationEstimates['F_10_to_14sum'] - 0.0080*PopulationEstimates['F_15_to_19sum'] 
PopulationEstimates['Y_F_2'] = 0.1840*PopulationEstimates['F_0_to_4sum'] + 0.0400*PopulationEstimates['F_5_to_9sum'] - 0.0320*PopulationEstimates['F_10_to_14sum'] + 0.0080*PopulationEstimates['F_15_to_19sum'] 
PopulationEstimates['Y_F_3'] = 0.1200*PopulationEstimates['F_0_to_4sum'] + 0.1360*PopulationEstimates['F_5_to_9sum'] - 0.0720*PopulationEstimates['F_10_to_14sum'] + 0.0160*PopulationEstimates['F_15_to_19sum'] 
PopulationEstimates['Y_F_4'] = PopulationEstimates['F_0_to_4sum'] - PopulationEstimates['Y_F_0'] - PopulationEstimates['Y_F_1'] - PopulationEstimates['Y_F_2'] - PopulationEstimates['Y_F_3']
PopulationEstimates['Y_F_5'] = 0.0336*PopulationEstimates['F_0_to_4sum'] + 0.2272*PopulationEstimates['F_5_to_9sum'] - 0.0752*PopulationEstimates['F_10_to_14sum'] + 0.0144*PopulationEstimates['F_15_to_19sum'] 
PopulationEstimates['Y_F_6'] = 0.0080*PopulationEstimates['F_0_to_4sum'] + 0.2320*PopulationEstimates['F_5_to_9sum'] - 0.0480*PopulationEstimates['F_10_to_14sum'] + 0.0080*PopulationEstimates['F_15_to_19sum'] 
PopulationEstimates['Y_F_7'] = -0.0080*PopulationEstimates['F_0_to_4sum'] + 0.2160*PopulationEstimates['F_5_to_9sum'] - 0.0080*PopulationEstimates['F_10_to_14sum'] + 0.0000*PopulationEstimates['F_15_to_19sum']
PopulationEstimates['Y_F_8'] = -0.0160*PopulationEstimates['F_0_to_4sum'] + 0.1840*PopulationEstimates['F_5_to_9sum'] + 0.0400*PopulationEstimates['F_10_to_14sum'] - 0.0080*PopulationEstimates['F_15_to_19sum']
PopulationEstimates['Y_F_9'] = PopulationEstimates['F_5_to_9sum'] - PopulationEstimates['Y_F_5'] - PopulationEstimates['Y_F_6'] - PopulationEstimates['Y_F_7'] - PopulationEstimates['Y_F_8']
PopulationEstimates['Y_F_10'] = -0.0128*PopulationEstimates['F_0_to_4sum'] + 0.0848*PopulationEstimates['F_5_to_9sum'] + 0.1504*PopulationEstimates['F_10_to_14sum'] - 0.0240*PopulationEstimates['F_15_to_19sum'] + 0.0016*PopulationEstimates['F_20_to_24sum']
PopulationEstimates['Y_F_11'] = -0.0016*PopulationEstimates['F_0_to_4sum'] + 0.0144*PopulationEstimates['F_5_to_9sum'] + 0.2224*PopulationEstimates['F_10_to_14sum'] - 0.0416*PopulationEstimates['F_15_to_19sum'] + 0.0064*PopulationEstimates['F_20_to_24sum']
PopulationEstimates['Y_F_12'] = 0.0064*PopulationEstimates['F_0_to_4sum'] - 0.0336*PopulationEstimates['F_5_to_9sum'] + 0.2544*PopulationEstimates['F_10_to_14sum'] - 0.0336*PopulationEstimates['F_15_to_19sum'] + 0.0064*PopulationEstimates['F_20_to_24sum']
PopulationEstimates['Y_F_13'] = 0.0064*PopulationEstimates['F_0_to_4sum'] - 0.0416*PopulationEstimates['F_5_to_9sum'] + 0.2224*PopulationEstimates['F_10_to_14sum'] + 0.0144*PopulationEstimates['F_15_to_19sum'] - 0.0016*PopulationEstimates['F_20_to_24sum']
PopulationEstimates['Y_F_14'] = PopulationEstimates['F_10_to_14sum'] - PopulationEstimates['Y_F_10'] - PopulationEstimates['Y_F_11'] - PopulationEstimates['Y_F_12'] - PopulationEstimates['Y_F_13']
PopulationEstimates['Y_F_15'] = -0.0128*PopulationEstimates['F_5_to_9sum'] + 0.0848*PopulationEstimates['F_10_to_14sum'] + 0.1504*PopulationEstimates['F_15_to_19sum'] - 0.0240*PopulationEstimates['F_20_to_24sum'] + 0.0016*PopulationEstimates['F_25_to_29sum']
PopulationEstimates['Y_F_16'] = -0.0016*PopulationEstimates['F_5_to_9sum'] + 0.0144*PopulationEstimates['F_10_to_14sum'] + 0.2224*PopulationEstimates['F_15_to_19sum'] - 0.0416*PopulationEstimates['F_20_to_24sum'] + 0.0064*PopulationEstimates['F_25_to_29sum']
PopulationEstimates['Y_F_17'] = 0.0064*PopulationEstimates['F_5_to_9sum'] - 0.0336*PopulationEstimates['F_10_to_14sum'] + 0.2544*PopulationEstimates['F_15_to_19sum'] - 0.0336*PopulationEstimates['F_20_to_24sum'] + 0.0064*PopulationEstimates['F_25_to_29sum']
PopulationEstimates['Y_F_18'] = 0.0064*PopulationEstimates['F_5_to_9sum'] - 0.0416*PopulationEstimates['F_10_to_14sum'] + 0.2224*PopulationEstimates['F_15_to_19sum'] + 0.0144*PopulationEstimates['F_20_to_24sum'] - 0.0016*PopulationEstimates['F_25_to_29sum']
PopulationEstimates['Y_F_19'] = PopulationEstimates['F_15_to_19sum'] - PopulationEstimates['Y_F_15'] - PopulationEstimates['Y_F_16'] - PopulationEstimates['Y_F_17'] - PopulationEstimates['Y_F_18']
PopulationEstimates['Y_F_20'] = -0.0128*PopulationEstimates['F_10_to_14sum'] + 0.0848*PopulationEstimates['F_15_to_19sum'] + 0.1504*PopulationEstimates['F_20_to_24sum'] - 0.0240*PopulationEstimates['F_25_to_29sum'] + 0.0016*PopulationEstimates['F_30_to_34sum']
PopulationEstimates['Y_F_21'] = -0.0016*PopulationEstimates['F_10_to_14sum'] + 0.0144*PopulationEstimates['F_15_to_19sum'] + 0.2224*PopulationEstimates['F_20_to_24sum'] - 0.0416*PopulationEstimates['F_25_to_29sum'] + 0.0064*PopulationEstimates['F_30_to_34sum']
PopulationEstimates['Y_F_22'] = 0.0064*PopulationEstimates['F_10_to_14sum'] - 0.0336*PopulationEstimates['F_15_to_19sum'] + 0.2544*PopulationEstimates['F_20_to_24sum'] - 0.0336*PopulationEstimates['F_25_to_29sum'] + 0.0064*PopulationEstimates['F_30_to_34sum']
PopulationEstimates['Y_F_23'] = 0.0064*PopulationEstimates['F_10_to_14sum'] - 0.0416*PopulationEstimates['F_15_to_19sum'] + 0.2224*PopulationEstimates['F_20_to_24sum'] + 0.0144*PopulationEstimates['F_25_to_29sum'] - 0.0016*PopulationEstimates['F_30_to_34sum']
PopulationEstimates['Y_F_24'] = PopulationEstimates['F_20_to_24sum'] - PopulationEstimates['Y_F_20'] - PopulationEstimates['Y_F_21'] - PopulationEstimates['Y_F_22'] - PopulationEstimates['Y_F_23']
PopulationEstimates['Y_F_25'] = -0.0128*PopulationEstimates['F_15_to_19sum'] + 0.0848*PopulationEstimates['F_20_to_24sum'] + 0.1504*PopulationEstimates['F_25_to_29sum'] - 0.0240*PopulationEstimates['F_30_to_34sum'] + 0.0016*PopulationEstimates['F_35_to_39sum']
PopulationEstimates['Y_F_26'] = -0.0016*PopulationEstimates['F_15_to_19sum'] + 0.0144*PopulationEstimates['F_20_to_24sum'] + 0.2224*PopulationEstimates['F_25_to_29sum'] - 0.0416*PopulationEstimates['F_30_to_34sum'] + 0.0064*PopulationEstimates['F_35_to_39sum']
PopulationEstimates['Y_F_27'] = 0.0064*PopulationEstimates['F_15_to_19sum'] - 0.0336*PopulationEstimates['F_20_to_24sum'] + 0.2544*PopulationEstimates['F_25_to_29sum'] - 0.0336*PopulationEstimates['F_30_to_34sum'] + 0.0064*PopulationEstimates['F_35_to_39sum']
PopulationEstimates['Y_F_28'] = 0.0064*PopulationEstimates['F_15_to_19sum'] - 0.0416*PopulationEstimates['F_20_to_24sum'] + 0.2224*PopulationEstimates['F_25_to_29sum'] + 0.0144*PopulationEstimates['F_30_to_34sum'] - 0.0016*PopulationEstimates['F_35_to_39sum']
PopulationEstimates['Y_F_29'] = PopulationEstimates['F_25_to_29sum'] - PopulationEstimates['Y_F_25'] - PopulationEstimates['Y_F_26'] - PopulationEstimates['Y_F_27'] - PopulationEstimates['Y_F_28']


# Total

PopulationEstimates['Y_T_0'] = PopulationEstimates['Y_M_0'] + PopulationEstimates['Y_F_0']
PopulationEstimates['Y_T_1'] = PopulationEstimates['Y_M_1'] + PopulationEstimates['Y_F_1']
PopulationEstimates['Y_T_2'] = PopulationEstimates['Y_M_2'] + PopulationEstimates['Y_F_2']
PopulationEstimates['Y_T_3'] = PopulationEstimates['Y_M_3'] + PopulationEstimates['Y_F_3']
PopulationEstimates['Y_T_4'] = PopulationEstimates['Y_M_4'] + PopulationEstimates['Y_F_4']
PopulationEstimates['Y_T_5'] = PopulationEstimates['Y_M_5'] + PopulationEstimates['Y_F_5']
PopulationEstimates['Y_T_6'] = PopulationEstimates['Y_M_6'] + PopulationEstimates['Y_F_6']
PopulationEstimates['Y_T_7'] = PopulationEstimates['Y_M_7'] + PopulationEstimates['Y_F_7']
PopulationEstimates['Y_T_8'] = PopulationEstimates['Y_M_8'] + PopulationEstimates['Y_F_8']
PopulationEstimates['Y_T_9'] = PopulationEstimates['Y_M_9'] + PopulationEstimates['Y_F_9']
PopulationEstimates['Y_T_10'] = PopulationEstimates['Y_M_10'] + PopulationEstimates['Y_F_10']
PopulationEstimates['Y_T_11'] = PopulationEstimates['Y_M_11'] + PopulationEstimates['Y_F_11']
PopulationEstimates['Y_T_12'] = PopulationEstimates['Y_M_12'] + PopulationEstimates['Y_F_12']
PopulationEstimates['Y_T_13'] = PopulationEstimates['Y_M_13'] + PopulationEstimates['Y_F_13']
PopulationEstimates['Y_T_14'] = PopulationEstimates['Y_M_14'] + PopulationEstimates['Y_F_14']
PopulationEstimates['Y_T_15'] = PopulationEstimates['Y_M_15'] + PopulationEstimates['Y_F_15']
PopulationEstimates['Y_T_16'] = PopulationEstimates['Y_M_16'] + PopulationEstimates['Y_F_16']
PopulationEstimates['Y_T_17'] = PopulationEstimates['Y_M_17'] + PopulationEstimates['Y_F_17']
PopulationEstimates['Y_T_18'] = PopulationEstimates['Y_M_18'] + PopulationEstimates['Y_F_18']
PopulationEstimates['Y_T_19'] = PopulationEstimates['Y_M_19'] + PopulationEstimates['Y_F_19']
PopulationEstimates['Y_T_20'] = PopulationEstimates['Y_M_20'] + PopulationEstimates['Y_F_20']
PopulationEstimates['Y_T_21'] = PopulationEstimates['Y_M_21'] + PopulationEstimates['Y_F_21']
PopulationEstimates['Y_T_22'] = PopulationEstimates['Y_M_22'] + PopulationEstimates['Y_F_22']
PopulationEstimates['Y_T_23'] = PopulationEstimates['Y_M_23'] + PopulationEstimates['Y_F_23']
PopulationEstimates['Y_T_24'] = PopulationEstimates['Y_M_24'] + PopulationEstimates['Y_F_24']
PopulationEstimates['Y_T_25'] = PopulationEstimates['Y_M_25'] + PopulationEstimates['Y_F_25']
PopulationEstimates['Y_T_26'] = PopulationEstimates['Y_M_26'] + PopulationEstimates['Y_F_26']
PopulationEstimates['Y_T_27'] = PopulationEstimates['Y_M_27'] + PopulationEstimates['Y_F_27']
PopulationEstimates['Y_T_28'] = PopulationEstimates['Y_M_28'] + PopulationEstimates['Y_F_28']
PopulationEstimates['Y_T_29'] = PopulationEstimates['Y_M_29'] + PopulationEstimates['Y_F_29']

# We eliminate the old variables

OldVariables = ['F_0_to_1sum', 'F_0_to_4sum', 'F_1_to_4sum', 'F_5_to_9sum', 'F_10_to_14sum', 'F_15_to_19sum', 'F_20_to_24sum', 'F_25_to_29sum', 'F_30_to_34sum', 'F_35_to_39sum', 'M_0_to_1sum', 'M_0_to_4sum', 'M_1_to_4sum', 'M_5_to_9sum', 'M_10_to_14sum', 'M_15_to_19sum', 'M_20_to_24sum', 'M_25_to_29sum', 'M_30_to_34sum', 'M_35_to_39sum']

for Variable in OldVariables:
    del PopulationEstimates[Variable]

# Once the calculation is ready, we export the file, again as a CSV file, to be imported into QGIS and merged using the 'admin3Name' variable as key

PopulationEstimates.to_csv("Administrative boundaries - Level 4 - Treated.csv", encoding='utf-8', index=False, header=True)
