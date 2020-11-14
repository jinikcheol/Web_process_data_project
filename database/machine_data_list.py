from database import connection


# 해야 할 일 내용 가져오기
# 최근에 작성된 순서대로
def get_machine_data_list(char1_0, char1, char1_1):
    #char1_input = char1
    conn = connection.get_connection()
    cursor = conn.cursor()
    if char1_0 == 'OP_all':
        sql = '''
        select machine_code,product_key,start_time,end_time,process_time,machine_data,machine_data_code,
        date_format( start_time , '%%Y년%%m월%%d일 %%H시%%i분%%s초' ) as insert_date2
        from machine
        where date_format(start_time , '%%Y-%%m-%%d') >= '%s'
        and date_format(start_time , '%%Y-%%m-%%d') <= '%s'
        order by start_time ASC
        ''' % (char1, char1_1)

    else:
        sql = '''
        select machine_code,product_key,start_time,end_time,process_time,machine_data,machine_data_code,
        date_format( start_time , '%%Y년%%m월%%d일 %%H시%%i분%%s초' ) as insert_date2
        from machine
        where machine_code = '%s' and date_format(start_time , '%%Y-%%m-%%d') >= '%s'
        and date_format(start_time , '%%Y-%%m-%%d') <= '%s'
        order by start_time ASC
        ''' % (char1_0, char1, char1_1)

    cursor.execute(sql)
    row = cursor.fetchall()
    machine_data_list = []
    for obj in row:
        data_dic = {
            'machine_code': obj[0],
            'product_key': obj[1],
            'start_time': obj[2],
            'end_time': obj[3],
            'process_time': obj[4],
            'machine_data': obj[5],
            'machine_data_code': obj[6]
        }
        machine_data_list.append(data_dic)

    conn.close
    return machine_data_list
