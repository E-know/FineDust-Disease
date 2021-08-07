import os.path

import numpy as np
import pandas as pd

A_sick_code = ['J45', 'J46']
B_sick_code = ['J30', 'L23']
C_sick_code = ['J44']
D_sick_code = ['D59']
E_sick_code = ['C']
F_sick_code = ['E10', 'E11', 'E12', 'E13', 'E14', 'O24', 'R81']
G_sick_code = ['N11', 'N18']
H_sick_code = ['M00', 'M01', 'M03', 'M05', 'M06', 'M07', 'M08', 'M09', 'M13']
I_sick_code = ['M80', 'M81', 'M82']
J_sick_code = ['G30', 'F00']
K_sick_code = ['H25', 'H26', 'H28']
L_sick_code = ['G20', 'G21', 'G22']
M_sick_code = ['I05', 'I06', 'I07', 'I08', 'I09', 'I20', 'I21', 'I22', 'I23', 'I24', 'I25', 'I27']
sick_code_list = [A_sick_code, B_sick_code, C_sick_code, D_sick_code, E_sick_code, F_sick_code, G_sick_code, H_sick_code, I_sick_code, J_sick_code, K_sick_code, L_sick_code, M_sick_code]
ALP = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']

start_year = 2002
end_year = 2002


def main():
	for y in range(start_year, end_year + 1):
		year = str(y)
		
		result = pd.read_csv('../../data/health/jk+gggj/' + year + 'jk+gggj.csv', index_col='PERSON_ID')
		for alp in ALP:
			result[alp + '_DATE'] = pd.Series()
		
		df_mss = pd.read_csv('../../data/health/filter_mss/' + year + 'mss.csv')
		
		result_index = list(result.index)
		print('START')
		for index in df_mss.index:
			# 잘못 적힌 데이터 Skip
			if df_mss.at[index, 'RECU_FR_DT'] < 10000:
				continue
			
			PERSON_ID = df_mss.at[index, 'PERSON_ID']
			
			if PERSON_ID in result_index:
				row_mss = df_mss.iloc[index]
				main_sick = row_mss.at['MAIN_SICK']
				sub_sick = row_mss.at['SUB_SICK']
				
				if isinstance(main_sick, str):
					main_sick = main_sick[:3]
					if main_sick[0] == 'C':
						main_sick = 'C'
				
				if isinstance(sub_sick, str):
					sub_sick = sub_sick[:3]
					if sub_sick[0] == 'C':
						sub_sick = 'C'
				
				for i in range(len(sick_code_list)):
					if main_sick in sick_code_list[i] or sub_sick in sick_code_list[i]:
						set_Date(result, PERSON_ID, ALP[i] + '_DATE', str(row_mss.at['RECU_FR_DT']))
		
		os.makedirs('../../data/model', exist_ok=True)
		result.to_csv('../../data/model/' + year + 'model.csv')
		print(year, ' IS END')
		
		# TODO ERASE
		if os.path.isfile('temp.csv'):
			os.remove('temp.csv')

def set_Date(result, PERSON_ID, X_DATE, date):
	if pd.isnull(result.at[PERSON_ID, X_DATE]):
		result.at[PERSON_ID, X_DATE] = date
	elif int(date) < int(result.at[PERSON_ID, X_DATE]):
		result.at[PERSON_ID, X_DATE] = date


def convert_date_TO_dust(result, year):
	dust = pd.read_csv('../../data/dust/' + year + 'dust.csv', index_col='SIDO_SGG')
	
	for PERSON_ID in result.index:
		for alp in ALP:
			sido = str(result.at[PERSON_ID, 'SIDO'])
			sgg = str(result.at[PERSON_ID, 'SGG'])
			if not pd.isnull(result.at[PERSON_ID, alp + '_DATE']):
				result.at[PERSON_ID, alp + '_DATE'] = dust.at[sido + '_' + sgg, str(int(result.at[PERSON_ID, alp + '_DATE']))]
			

main()
