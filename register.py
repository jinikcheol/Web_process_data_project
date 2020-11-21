from flask import Flask, render_template, request, escape, session
from datetime import timedelta
import pymysql
import bcrypt
import re

app = Flask(__name__)

app.secret_key = "DayTory123"

db = pymysql.connect(host='127.0.0.1', user='root', password='1234', db='test', charset='utf8')

cursor = db.cursor()

@app.route('/Home') ###로그인 하고 들어가는 메인 페이지를 넣을 것
def mmain():
    if not 'ID' in session:
        return ''' <script> location.href = "http://127.0.0.1:5002/" </script> '''
    else:
        return render_template("Home.html")


@app.route('/', methods=['GET'])
def index():
    if 'ID' in session:
        return ''' <script> location.href = "http://127.0.0.1:5002/Home" </script> '''
    else:
        return render_template('index.html')  # 로그인 되어 있지 않으니 로그인 홈 가기 버튼으로


app.cnt = 1
@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'GET':
        return render_template('Login.html')

    if request.method == 'POST':
        login_info = request.form

        id = login_info['ID']
        password = login_info['Password']

        sql = "SELECT * FROM total WHERE ID = %s"

        row_count = cursor.execute(sql, id)

        if app.cnt == 5:
            return ''' <script> alert("로그인 {}회 실패 하셨기에 보안을 위해 로그인 시스템을 종료합니다 "); 
                                                          location.href = "http://127.0.0.1:5002/" </script> '''\
                .format(app.cnt)

        if not row_count:
            app.cnt += 1
            return ''' <script> alert("아이디를 확인하여 주십시오"); 
                            location.href = "http://127.0.0.1:5002/login" </script> '''
        if row_count > 0:
            user_info = cursor.fetchone()
            pw_db = user_info[2]

            is_pw = bcrypt.checkpw(password.encode('UTF-8'),  pw_db.encode('UTF-8'))
            if is_pw:
                session['ID'] = id
                return ''' <script> alert("{}님이 로그인 하였습니다"); 
                location.href = "http://127.0.0.1:5002/" </script> '''.format(id)
            else:
                app.cnt += 1
                return  ''' <script> alert("비밀번호를 확인하여 주십시오"); 
                location.href = "http://127.0.0.1:5002/login" </script> '''

    return render_template('Login.html')


@app.route('/logout')
def logout():
    return ''' <script> alert("%s 님이 로그아웃 하였습니다"); 
    location.href = "http://127.0.0.1:5002/logo" </script> ''' % escape(session['ID'])

#이 두개를 한번에 붙이지 않은 이유는 session pop 한 후에는 ID가 없어서 escape기능을 못하기에
@app.route('/logo')
def logo():
    session.pop('ID', None)
    return ''' <script> location.href = "http://127.0.0.1:5002/" </script> '''

@app.before_request # 1분 시간 뒤에 session 종료
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('Signin.html')

    if request.method == 'POST':
        register_info = request.form
        id = register_info['ID']
        password = register_info['Password']
        repassword = register_info['repassword']
        email = register_info['Email']
        abc = """ 
                        Select ID from total where ID = %s
                    """
        cursor.execute(abc, id)
        row = cursor.fetchone()

        Check_count = str(type(row)) # NoneType passing
        pasing = Check_count.replace("<", "")
        pasing1 = pasing.replace("class", "")
        pasing2 = pasing1.replace("'", "")
        pasing3 = pasing2.replace("'", "")
        pasing4 = pasing3.replace(">", "")
        pasing5 = pasing4.replace(" ", "")


        if row != None:
            if id == row[0]:
                return render_template('reg1.html')

        if pasing5 == 'NoneType':  # 아이디가 생성 가능한 상황
            if not (id and password and repassword and email):
                return render_template('reg2.html')

            elif not 4 < len(password) < 20:
                return render_template('reg3.html')

            elif not (re.search('[a-z]', password) and re.search('[0-9]', password) and re.search('[A-Z]', password)):
                return render_template('reg3.html')

            elif password != repassword:
                return render_template('reg4.html')

            elif password == repassword:
                password = bcrypt.hashpw(register_info['Password'].encode('utf-8'), bcrypt.gensalt())
                sql = """
                        INSERT INTO total(ID, Password, Email) Values(%s, %s, %s)
                        """
                cursor.execute(sql, (id, password, email))
                db.commit()
                return render_template('reg5.html')

            return render_template('Signin.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5002, debug=True)