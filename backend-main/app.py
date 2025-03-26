import os
import json
import pandas as pd
from flask import Flask, flash, request, redirect, url_for, render_template, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from geopy.geocoders import Nominatim
from haversine import haversine
import re
import uuid
from datetime import datetime, timedelta
import ast

app = Flask(__name__)
CORS(app)
geolocator = Nominatim(user_agent="my_geocoder")
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'json'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def open_json_with_key(key):
    file_path = os.path.join(UPLOAD_FOLDER, key)
    try:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None

def is_json_file(filename):
    return filename.lower().endswith(".json")

def date_filtering(x):
    x_modified = x.replace('T', ' ')
    x_modified = x_modified.rsplit(':', 1)[0]
    return x_modified

def activity_and_stay(af):
    data_list = []
    timeline_objects = af['timelineObjects']

    for data in timeline_objects:
        if data.get('activitySegment', {}).get('activityType'):
            activity_segment = data.get('activitySegment', {})
            activity_type = activity_segment.get('activityType')
        
            if activity_type:
                start_location = activity_segment.get('startLocation', {})
                end_location = activity_segment.get('endLocation', {})
                duration = activity_segment.get('duration', {})
        
                start_latitude = start_location.get('latitudeE7', 0) / 1e7
                start_longitude = start_location.get('longitudeE7', 0) / 1e7
        
                end_latitude = end_location.get('latitudeE7', 0) / 1e7
                end_longitude = end_location.get('longitudeE7', 0) / 1e7
        
                start_timestamp = duration.get('startTimestamp', '')
                end_timestamp = duration.get('endTimestamp', '')
        
                filtering_start_time = date_filtering(start_timestamp)
                filtering_end_time = date_filtering(end_timestamp)
                
                segment_data = {
                    'Activity Type': activity_type,
                    '시작 시간': filtering_start_time,
                    '종료 시간': filtering_end_time,
                    '시작 위치(위도)': start_latitude,
                    '시작 위치(경도)': start_longitude,
                    '종료 위치(위도)': end_latitude,
                    '종료 위치(경도)': end_longitude
                }
            data_list.append(segment_data)
            
        elif data.get('placeVisit', {}).get('placeVisitType'):
            stay_segment = data.get('placeVisit', {})
            stay_type = stay_segment.get('placeVisitType')

            if stay_type:
                start_location = stay_segment.get('location', {})
                end_location = stay_segment.get('location', {})
                duration = stay_segment.get('duration', {})
        
                start_latitude = start_location.get('latitudeE7', 0) / 1e7
                start_longitude = start_location.get('longitudeE7', 0) / 1e7

                end_latitude = end_location.get('latitudeE7', 0) / 1e7
                end_longitude = end_location.get('longitudeE7', 0) / 1e7
        
                start_timestamp = duration.get('startTimestamp', '')
                end_timestamp = duration.get('endTimestamp', '')
        
                filtering_start_time = date_filtering(start_timestamp)
                filtering_end_time = date_filtering(end_timestamp)

                segment_data = {
                    'Activity Type': stay_type,
                    '시작 시간': filtering_start_time,
                    '종료 시간': filtering_end_time,
                    '시작 위치(위도)': start_latitude,
                    '시작 위치(경도)': start_longitude,
                    '종료 위치(위도)': end_latitude,
                    '종료 위치(경도)': end_longitude
                }
            data_list.append(segment_data)
            
    return data_list


def make_meeting_points(df1, df2) :
    matches = []
    
    for idx1, row1 in df1.iterrows():
        for idx2, row2 in df2.iterrows():
            if (row1['시작 시간'] <= row2['시작 시간'] and row1['종료 시간'] >= row2['시작 시간']) or (row1['시작 시간'] <= row2['종료 시간'] and row1['종료 시간'] >= row2['종료 시간']):
                start_distance = haversine((row1['시작 위치(위도)'], row1['시작 위치(경도)']), (row2['시작 위치(위도)'], row2['시작 위치(경도)']), unit='m')
                end_distance = haversine((row1['종료 위치(위도)'], row1['종료 위치(경도)']), (row2['종료 위치(위도)'], row2['종료 위치(경도)']), unit='m')
                if start_distance <= 20 or end_distance <= 20:
                    start_time = max(row1['시작 시간'], row2['시작 시간'])
                    end_time = min(row1['종료 시간'], row2['종료 시간'])
                    new_match = f"{start_time} ~ {end_time} 시간에 {row1['시작 위치(위도)']}, {row1['시작 위치(경도)']} 위치에서 만났을 수 있다"
                    if new_match not in matches:
                        matches.append(new_match)
    
    return matches

def make_meeting_points_only_time(df1, df2) :
    matches = []
    
    for idx1, row1 in df1.iterrows():
        for idx2, row2 in df2.iterrows():
            if (row1['시작 시간'] <= row2['시작 시간'] and row1['종료 시간'] >= row2['시작 시간']) or (row1['시작 시간'] <= row2['종료 시간'] and row1['종료 시간'] >= row2['종료 시간']):
                start_distance = haversine((row1['시작 위치(위도)'], row1['시작 위치(경도)']), (row2['시작 위치(위도)'], row2['시작 위치(경도)']), unit='m')
                end_distance = haversine((row1['종료 위치(위도)'], row1['종료 위치(경도)']), (row2['종료 위치(위도)'], row2['종료 위치(경도)']), unit='m')
                if start_distance <= 20 or end_distance <= 20:
                    start_time = max(row1['시작 시간'], row2['시작 시간'])
                    end_time = min(row1['종료 시간'], row2['종료 시간'])
                    new_match = f"{start_time} ~ {end_time}"
                    if new_match not in matches:
                        matches.append(new_match)
    
    return matches

def data_to_math(data_list) :
    result_list = []
    
    for item in data_list:
        match = re.search(r'(\d+\.\d+), (\d+\.\d+)', item)
        if match:
            latitude, longitude = map(float, match.groups())
            result_list.append({'latitude': latitude, 'longitude': longitude})

    json_list = json.dumps(result_list)
    
    return json_list

def adjust_time_range(input_time_range):
    start_time_str, end_time_str = input_time_range.split(' ~ ')
    
    start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M')
    end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M')
    
    adjusted_start_time = start_time - timedelta(hours=1)
    adjusted_end_time = end_time + timedelta(hours=1)
    
    adjusted_start_time_str = adjusted_start_time.strftime('%Y-%m-%d %H:%M')
    adjusted_end_time_str = adjusted_end_time.strftime('%Y-%m-%d %H:%M')
    
    adjusted_time_range = f"{adjusted_start_time_str} ~ {adjusted_end_time_str}"
    return adjusted_time_range

def find_rows2(df, time_range_str):
    result = []

    time_range_str = adjust_time_range(time_range_str)
    start_time_str, end_time_str = time_range_str.split(' ~ ')
    
    start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M')
    end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M')
    
    for index, row in df.iterrows():
        activity_start_time = datetime.strptime(row['시작 시간'], '%Y-%m-%d %H:%M')
        activity_end_time = datetime.strptime(row['종료 시간'], '%Y-%m-%d %H:%M')
        
        if (activity_start_time >= start_time and activity_start_time <= end_time) or \
           (activity_end_time >= start_time and activity_end_time <= end_time) or \
           (activity_start_time <= start_time and activity_end_time >= end_time):
            result.append(row)
    
    return result


def find_rows(df, time_range_str):
    result = []

    time_range_str = adjust_time_range(time_range_str)
    start_time_str, end_time_str = time_range_str.split(' ~ ')
    
    start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M')
    end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M')
    
    for index, row in df.iterrows():
        activity_start_time = datetime.strptime(row['시작 시간'], '%Y-%m-%d %H:%M')
        activity_end_time = datetime.strptime(row['종료 시간'], '%Y-%m-%d %H:%M')
        
        if (start_time >= activity_start_time and start_time <= activity_end_time) or \
           (end_time >= activity_start_time and end_time <= activity_end_time):
            result.append(row)
    
    return result

def generate_location_info(data, input_time_range):
    coordinates_info = []

    if len(data) == 1:
        coordinates_info.append({
            "start_lat": data[0]['시작 위치(위도)'],
            "start_lng": data[0]['시작 위치(경도)'],
            "end_lat": data[0]['종료 위치(위도)'],
            "end_lng": data[0]['종료 위치(경도)'],
        })
    
    elif len(data) == 2:
        first_info = {
            "start_lat": data[0]['시작 위치(위도)'],
            "start_lng": data[0]['시작 위치(경도)'],
            "end_lat": data[0]['종료 위치(위도)'],
            "end_lng": data[0]['종료 위치(경도)'],
        }

        second_info = {
            "start_lat": data[1]['시작 위치(위도)'],
            "start_lng": data[1]['시작 위치(경도)'],
            "end_lat": data[1]['종료 위치(위도)'],
            "end_lng": data[1]['종료 위치(경도)'],
        }

        coordinates_info.extend([first_info, second_info])

    return coordinates_info

def generate_location_info2(data, input_time_range):
    if len(data) == 1:
        coordinates_info = f"'{data[0]['시작 위치(위도)']} {data[0]['시작 위치(경도)']}' '{data[0]['종료 위치(위도)']} {data[0]['종료 위치(경도)']}'"
    
    elif len(data) == 2:
        first_start = f"'{data[0]['시작 위치(위도)']}, {data[0]['시작 위치(경도)']}'"
        first_end = f"'{data[0]['종료 위치(위도)']}, {data[0]['종료 위치(경도)']}'"

        second_start = f"'{data[1]['시작 위치(위도)']}, {data[1]['시작 위치(경도)']}',"
        second_end = f"'{data[1]['종료 위치(위도)']}, {data[1]['종료 위치(경도)']}'"

        coordinates_info = f"{first_start} {first_end} {second_start} {second_end}"

    return coordinates_info




def generate_location_info3(data, input_time_range):
    coordinates_info = []

    if len(data) == 1:
        coordinates_info.append({
            "start_lat": data[0]['시작 위치(위도)'],
            "start_lng": data[0]['시작 위치(경도)'],
            "end_lat": data[0]['종료 위치(위도)'],
            "end_lng": data[0]['종료 위치(경도)'],
        })
    
    elif len(data) == 2:
        first_info = {
            "start_lat": data[0]['시작 위치(위도)'],
            "start_lng": data[0]['시작 위치(경도)'],
            "end_lat": data[0]['종료 위치(위도)'],
            "end_lng": data[0]['종료 위치(경도)'],
        }

        second_info = {
            "start_lat": data[1]['시작 위치(위도)'],
            "start_lng": data[1]['시작 위치(경도)'],
            "end_lat": data[1]['종료 위치(위도)'],
            "end_lng": data[1]['종료 위치(경도)'],
        }

        coordinates_info.extend([first_info, second_info])
    
    else:
        for entry in data:
            entry_info = {
                "start_lat": entry['시작 위치(위도)'],
                "start_lng": entry['시작 위치(경도)'],
                "end_lat": entry['종료 위치(위도)'],
                "end_lng": entry['종료 위치(경도)'],
            }
            coordinates_info.append(entry_info)

    return coordinates_info





def convert_to_route_format(data):
    route_data = {}

    for i, route_info in enumerate(data):
        route_key = f"route{i + 1}"
        coordinates_list = []

        for location_info in route_info:
            coordinates_list.append({"lat": location_info['start_lat'], "lng": location_info['start_lng']})
            coordinates_list.append({"lat": location_info['end_lat'], "lng": location_info['end_lng']})

        route_data[route_key] = coordinates_list

    return route_data

def generate_combined_list(str_data, dict_data, dict_data2):
    list_data = ast.literal_eval(str_data)

    combined_list = []

    for i in range(len(list_data)):
        crossing_point = [{"lat": list_data[i]['latitude'], "lng": list_data[i]['longitude']}]
        route_key = f"route{i + 1}"
        route_info = [{"lat": point['lat'], "lng": point['lng']} for point in dict_data[route_key]]
        route_key2 = f"route{i + 1}"
        route_info2 = [{"lat": point['lat'], "lng": point['lng']} for point in dict_data2[route_key2]]
        
        combined_list.append({"crossing_point": crossing_point, "route1": route_info, "route2": route_info2})

    transformed_data = []

    for i, data in enumerate(combined_list, start=1):
        transformed_data.append({'data{}'.format(i): [data]})

    return transformed_data

def list_to_json(lst):
    json_data = json.dumps(lst, indent=2)
    return json_data

@app.route('/', methods=['GET'])
def index():
    return 'Hello World!'



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_file', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            uuid_test = uuid.uuid4()
            random_file_name = str(uuid_test)[:6]
            random_file_name_json = random_file_name + '.json'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], random_file_name_json))
            return random_file_name

@app.route('/upload_date', methods=['POST'])
def upload_date():
    if request.method == 'POST':
        date_str = request.form.get('date')
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            return f"날짜: {date}"
        except Exception as e:
            return f"에러 발생: {str(e)}"
    return render_template('index.html')

@app.route('/upload_address', methods=['POST'])
def upload_address():
    if request.method == 'POST':
        address = request.form.get('address')
        try:
            location = geolocator.geocode(address)
            if location:
                latitude = location.latitude
                longitude = location.longitude
            else:
                latitude = longitude = None
        
            return f"주소: {address}, 위도: {latitude}, 경도: {longitude}"
        except Exception as e:
            return f"에러 발생: {str(e)}"
    return render_template('index.html')







@app.route('/analyze', methods=['POST'])
def analyze():

    result_location_info1 = []
    result_location_info2 = []

    params = request.get_json()

    x = params['key1']
    y = params['key2']
    
    a = open_json_with_key(f'{x}.json')
    b = open_json_with_key(f'{y}.json')

    # return f'{x}.json'
    
    cf1 = activity_and_stay(a)
    cf2 = activity_and_stay(b)

    df1 = pd.DataFrame(cf1)
    df2 = pd.DataFrame(cf2)

    meeting_points = make_meeting_points(df1, df2)
    data_place_number = data_to_math(meeting_points)

    meeting_points_time = make_meeting_points_only_time(df1, df2)

    for i in meeting_points_time:
        result = find_rows2(df1,i)
        result_location_info1.append(generate_location_info3(result, i))

    for i in meeting_points_time:
        result = find_rows2(df2, i)
        result_location_info2.append(generate_location_info3(result, i))

    result_location_info1 = convert_to_route_format(result_location_info1)
    result_location_info2 = convert_to_route_format(result_location_info2)

    result = generate_combined_list(data_place_number, result_location_info1, result_location_info2)
    result_json = list_to_json(result)

    return result

@app.route('/data_test', methods=['GET'])
def data_test():
    result_location_info1 = []
    result_location_info2 = []
    
    a = open_json_with_key('9d3ea4.json')
    b = open_json_with_key('fb5818.json')

    # return f'{x}.json'
    
    cf1 = activity_and_stay(a)
    cf2 = activity_and_stay(b)

    df1 = pd.DataFrame(cf1)
    df2 = pd.DataFrame(cf2)

    meeting_points = make_meeting_points(df1, df2)
    data_place_number = data_to_math(meeting_points)

    meeting_points_time = make_meeting_points_only_time(df1, df2)

    for i in meeting_points_time:
        result = find_rows2(df1,i)
        result_location_info1.append(generate_location_info3(result, i))

    for i in meeting_points_time:
        result = find_rows2(df2, i)
        result_location_info2.append(generate_location_info3(result, i))

    result_location_info1 = convert_to_route_format(result_location_info1)
    result_location_info2 = convert_to_route_format(result_location_info2)

    result = generate_combined_list(data_place_number, result_location_info1, result_location_info2)
    result_json = list_to_json(result)

    return result
    

if __name__ == '__main__':
    
    # app.secret_key = 'super secret key'
    # app.config['SESSION_TYPE'] = 'filesystem'
    # sess.init_app(app)
    app.run(host='0.0.0.0')
