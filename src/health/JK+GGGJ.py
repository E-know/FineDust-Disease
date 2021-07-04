import os

import pandas as pd
################
# Plz READ ME
# 자격과 건강검진 데이터를 모두 순환해야하기 때문에 데이터가 상당합니다.
# 연도를 나눠서 진행하기를 권장합니다.
# start_year 부터 end_year 까지 진행됨으로, 나눠서 진행을 원할경우 숫자를 변경하시면 됩니다.
################
start_year = 2002
end_year = 2013

for y in range(start_year, end_year + 1):
	year = str(y)
	
	col_list = ['SEX', 'AGE_GROUP', 'SIDO', 'SGG', 'HEIGHT', 'WEIGHT', 'HCHK_PMH_CD1', 'HCHK_PMH_CD2', 'HCHK_PMH_CD3', 'FMLY_LIVER_DISE_PATIEN_YN', 'FMLY_APOP_PATIEN_YN', 'FMLY_HDISE_PATIEN_YN', 'FMLY_CANCER_PATIEN_YN', 'SMK_STAT_TYPE_RSPS_CD', 'SMK_TERM_RSPS_CD', 'DSQTY_RSPS_CD',
	            'DRNK_HABIT_RSPS_CD',
	            'EXERCI_FREQ_RSPS_CD']
	
	df_jk = pd.read_sas('../../data/raw_helath/jk/nhid_jk_' + year + '.sas7bdat', index='PERSON_ID')
	
	# 건강-자격 데이터에서 필요 없는 데이터 삭제
	for col in df_jk.columns:
		if col not in col_list:
			df_jk.drop([col], axis=1, inplace=True)
			
	df_gggj = pd.read_sas('../../data/raw_helath/gggj/nhid_gj_' + year + '.sas7bdat', index='PERSON_ID')
	
	# 건강-건강검진 데이터에서 필요 없는 데이터 삭제
	for col in df_gggj.columns:
		if col not in col_list:
			df_gggj.drop([col], axis=1, inplace=True)
	
	result = pd.DataFrame(columns=list(df_jk.columns) + list(df_gggj.columns) + ['A_DATE', 'B_DATE', 'C_DATE', 'D_DATE', 'E_DATE', 'F_DATE', 'G_DATE', 'H_DATE', 'I_DATE', 'J_DATE', 'K_DATE', 'L_DATE', 'M_DATE'])
	result.index.name = 'PERSON_ID'
	"""
	A_Date 천식
	B_DATE 알레르기 질환
	C_DATE 만성폐쇄성폐질환
	D_DATE --[삭제]--
	E_DATE 종양(암)
	F_DATE 당뇨
	G_DATE 만성신장질환
	H_DATE 관절염
	I_DATE 골다공증
	J_DATE 알츠하이머
	K_DATE 백내장
	L_DATE 파킨슨
	M_DATE 심장질환
	"""
	
	for PERSON_ID in df_gggj.index:
		row_jk = df_jk.loc[PERSON_ID]
		row_gggj = df_gggj.loc[PERSON_ID]
		
		for index in row_jk.index:
			if isinstance(row_jk.at[index], bytes):
				result.at[PERSON_ID, index] = row_jk.at[index].decode()
			else:
				result.at[PERSON_ID, index] = row_jk.at[index]
		
		for index in row_gggj.index:
			if isinstance(row_gggj.at[index], bytes):
				result.at[PERSON_ID, index] = row_gggj.at[index].decode()
			else:
				result.at[PERSON_ID, index] = row_gggj.at[index]
	
	os.makedirs('../../data/', exist_ok=True)
	os.makedirs('../../data/helath', exist_ok=True)
	os.makedirs('../../data/helath/jk+gggj', exist_ok=True)
	
	result.to_csv('../../data/helath/jk+gggj/' + year + 'jk+gggj.csv')
	print(year, 'JK+GGGJ IS DONE')