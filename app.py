from flask import Flask, render_template, redirect, request, url_for, jsonify, make_response
from process import process_operate
from OEE_calculator import OEE_cal
from SQL import MySQL_query
from time import time
import json
import pymysql
from datetime import datetime

app = Flask(__name__)

app.count = 1

@app.route('/Home')
def Home():
    return render_template('Home.html')


@app.route('/Monitoring')
def Monitoring():
    return render_template('Monitoring.html')


@app.route('/OEE')
def OEE():
    return render_template('OEE.html')


@app.route('/OEE_Calculator')
def OEE_Calculator():

    OEE_list = []
    OEE_dict = {}

    availability = OEE_cal.Availability_Calculator(1)

    productivity = OEE_cal.Productivity_Calculator(1)

    quality = OEE_cal.Quality_Calculator(1)

    OEE = (availability * productivity * quality) / 10000

    OEE_dict['OEE'] = str(OEE)
    OEE_dict['availability'] = str(availability)
    OEE_dict['productivity'] = str(productivity)
    OEE_dict['quality'] = str(quality)

    OEE_list.append(OEE_dict)

    return jsonify(OEE_list)


@app.route('/re_data', methods=["GET", "POST"])
def re_data():
    a = OEE_cal.Availability_Calculator(1)  # 시간가동률
    b = OEE_cal.Productivity_Calculator(1)  # 성능가동률
    c = OEE_cal.Quality_Calculator(1)  # 품질
    d = a * b * c / 10000  # OEE
    data = [time() * 1000, d, a, b, c]

    response = make_response(json.dumps(data))

    response.content_type = 'application/json'

    return response


@app.route('/real_value', methods=["GET", "POST"])
def real_value():
    now_data = MySQL_query.get_item_count_now(1)  # 실제값 하루 생산되는 양품수
    OK_count = now_data[0]['item_count']
    quality = round(OK_count, 1)
    data = [time() * 1000, quality]

    response = make_response(json.dumps(data))

    response.content_type = 'application/json'

    return response



@app.route('/Machine')
def Machine():
    return render_template('Machine.html')


@app.route('/Process')
def Machine_start():
    return process_operate.process_start(1)


@app.route('/live_Electronic_OP10')
def live_Electronic_OP10():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='data12345', db='projectdata', charset='utf8')
    cursor = conn.cursor()
    cursor.execute("SELECT machine_data from machine where machine_code = 'OP10' and machine_data_code = 'E01' ")
    results = cursor.fetchall()
    result_list = list(results[-1])
    result = str(result_list)
    result_re1 = result.replace("[", "")
    result_re2 = result_re1.replace("]", "")
    result_re3 = float(result_re2)
    app.count += 1
    data = [time() * 5000, result_re3]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response


@app.route('/realtime_data')
def post_realtime_data():
    parameter = MySQL_query.get_product_key_machine_code(1)
    product_key = parameter[0]['product_key']
    machine_code = parameter[0]['machine_code']

    data = MySQL_query.get_machine_data_for_realtime(machine_code, product_key)

    data = data[0]  # 여기서 data가 딕셔너리 형태로 변환

    data_list = []
    product_key = product_key[-4:]

    machine_data = data['machine_data']
    process_time = data['process_time']
    start_time = data['start_time']
    end_time = data['end_time']
    product_test = data['product_test']
    product_size_l = data['product_size_l']
    product_size_w = data['product_size_w']
    product_size_h = data['product_size_h']

    data_list.append(product_key)
    data_list.append(machine_code)
    data_list.append(machine_data)
    data_list.append(process_time)
    data_list.append(start_time)
    data_list.append(end_time)
    data_list.append(product_test)
    data_list.append(product_size_l)
    data_list.append(product_size_w)
    data_list.append(product_size_h)

    return data


@app.route('/realtime_table_OP10')
def realtime_table_OP10():
    count = app.count
    conn = pymysql.connect(host='127.0.0.1', user='root', password='data12345', db='projectdata', charset='utf8')

    sql = '''
                   SELECT machine.product_key, machine.machine_code, machine.machine_data, machine.process_time, 
                   machine.start_time, machine.end_time, product_quality.product_test, 
                   product_quality.product_size_l, product_quality.product_size_w, product_quality.product_size_h
                   FROM machine INNER JOIN product_quality
                   ON  machine.product_key = product_quality.product_key
                   WHERE machine.machine_code = 'OP10' order by end_time DESC LIMIT %s
           ''' % (count)

    cursor = conn.cursor()
    cursor.execute(sql)
    row = cursor.fetchall()
    app.count += 1
    data_list = []
    for obj in row:
        data_dic = {
            'product_key': obj[0][-4:],
            'machine_code': obj[1],
            'machine_data': str(obj[2]),
            'process_time': str(obj[3]),
            'start_time': obj[4],
            'end_time': obj[5],
            'product_test': obj[6],
            'product_size_l': str(obj[7]),
            'product_size_w': str(obj[8]),
            'product_size_h': str(obj[9])
        }
        data_list.append(data_dic)

    conn.close()

    return jsonify(data_list)


@app.route('/MachineOP20')
def Machine20():
    return render_template('MachineOP20.html')


@app.route('/live_Electronic_OP20')
def live_Electronic_OP20():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='data12345', db='projectdata', charset='utf8')
    cursor = conn.cursor()
    cursor.execute("SELECT machine_data from machine where machine_code = 'OP20' and machine_data_code = 'E01' ")
    results = cursor.fetchall()
    result_list = list(results[-1])
    result = str(result_list)
    result_re1 = result.replace("[", "")
    result_re2 = result_re1.replace("]", "")
    result_re3 = float(result_re2)
    app.count += 1
    data = [time() * 5000, result_re3]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response


@app.route('/MachineOP30')
def MachineOP30():
    return render_template('MachineOP30.html')


@app.route('/live_Electronic_OP30')
def live_Electronic_OP30():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='data12345', db='projectdata', charset='utf8')
    cursor = conn.cursor()
    cursor.execute("SELECT machine_data from machine where machine_code = 'OP30' and machine_data_code = 'E01' ")
    results = cursor.fetchall()
    result_list = list(results[-1])
    result = str(result_list)
    result_re1 = result.replace("[", "")
    result_re2 = result_re1.replace("]", "")
    result_re3 = float(result_re2)
    app.count += 1
    data = [time() * 5000, result_re3]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response


@app.route('/MachineOP40')
def MachineOP40():
    return render_template('MachineOP40.html')


@app.route('/live_Temperature_OP40')
def live_Temperature_OP40():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='data12345', db='projectdata', charset='utf8')
    cursor = conn.cursor()
    cursor.execute("SELECT machine_data from machine where machine_code = 'OP40' and machine_data_code = 'T01' ")
    results = cursor.fetchall()
    result_list = list(results[-1])
    result = str(result_list)
    result_re1 = result.replace("[", "")
    result_re2 = result_re1.replace("]", "")
    result_re3 = float(result_re2)
    app.count += 1
    data = [time() * 5000, result_re3]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response


@app.route('/MachineOP50')
def MachineOP50():
    return render_template('MachineOP50.html')


@app.route('/live_Temperature_OP50')
def live_Temperature_OP50():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='data12345', db='projectdata', charset='utf8')
    cursor = conn.cursor()
    cursor.execute("SELECT machine_data from machine where machine_code = 'OP50' and machine_data_code = 'T01' ")
    results = cursor.fetchall()
    result_list = list(results[-1])
    result = str(result_list)
    result_re1 = result.replace("[", "")
    result_re2 = result_re1.replace("]", "")
    result_re3 = float(result_re2)
    app.count += 1
    data = [time() * 5000, result_re3]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response


@app.route('/Date')
def Date():
    return render_template('Date.html')


@app.route('/Item1')
def Item():
    return render_template('Item.html')


@app.route('/Item', methods=['POST', 'GET'])
def quality_data_load():
    product = {}
    if request.method == 'POST':
        product['product_test'] = request.form.get('product_test')
        #return render_template('test_load_chart.html') #, test=temp_test)
        return jsonify(product)

    elif request.method == 'GET':
        temp1 = request.args.get('date1')
        temp2 = request.args.get('date2')
        content_list = MySQL_query.get_quality_data_list(temp1, temp2)
    # now = datetime.today()
    # content_list.append(now)
        print(content_list)
        html = render_template('Item.html', quality_data_list=content_list, date1=temp1, date2=temp2)
        #html = render_template('Quality_index.html', quality_data_list=content_list, char2_0=temp2_0, char2=temp2, char2_1=temp2_1)
        return html



@app.route('/Predict')
def Predict():
    return render_template('Predict.html')


@app.route('/Analysis_OP10')
def Analysis_OP10():
    return render_template('Analysis_OP10.html')

@app.route('/Scatter_OP10')
def Scatter_OP10():

    machine_code = 'OP10'
    size = 'l'
    char1 = '2020-11-16'
    char2 = '2020-11-20'

    list_dict = MySQL_query.get_data_for_scatter(machine_code, size, char1, char2)

    data_list = []
    for i in range(len(list_dict)):
        temp_list = []

        x = list_dict[i]['machine_data']
        y = list_dict[i]['product_size']
        temp_list.append(x)
        temp_list.append(y)

        data_list.append(temp_list)

    return jsonify(data_list)


@app.route('/Pareto')
def Pareto():

    char1 = '2020-11-01'
    char2 = '2020-11-17'

    count_list = []

    OP10_NOK = MySQL_query.get_data_for_pareto('OP10', char1, char2)
    OP20_NOK = MySQL_query.get_data_for_pareto('OP20', char1, char2)
    OP30_NOK = MySQL_query.get_data_for_pareto('OP30', char1, char2)
    OP40_NOK = MySQL_query.get_data_for_pareto('OP40', char1, char2)
    OP50_NOK = MySQL_query.get_data_for_pareto('OP50', char1, char2)

    count_OP10 = OP10_NOK[0]['NOK']
    count_OP20 = OP20_NOK[0]['NOK']
    count_OP30 = OP30_NOK[0]['NOK']
    count_OP40 = OP40_NOK[0]['NOK']
    count_OP50 = OP50_NOK[0]['NOK']

    count_list.append(count_OP10)
    count_list.append(count_OP20)
    count_list.append(count_OP30)
    count_list.append(count_OP40)
    count_list.append(count_OP50)

    data1 = [count_OP10]
    data2 = [count_OP20]
    data3 = [count_OP30]
    data4 = [count_OP40]
    data5 = [count_OP50]
    print(count_list)
    data_list = [data1, data2, data3, data4, data5]
    response = make_response(json.dumps(count_list))
    response.content_type = 'application/json'
    # return response
    return jsonify(count_list)


@app.route('/chart_test')
def chart_test():
    return render_template('chart_test.html')


@app.route('/Pareto_chart')
def Pareto_chart():
    return render_template('Pareto.html')

@app.route('/bar_chart_test')
def bar_chart_test():
    return render_template('bar_chart_test.html')


@app.route('/Login')
def Login():
    return render_template('Login.html')


@app.route('/Signin')
def Signin():
    return render_template('Signin.html')


if __name__ == '__main__':
   app.run('0.0.0.0', port=5324, debug=True)
