from database import connection

# 해야 할 일 내용 가져오기
# 최근에 작성된 순서대로

def get_quality_data_list(char2_0, char2, char2_1):
    conn = connection.get_connection()
    cursor = conn.cursor()
    if char2_0 == 'Q_all':
        sql = '''
        select product_key,product_test,product_test_timestamp,
        date_format( product_test_timestamp , '%%Y년%%m월%%d일 %%H시%%i분%%s초' ) as insert_date
        from product_quality
        where date_format(product_test_timestamp , '%%Y-%%m-%%d') >= '%s'
        and date_format(product_test_timestamp , '%%Y-%%m-%%d') <= '%s'
        order by product_test_timestamp ASC
        ''' % (char2, char2_1)
    else:
        sql = '''
        select product_key,product_test,product_test_timestamp,
        date_format( product_test_timestamp , '%%Y년%%m월%%d일 %%H시%%i분%%s초' ) as insert_date
        from product_quality
        where product_test = '%s' and date_format(product_test_timestamp , '%%Y-%%m-%%d') >= '%s'
        and date_format(product_test_timestamp , '%%Y-%%m-%%d') <= '%s'
        order by product_test_timestamp ASC
        ''' % (char2_0, char2, char2_1)


    cursor.execute(sql)
    row = cursor.fetchall()
    count = 0
    data_list = []
    for obj in row :
        data_dic = {
            'product_key': obj[0],
            'product_test': obj[1],
            'product_test_timestamp': obj[2]
        }
        data_list.append(data_dic)
        if obj[1] == 'OK' or 'NOK' :
             count += 1
    conn.close
    print(count)
    return data_list