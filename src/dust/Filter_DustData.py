import pandas as pd
import numpy as np
import os
import math

start_year = 2002  # Plz Input Start Year
end_year = 2013  # Plz Input End Year

def get_sido_sgg_code():
	answer = {}
	
	sido_sgg = pd.read_csv('../../data/raw_dust/sido_sgg_code.csv')
	
	for index in sido_sgg.index:
		row = sido_sgg.loc[index]
		sido = str(row.at['SIDO_CODE'])
		sgg = str(row.at['SGG_CODE'])
		lat = row.at['lat']
		lon = row.at['lon']
		dict = {'lat': lat, 'lon': lon}
		answer.update({sido + '_' + sgg: dict})
	return answer


def get_processed_data(year, quat):
	data_name = './../../data/raw_dust/' + str(year) + '년0' + str(quat) + '분기.xlsx'
	data_excel = pd.read_excel(data_name)
	# data_excel = 측정소에서 얻어온 결과값 엑셀
	
	data_excel.drop(['지역', '측정소명', 'SO2', 'CO', 'O3', 'NO2'], axis=1, inplace=True)
	if 'PM25' in data_excel.columns:
		data_excel.drop(['PM25'], axis=1, inplace=True)
	# 필요 없는 데이터값 제거
	
	result_excel = pd.DataFrame(columns=['lat', 'lon'])
	ms_code = None  # Measure Station Code
	date = None
	sum_pm = 0
	count = 0
	
	ms_info = pd.read_excel('./../../data/MS_Info.xlsx', index_col='MS_CODE')
	
	for index in data_excel.index:
		row = data_excel.loc[index]
		# 측정일시가 달라지면 새로운 열 생
		if date != str(row.at['측정일시'])[:8]:
			input_dust_day_data(result_excel, ms_code, date, sum_pm, count)
			sum_pm = 0
			count = 0
			
			date = str(row['측정일시'])[:8]
		
		# 측정소코드(측정소 장소)가 달라지면 새로운 열 생성
		if ms_code != row.at['측정소코드']:
			input_dust_day_data(result_excel, ms_code, date, sum_pm, count)
			sum_pm = 0
			count = 0
			ms_code = row.at['측정소코드']
			result_excel.at[ms_code, 'lat'] = ms_info.at[ms_code, 'LAT']
			result_excel.at[ms_code, 'lon'] = ms_info.at[ms_code, 'LON']
		
		# 측정일시 혹은 측정소코드가 달라지지 않으면 PM10의 총합 계산
		if pd.notnull(row.at['PM10']) and row.at['PM10'] != -999:
			sum_pm += row.at['PM10']
			count += 1
	
	return result_excel


def make_data(dust_year_data, sido_sgg_dict, year):
	result_excel = pd.DataFrame(columns=['lat', 'lon'])
	
	ms_info = pd.read_excel('./../../data/MS_Info.xlsx', index_col='MS_CODE')
	
	for sido_sgg in sido_sgg_dict.keys():
		result_excel.at[sido_sgg, 'lat'] = sido_sgg_dict[sido_sgg]['lat']
		result_excel.at[sido_sgg, 'lon'] = sido_sgg_dict[sido_sgg]['lon']
	
	for ms_code in dust_year_data.index:
		dust_year_data.at[ms_code, 'lat'] = ms_info.at[ms_code, 'LAT']
		dust_year_data.at[ms_code, 'lon'] = ms_info.at[ms_code, 'LON']
	
	for date in dust_year_data.columns:
		# processed_excel 에서 열 = 날짜 하지만 첫 두 열은 lat과 lon 이므로 제외
		if date == 'lat' or date == 'lon':
			continue
		
		input_data = pd.DataFrame()
		input_data['lat'] = dust_year_data['lat']
		input_data['lon'] = dust_year_data['lon']
		input_data[date] = dust_year_data[date]
		input_data.dropna(inplace=True)
		
		func_result = idwr(x=input_data['lat'].tolist(), y=input_data['lon'].tolist(), z=input_data[date].tolist(), xi=result_excel['lat'].tolist(), yi=result_excel['lon'].tolist())
		func_df = pd.DataFrame(func_result, columns=['lat', 'lon', date])  # 함수의 결과값이 이중리스트이므로 데이터프레임화 해서 date 열만 사용
		dust_list = func_df[date].tolist()
		dust_index = 0
		for index in result_excel.index:
			result_excel.at[index, date] = dust_list[dust_index]
			dust_index += 1
		
	temp = dust_year_data.drop(['lat', 'lon'], axis=1)
	for index in dust_year_data.index:
		dust_year_data.at[index, 'AVE'] = temp.loc[index].mean()
		
	
	os.makedirs('../../data/dust', exist_ok=True)
	result_excel.to_csv('../../data/dust/' + year + 'dust.csv')


def main():
	sido_sgg_dict = get_sido_sgg_code()
	for y in range(start_year, end_year + 1):
		year_data = None
		year = str(y)
		for q in range(1, 5):
			quat = str(q)
			quat_dust_day_data = get_processed_data(year, quat)
			
			if year_data is None:
				year_data = pd.DataFrame(columns=quat_dust_day_data.columns)
				year_data.index.name = 'MS_CODE'
			
			dust_data_quat_to_year(year_data, quat_dust_day_data)
		make_data(year_data, sido_sgg_dict, year)


def input_dust_day_data(df, ms_code, date, sum_pm, count):
	if count == 0 or ms_code is None:
		return False
	else:
		df.at[ms_code, date] = int(sum_pm / count)
		return True


def dust_data_quat_to_year(year_data, quat_data):
	for col in quat_data:
		if col == 'lat' or col == 'lon':
			continue
		else:
			year_data[col] = quat_data[col]
	return True


# ------------------------------------------------------------
# Distance calculation, degree to km (Haversine method)
def harvesine(lon1, lat1, lon2, lat2):
	rad = math.pi / 180  # degree to radian
	R = 6378.1  # earth average radius at equador (km)
	dlon = (lon2 - lon1) * rad
	dlat = (lat2 - lat1) * rad
	a = (math.sin(dlat / 2)) ** 2 + math.cos(lat1 * rad) * \
	    math.cos(lat2 * rad) * (math.sin(dlon / 2)) ** 2
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
	d = R * c
	return d


# ------------------------------------------------------------
# Prediction
def idwr(x, y, z, xi, yi):
	lstxyzi = []
	for p in range(len(xi)):
		lstdist = []
		for s in range(len(x)):
			d = (harvesine(x[s], y[s], xi[p], yi[p]))
			if d == 0:
				d = 0.00000000000000001
			lstdist.append(d)
			
		
		sumsup = list((1 / np.power(lstdist, 2)))
		suminf = np.sum(sumsup)
		sumsup = np.sum(np.array(sumsup) * np.array(z))
		u = sumsup / suminf
		u = round(u, 2)
		xyzi = [xi[p], yi[p], u]
		lstxyzi.append(xyzi)
	return lstxyzi
