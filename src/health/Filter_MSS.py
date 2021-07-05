import pandas as pd
import os

# 연도의 데이터가 상당하므로 연도별로 따로 실행하는 것을 권장합니다.

for y in range(2002, 2013):
	year = str(y)
	df_sas = pd.read_sas('../../data/health/mss/nhid_gy20_t1_' + year + '.sas7bdat')
	
	drop_list = ['KEY_SEQ', 'YKIHO_ID', 'FORM_CD', 'IN_PAT_CORS_TYPE', 'OFFC_INJ_TYPE', 'RECN', 'VSCN', 'FST_IN_PAT_DT', 'DMD_TRAMT', 'DMD_SBRDN_AMT', 'DMD_JBRDN_AMT', \
	             'DMD_CT_TOT_AMT', 'DMD_MRI_TOT_AMT', 'EDEC_ADD_RT', 'EDEC_TRAMT', 'EDEC_SBRDN_AMT', 'EDEC_JBRDN_AMT', 'EDEC_CT_TOT_AMT', 'EDEC_MRI_TOT_AMT', \
	             'DMD_DRG_NO', 'TOT_PRES_DD_CNT', 'DSBJT_CD']
	# 용량 간소화를 위해 사용하지 않는 칼럼들 Drop
	
	for col in drop_list:
		if col in df_sas.columns:
			df_sas.drop([col], axis=1, inplace=True)
	
	sick_code_list = []
	sick_code_list.append('J45', 'J46')  # 천식
	sick_code_list.append('J30', 'L23', 'Z88')  # 알레르기 질환
	sick_code_list.append('J44')  # 만성폐쇄성질환
	sick_code_list.append('C')  # 종양(암)
	sick_code_list.append('E10', 'E11', 'E12', 'E13', 'E14', 'O24', 'R81')  # 당뇨
	sick_code_list.append('N11', 'N18')  # 만성신장질환
	sick_code_list.append('M00', 'M01', 'M03', 'M05', 'M06', 'M07', 'M08', 'M09', 'M13')  # 관절염
	sick_code_list.append('M80', 'M81', 'M82')  # 골다공증
	sick_code_list.append('G30', 'F00')  # 알츠하이머
	sick_code_list.append('H25', 'H26', 'H28')  # 백내장
	sick_code_list.append('G20', 'G21', 'G22')  # 파킨슨
	sick_code_list.append('I05', 'I06', 'I07', 'I08', 'I09', 'I20', 'I21', 'I22', 'I23', 'I24', 'I25', 'I27')  # 심장 질환
	
	result_df = pd.DataFrame(columns=df_sas.columns)
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
					if isinstance(result_df.at[result_index, col], bytes):
						result_df.at[result_index, col] = result_df.at[result_index, col].decode()
				result_index += 1
	
	os.makedirs('../../data/filter_mss', exist_ok=True)
	result_df.to_csv('../../data/filter_mss/' + year + 'mss.csv', index=False)
	print(year + ' IS DONE!')
