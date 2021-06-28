import pandas as pd
import numpy as np
import googlemaps
import os
# Plz input your Google geocode API
# 사용자의 구글 지오코드 API 키 값이 환경변수로 저장되어 있어야합니다.

geo_api = os.environ['GEOCODE_API']
map = googlemaps.Client(key=geo_api)


def get_processed_data(year, quat):
	data_name = './../../data/dust/' + str(year) + '년0' + str(quat) + '분기.xlsx'
	data_excel = pd.read_excel(data_name)
	# data_excel = 측정소에서 얻어온 결과값 엑셀
	
	data_excel.drop(['지역', '측정소명', 'SO2', 'CO', 'O3', 'NO2'], axis=1, inplace=True)
	if 'PM25' in data_excel.columns:
		data_excel.drop(['PM25'], axis=1, inplace=True)
	# 필요 없는 데이터값 제거
	
	result_excel = pd.DataFrame(columns=['lat', 'lon'])
	ms_code = None # Measure Station Code
	date = None
	sum_pm = 0
	count = 0
	
	for index in data_excel.index:
		row = data_excel.loc[index]
		
		# 측정일시가 달라지면 새로운 열 생
		if date != str(row.at['측정일시'])[:8]:
			input_dust_day_data(result_excel, ms_code, sum_pm, count)
			sum_pm = 0
			count = 0

			date = str(row['측정일시'])[:8]
			
			
		# 측정소코드(측정소 장소)가 달라지면 새로운 열 생성
		if ms_code != row.at['측정소코드']:
			input_dust_day_data(result_excel, ms_code, sum_pm, count)
			sum_pm = 0
			count = 0
			
			ms_code = row.at['측정소코드']
			lat_A_lon = get_lat_AND_lon(row.at['주소'])
			result_excel.at[ms_code, 'lat'] = round(lat_A_lon[0], 2)
			result_excel.at[ms_code, 'lon'] = round(lat_A_lon[1], 2)
		
		# 측정일시 혹은 측정소코드가 달라지지 않으면 PM10의 총합 계산
		if pd.notnull(row.at['PM10']):
			sum_pm += row.at['PM10']
			count += 1
			
	return result_excel

def make_data(dust_year_data, year):
	sido_sgg_df = pd.read_excel('./../../data/sido_sgg.xlsx')
	
	result_excel = pd.DataFrame(columns=['lat', 'lon'])
	
	for index in sido_sgg_df.index:
		row = sido_sgg_df.loc[index]
		lat_A_lon = get_lat_AND_lon(row.at['address'])
		index_name = row.at['sido_code'] + '_' + row.at['sgg_code']
		
		result_excel.at[index_name, 'lat'] = round(2, lat_A_lon[0])
		result_excel.at[index_name, 'lon'] = round(2, lat_A_lon[1])
	
	for date in dust_year_data.columns:
		# processed_excel 에서 열 = 날짜 하지만 첫 두 열은 lat과 lon 이므로 제외
		if date == 'lat' or date == 'lon':
			continue
			
		data_lat = dust_year_data['lat'].tolist()
		data_lon = dust_year_data['lon'].tolist()
		data_dust = dust_year_data[date].tolist()
		
		# 측정소에서 운영을 하지 않았던 날도 있으므로 운영을 하지 않은 측정소는 열외
		for i, e in enumerate(data_dust):
			if np.isnan(e):
				data_dust.pop(i)
				data_lat.pop(i)
				data_lon.pop(i)
		
		func_result = idwr(x=data_lat, y=data_lon, z=data_dust, xi=result_excel['lat'].tolist(), yi=result_excel['lon'].tolist())
		func_df = pd.DataFrame(func_result, columns=['lat', 'lon', date])  # 함수의 결과값이 이중리스트이므로 데이터프레임화 해서 date 열만 사용
		result_excel[date] = func_df[date]
	
	os.makedirs('./../../data/dust', exist_ok=True)
	result_excel.to_csv('./../../data/dust/dust' + year + '.csv')
	
def main():
	for y in range(2002, 2014):
		year_data = None
		year = str(y)
		for q in range(1, 5):
			quat = str(q)
			dust_day_data = get_processed_data(year, quat)
			
			if year_data is None:
				year_data = pd.DataFrame(columns=quat_data.columns)
				year_data.index.name = ms_code
			
			dust_data_quat_to_year(year_data, quat_data)
			
		make_data(year_data, year)

def input_dust_day_data(df, ms_code, date, sum_pm, count):
	if count == 0 or ms_code is None:
		return False
	else:
		df.at[ms_code, date] = int(sum_pm / count)
		return True
	
def get_lat_AND_lon(address):
	geometry = map.geocode(address)[0]['geometry']['location']
	lat = round(geometry['lat'], 2)
	lon = round(geometry['lon'], 2)
	return lat, lon

def dust_data_quat_to_year(year_data, quat_data):
	if len(year_data.index) != len(quat_data.index):
		print('dust_data_quat_to_year -> FAILED')
		return False
	
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
			lstdist.append(d)
		sumsup = list((1 / np.power(lstdist, 2)))
		suminf = np.sum(sumsup)
		sumsup = np.sum(np.array(sumsup) * np.array(z))
		u = sumsup / suminf
		u = round(u, 2)
		xyzi = [xi[p], yi[p], u]
		lstxyzi.append(xyzi)
	return lstxyzi