import os
import math
import pandas as pd

################
# Plz READ ME
# 자격과 건강검진 데이터를 모두 순환해야하기 때문에 데이터가 상당합니다.
# 연도를 나눠서 진행하기를 권장합니다.
# start_year 부터 end_year 까지 진행됨으로, 나눠서 진행을 원할경우 숫자를 변경하시면 됩니다.
################
start_year = 2002
end_year = 2013

result_col = [
	'SEX', 'AGE_GROUP', 'SIDO', 'SGG',
	'HEIGHT', 'WEIGHT',
	'HCHK_APOP_PMH_YN', 'HCHK_HDISE_PMH_YN', 'HCHK_HPRTS_PMH_YN', 'HCHK_DIABML_PMH_YN', 'HCHK_PHSS_PMH_YN', 'HCHK_ETCDSE_PMH_YN',  # 암 포함 기타질환
	'FMLY_APOP_PATIEN_YN', 'FMLY_HDISE_PATIEN_YN', 'FMLY_HPRTS_PATIEN_YN', 'FMLY_CANCER_PATIEN_YN',
	'SMK_STAT_TYPE_RSPS_CD', 'SMK_TERM_RSPS_CD', 'DSQTY_RSPS_CD',
	'DRNK_HABIT_RSPS_CD', 'TM1_DRKQTY_RSPS_CD',
	'EXERCI_FREQ_RSPS_CD'
]


def main():
	for y in range(start_year, end_year + 1):
		if 2002 <= y <= 2008:
			year_2002_2008(y)
		elif 2008 < y <= 2013:
			year_2009_2013(y)
		else:
			print('연도 범위를 넘었습니다. 연도를 재 정의해주세요.')


def get_value_T_str(value, correction_value=0, na_replace_zero=False):
	if not pd.isnull(value):
		if isinstance(value, bytes):
			return str(int(value.decode()) - correction_value)
		else:
			return str(int(value) - correction_value)
	elif na_replace_zero:
		return 0
	else:
		return value


# PMH = Personal Medical History
def set_PMH(result, PERSON_ID, ele):
	value = get_value_T_str(ele)
	if value == '1':
		result.at[PERSON_ID, 'HCHK_PHSS_PMH_YN'] = 1
	elif value == '4':
		reseult.at[PERSON_ID, 'HCHK_HPRTS_PMH_YN'] = 1
	elif value == '5':
		result.at[PERSON_ID, 'HCHK_HDISE_PMH_YN'] = 1
	elif value == '6':
		result.at[PERSON_ID, 'HCHK_APOP_PMH_YN'] = 1
	elif value == '7':
		result.at[PERSON_ID, 'HCHK_DIABML_PMH_YN'] = 1
	elif value == '8' or value == '9':
		result.at[PERSON_ID, 'HCHK_ETCDSE_PMH_YN'] = 1


def set_Term_SMK(result, PERSON_ID, value):
	if pd.isnull(value):
		return
	
	ele = 0
	if value == 0:
		ele = 0
	elif value < 5:
		ele = 1
	elif value < 10:
		ele = 2
	elif value < 20:
		ele = 3
	elif value < 30:
		ele = 4
	else:
		ele = 5
		
	if pd.isnull(result.at[PERSON_ID, 'SMK_TERM_RSPS_CD']):
		result.at[PERSON_ID, 'SMK_TERM_RSPS_CD'] = ele
	elif int(result.at[PERSON_ID, SMK_TERM_RSPS_CD]) < ele:
		result.at[PERSON_ID, 'SMK_TERM_RSPS_CD'] = ele


def set_Qty_SMK(result, value):
	if pd.isnull(value):
		return
	ele = 0
	if value == 0:
		ele = 0
	elif value < 10:
		ele = 1
	elif value < 20:
		ele = 2
	elif value < 40:
		ele = 3
	else:
		ele = 4
		
	if pd.isnull(result.at[PERSON_ID, 'DSQTY_RSPS_CD']):
		result.at[PERSON_ID, 'DSQTY_RSPS_CD'] = ele
	elif int(result.at[PERSON_ID, SMK_TERM_RSPS_CD]) < ele:
		result.at[PERSON_ID, 'DSQTY_RSPS_CD'] = ele


def get_HABIT_DRK(value):
	if pd.isnull(value):
		return value
	
	ele = get_value_T_str(value)
	if ele == 1:
		return 0
	elif ele == 2:
		return 1
	elif ele == 3:
		return 2
	elif ele == 4 or ele == 5:
		return 3
	else:
		return 4


def set_EXERCI_FREQ(result, PERSON_ID, value):
	if pd.isnull(value):
		return
	
	ele = get_value_T_str(value)
	ele_day = 0
	if ele == '1':
		ele_day = 0
	elif ele == '2' or ele == '3':
		ele_day = 1
	elif ele == '4' or ele == '5':
		ele_day = 2
	elif ele == '6' or ele == '7':
		ele_day = 3
	else:
		ele_day = 4
	
	if pd.isnull(result.at[PERSON_ID, 'EXERCI_FREQ_RSPS_CD']):
		result.at[PERSON_ID, 'EXERCI_FREQ_RSPS_CD'] = ele_day
	elif result.at[PERSON_ID, 'EXERCI_FREQ_RSPS_CD'] < ele_day:
		result.at[PERSON_ID, 'EXERCI_FREQ_RSPS_CD'] = ele_day


def year_2002_2008(y):
	year = str(y)
	
	df_jk = pd.read_sas('../../data/raw_helath/jk/nhid_jk_' + year + '.sas7bdat', index='PERSON_ID')
	df_gggj = pd.read_sas('../../data/raw_helath/gggj/nhid_gj_' + year + '.sas7bdat', index='PERSON_ID')
	result = pd.DataFrame(columns=result_col)
	result.index.name = 'PERSON_ID'
	
	jk_list = ['SEX', 'AGE_GROUP', 'SIDO', 'SGG']
	gggj_list = ['HEIGHT', 'WEIGHT',
	             'HCHK_PMH_CD1', 'HCHK_PMH_CD2', 'HCHK_PMH_CD3',
	             'FMLY_HPRTS_PATIEN_YN', 'FMLY_APOP_PATIEN_YN', 'FMLY_HDISE_PATIEN_YN', 'FMLY_CANCER_PATIEN_YN',
	             'SMK_STAT_TYPE_RSPS_CD', 'SMK_TERM_RSPS_CD', 'DSQTY_RSPS_CD',
	             'DRNK_HABIT_RSPS_CD', 'TM1_DRKQTY_RSPS_CD',
	             'EXERCI_FREQ_RSPS_CD']
	
	for col in df_jk.columns:
		if col not in jk_list:
			df_jk.drop(col, axis=1, inplace=True)
	
	for col in df_gggj.columns:
		if col not in gggj_list:
			df_gggj.drop(col, axis=1, inplace=True)
	
	for PERSON_ID in df_gggj.index:
		row_jk = df_jk.loc[PERSON_ID]
		
		for col in row_jk.index:  # row is Series
			result.at[PERSON_ID, col] = get_value_T_str(row_jk.at[col])
		##########################################################################
		row_gggj = df_gggj.loc[PERSON_ID]
		
		for col in row_gggj.index:  # row is Series
			if col == 'HEIGHT' or col == 'WEIGHT':
				result.at[PERSON_ID, col] = row_gggj.at[col]
			elif col == 'HCHK_PMH_CD1' or col == 'HCHK_PMH_CD1' or col == 'HCHK_PMH_CD1':
				set_PMH(result, PERSON_ID, row_gggj.at[col])
			elif col == 'FMLY_HPRTS_PATIEN_YN' or col == 'FMLY_APOP_PATIEN_YN' or col == 'FMLY_HDISE_PATIEN_YN' or col == 'FMLY_CANCER_PATIEN_YN':
				result.at[PERSON_ID, col] = get_value_T_str(row_gggj.at[col], -1)
			elif col == 'SMK_STAT_TYPE_RSPS_CD' or col == 'DRNK_HABIT_RSPS_CD' or col == 'EXERCI_FREQ_RSPS_CD':
				result.at[PERSON_ID, col] = get_value_T_str(row_gggj.at[col], -1)
			elif col == 'SMK_TERM_RSPS_CD' or col == 'DSQTY_RSPS_CD' or col == 'TM1_DRKQTY_RSPS_CD':
				result.at[PERSON_ID, col] = get_value_T_str(row_gggj.at[col])
		"""
			if col == 'HEIGHT' or col == 'WEIGHT':
				result.at[PERSON_ID, col] = row_gggj.at[col]
			elif col == 'HCHK_PMH_CD1' or col == 'HCHK_PMH_CD1' or col == 'HCHK_PMH_CD1':
				set_PMH(result, PERSON_ID, row_gggj.at[col])
			elif col == 'FMLY_HPRTS_PATIEN_YN' or col == 'FMLY_APOP_PATIEN_YN' or col == 'FMLY_HDISE_PATIEN_YN' or col == 'FMLY_CANCER_PATIEN_YN':
				result.at[PERSON_ID, col] = get_value_T_str(row_gggj.at[col], -1)
			elif col == 'SMK_STAT_TYPE_RSPS_CD':
				result.at[PERSON_ID, col] = get_value_T_str(row_gggj.at[col], -1)
			elif col == 'SMK_TERM_RSPS_CD' or col == 'DSQTY_RSPS_CD':
				result.at[PERSON_ID, col] = get_value_T_str(row_gggj.at[col])
			elif col == 'DRNK_HABIT_RSPS_CD':
				result.at[PERSON_ID, col] = get_value_T_str(row_gggj.at[col], -1)
			elif col == 'TM1_DRKQTY_RSPS_CD':
				result.at[PERSON_ID, col] = get_value_T_str(row_gggj.at[col])
			elif col == 'EXERCI_FREQ_RSPS_CD':
				result.at[PERSON_ID, col] = get_value_T_str(row_gggj.at[col], -1)
		"""
	result.fillna(0)
	os.makedirs('../../data/', exist_ok=True)
	os.makedirs('../../data/helath', exist_ok=True)
	os.makedirs('../../data/helath/jk+gggj', exist_ok=True)
	
	result.to_csv('../../data/helath/jk+gggj/' + year + 'jk+gggj.csv')
	print(year, 'JK+GGGJ IS DONE')


def year_2009_2013(y):
	year = str(y)
	
	df_jk = pd.read_sas('../../data/raw_helath/jk/nhid_jk_' + year + '.sas7bdat', index='PERSON_ID')
	df_gggj = pd.read_sas('../../data/raw_helath/gggj/nhid_gj_' + year + '.sas7bdat', index='PERSON_ID')
	result = pd.DataFrame(columns=result_col)
	result.index.name = 'PERSON_ID'
	
	jk_list = ['SEX', 'AGE_GROUP', 'SIDO', 'SGG']
	gggj_list = ['HEIGHT', 'WEIGHT',
	             'HCHK_APOP_PMH_YN', 'HCHK_HDISE_PMH_YN', 'HCHK_HPRTS_PMH_YN', 'HCHK_DIABML_PMH_YN', 'HCHK_PHSS_PMH_YN', 'HCHK_ETCDSE_PMH_YN',
	             'FMLY_HPRTS_PATIEN_YN', 'FMLY_APOP_PATIEN_YN', 'FMLY_HDISE_PATIEN_YN', 'FMLY_CANCER_PATIEN_YN',
	             'SMK_STAT_TYPE_RSPS_CD', 'PAST_SMK_TERM_RSPS_CD', 'PAST_DSQTY_RSPS_CD', 'CUR_SMK_TERM_RSPS_CD', 'CUR_DSQTY_RSPS_CD',
	             'DRNK_HABIT_RSPS_CD', 'TM1_DRKQTY_RSPS_CD',
	             'MOV20_WEK_FREQ_ID', 'MOV30_WEK_FREQ_ID', 'WLK30_WEK_FREQ_ID']
	
	for col in df_jk.columns:
		if col not in jk_list:
			df_jk.drop(col, axis=1, inplace=True)
	
	for col in df_gggj.columns:
		if col not in gggj_list:
			df_gggj.drop(col, axis=1, inplace=True)
	
	for PERSON_ID in df_gggj.index:
		row_jk = df_jk.loc[PERSON_ID]
		
		for col in row_jk.index:  # row is Series
			result.at[PERSON_ID, col] = get_value_T_str(row_jk.at[col])
		##########################################################################
		row_gggj = df_gggj.loc[PERSON_ID]
		
		for col in row_gggj.index:  # row is Series
			if col == 'HEIGHT' or col == 'WEIGHT':
				result.at[PERSON_ID, col] = row_gggj.at[col]
			elif col == 'HCHK_APOP_PMH_YN' or col == 'HCHK_HDISE_PMH_YN' or col == 'HCHK_HPRTS_PMH_YN' or col == 'HCHK_DIABML_PMH_YN' or col == 'HCHK_PHSS_PMH_YN' or col == 'HCHK_ETCDSE_PMH_YN':
				result.at[PERSON_ID, col] = get_value_T_str(row_gggj.at[col])
			elif col == 'FMLY_HPRTS_PATIEN_YN' or col == 'FMLY_APOP_PATIEN_YN' or col == 'FMLY_HDISE_PATIEN_YN' or col == 'FMLY_CANCER_PATIEN_YN':
				result.at[PERSON_ID, col] = get_value_T_str(row_gggj.at[col])
			elif col == 'SMK_STAT_TYPE_RSPS_CD':
				result.at[PERSON_ID, col] = get_value_T_str(row_gggj.at[col], -1)
			elif col == 'PAST_SMK_TERM_RSPS_CD' or col == 'CUR_SMK_TERM_RSPS_CD':
				set_Term_SMK(result, row_gggj.at[col])
			elif col == 'PAST_DSQTY_RSPS_CD' or col == 'CUR_DSQTY_RSPS_CD':
				set_Qty_SMK(result, row_gggj.at[col])
			elif col == 'DRNK_HABIT_RSPS_CD':
				result.at[PERSON_ID, col] = get_HABIT_DRK(row_gggj.at[col])
			elif col == 'TM1_DRKQTY_RSPS_CD':
				result.at[PERSON_ID, col] = math.ceil(int(get_value_T_str(row_gggj.at[col], na_replace_zero=True)) / 3.75)
			elif col == 'MOV20_WEK_FREQ_ID' or col == 'MOV30_WEK_FREQ_ID' or col == 'WLK30_WEK_FREQ_ID':
				set_EXERCI_FREQ(result, row_gggj.at[col])
				
	result.fillna(0)
	os.makedirs('../../data/', exist_ok=True)
	os.makedirs('../../data/helath', exist_ok=True)
	os.makedirs('../../data/helath/jk+gggj', exist_ok=True)
	
	result.to_csv('../../data/helath/jk+gggj/' + year + 'jk+gggj.csv')
	print(year, 'JK+GGGJ IS DONE')

main()