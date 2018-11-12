import os
from datetime import datetime as dt
import calendar
import exifread
from flask import Flask, jsonify, render_template, send_file, redirect

app = Flask(__name__)

source_folder = r"D:\MyFiles\OneDrive\传奇健身"


def get_orignal_datetime(filepath):
    f = open(filepath, 'rb')
    tags = exifread.process_file(f)

    if "EXIF DateTimeOriginal" in tags:
        return str(tags["EXIF DateTimeOriginal"])
    else:
        return ""


def find_matching_image(folder, date):
    image_path = None
    for root, dirnames, filenames in os.walk(folder):
        for filename in filenames:

            filePath = os.path.join(root, filename)
            datetime = get_orignal_datetime(filePath)
            if not datetime:
                datetime = os.path.getmtime(filePath)
                datetime = dt.fromtimestamp(datetime).strftime('%Y-%m-%d')
            else:
                parts = datetime.split()
                datetime = parts[0].replace(':', '-')
            if datetime == date:
                image_path = filePath
                break
    return image_path


def get_all_dates(folder):
    all_dates = []
    for root, dirnames, filenames in os.walk(folder):
        for filename in filenames:

            filePath = os.path.join(root, filename)
            datetime = get_orignal_datetime(filePath)
            # if filename=='wx_camera_1491820178605.jpg':
            # print('datetime:%s'%(datetime))
            if not datetime:
                datetime = os.path.getmtime(filePath)
                datetime = dt.fromtimestamp(datetime).strftime('%Y-%m-%d')
                # print('format:%s' % datetime)
            else:
                parts = datetime.split()
                datetime = parts[0].replace(':', '-')
                # print('else:%s' % datetime)
            all_dates.append(datetime)
    return all_dates


def get_days_in_month(year_month):
    parts = year_month.split('-')
    return calendar.monthrange(int(parts[0]), int(parts[1]))


def group_dates_by_month(dates):
    result = {}
    for date in dates:
        month_key = date[0:7]
        if result.get(month_key) is None:
            days_count_weekday = get_days_in_month(month_key)
            result[month_key] = {
                "daysCount": days_count_weekday[1], "days": [date], "firstDay": days_count_weekday[0]}
        else:
            result[month_key]['days'].append(date)
    return result


@app.route('/img/<string:date>')
def image(date):
    image = find_matching_image(source_folder, date)
    return send_file(image, mimetype='image/jpg')


@app.route('/index')
def index():
    all_dates = get_all_dates(source_folder)
    group = group_dates_by_month(all_dates)
    print(sorted(group))
    return render_template('index.html', dategroup=group)

@app.route('/index/<string:year>')
def index_year(year):
    all_dates = get_all_dates(source_folder)
    filter_dates = [x for x in all_dates if x.startswith(year)]
    group = group_dates_by_month(filter_dates)
    return render_template('index.html', dategroup=group)

@app.route('/')
def default():
    return redirect('/index')


@app.route('/dates')
def get_dates():
    all_dates = get_all_dates(source_folder)
    print(all_dates[len(all_dates)-1])
    group = group_dates_by_month(all_dates)
    return jsonify(group)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
