import pandas as pd
import os

for y in range(2002, 2013):
	year = str(y)
	df_sas = pd.read_sas('../../data/health/mss/nhid_gy20_t1_' + year + '.sas7bdat')
	
	drop_list = ['KEY_SEQ', 'YKIHO_ID', 'FORM_CD', 'IN_PAT_CORS_TYPE', 'OFFC_INJ_TYPE', 'RECN', 'VSCN', 'FST_IN_PAT_DT', 'DMD_TRAMT', 'DMD_SBRDN_AMT', 'DMD_JBRDN_AMT', \
	             'DMD_CT_TOT_AMT', 'DMD_MRI_TOT_AMT', 'EDEC_ADD_RT', 'EDEC_TRAMT', 'EDEC_SBRDN_AMT', 'EDEC_JBRDN_AMT', 'EDEC_CT_TOT_AMT', 'EDEC_MRI_TOT_AMT', \
	             'DMD_DRG_NO', 'TOT_PRES_DD_CNT', 'DSBJT_CD']
	
	for col in drop_list:
		if col in df_sas.columns:
			df_sas.drop([col], axis=1, inplace=True)
	
	result_df = pd.DataFrame(columns=df_sas.columns)
	
	sick_code_list = ['J45', 'J46', \
	                  'J30','L23', 'Z88',\
	                  'J44', \
	                  'C', \
	                  'E10', 'E11', 'E12', 'E13', 'E14', 'O24', 'R81', \
	                  'N11', 'N18', \
	                  'M00', 'M01', 'M03', 'M05', 'M06', 'M07', 'M08', 'M09', 'M13', \
	                  'M80', 'M81', 'M82', \
	                  'G30', 'F00', \
	                  'H25', 'H26', 'H28', \
	                  'G20', 'G21', 'G22', \
	                  'I05', 'I06', 'I07', 'I08', 'I09', 'I20', 'I21', 'I22', 'I23', 'I24', 'I25', 'I27']
	
	result_index = 0
	for i in df_sas.index:
		row_mss = df_sas.iloc[i]
		main_sick = ''
		if isinstance(row_mss.at['MAIN_SICK'], bytes):
			main_sick = row_mss.at['MAIN_SICK'].decode()
		
		sub_sick = ''
		if isinstance(row_mss.at['SUB_SICK'], bytes):
			sub_sick = row_mss.at['SUB_SICK'].decode()
		
		for sick_code in sick_code_list:
			if sick_code in main_sick or sick_code in sub_sick:
				result_df.loc[result_index] = row_mss
				for col in result_df.columns:
					if isinstance(result_df.at[result_index, col], bytes)
						result_df.at[result_index, col] = result_df.at[result_index, col].decode()
				result_index += 1
	
	os.makedirs('../../data/filter_mss', exist_ok=True)
	result_df.to_csv('../../data/filter_mss/mss' + year + '.csv', index=False)
	print(year + ' IS DONE!')
