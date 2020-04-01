from flask import Flask , render_template , url_for , request ,flash , redirect ,session, json
from config import config
import os
import psycopg2
from psycopg2 import Error
from flask_bootstrap import Bootstrap
from flask.json import jsonify

app = Flask(__name__)
l_email=' '
b_name=' '

Bootstrap(app)
app.secret_key = 'super secret'
def connect_db():
    conn = None
    
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
             
        return connection
        print("CONNECTED")
    except:
        print("cant connect")


#FUNCTION TO VALIDATE EMAIL
def check_mail(em):
    if('@' in em):
        k=list()
        k=em.split('@')
        if('.com' in k[1] and '@' not in k[1]):
            return 1
        else:
            return 0        
    else:
        return 0
  
        
#FUNCTION TO VALIDATE PASSWORD
def check_pass(pwd):
    import re
    lenght=len(pwd)
    print(lenght)

    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]') 

    if (len(pwd)>=5) and (len(pwd)<=25) and not (pwd.isupper()) and not (pwd.islower()) and not regex.search(pwd)==None:        
        return 1
    else: 
        return 0
        


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/to_login')
def to_login():
        return render_template('index.html')


@app.route('/login' , methods=['GET','POST'])
def login():
    global l_email
    global b_name
    conn=connect_db()
    cursor=conn.cursor()

    if request.method == 'POST':
        l_email = request.form['email']
        l_pass_word = request.form['pass_word']
        print(l_pass_word,l_email)
        

        cursor.execute("select u_email , u_pass_word,u_name from users")
        rows=cursor.fetchall()
        #print(rows)
        f=2
        for r in rows:
            print("r:",r)
            if r[0] == l_email :
                f=1
                print("r0:",r[0])
                if r[1] == l_pass_word:
                    print("r1:",r[1])
                    b_name = r[2]
                    return render_template("success.html",name = r[2],email=r[0])
                else:
                    break
                            
        return render_template("index.html",flag=f)

        

@app.route('/to_signup')
def to_signup():
    return render_template('signup.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    
    conn=connect_db()
    cursor=conn.cursor()

    if request.method == 'POST':
        s_name = request.form['name']
        s_email = request.form['email']
        s_pass_word= request.form['pass_word']
        if check_mail(s_email) == 1:
            cursor.execute("select u_email from users")
            rows=cursor.fetchall()
            for r in rows:
                print("r:",r)
                if r[0] == s_email:
                    return render_template("signup.html", flag =4)
            if check_pass(s_pass_word) == 1:
                postgres_insert_query = """ INSERT INTO users (u_name, u_email, u_pass_word) VALUES (%s,%s,%s)"""   #using this we can
                record_to_insert = (s_name,s_email,s_pass_word)                                  # pass python variables as parameters
                x=cursor.execute(postgres_insert_query, record_to_insert)
                conn.commit()
                conn.close()
                return render_template('signup.html',flag = 1)
            else:
                return render_template('signup.html',flag = 2)
        else:
            return render_template('signup.html',flag=3)
        
        print(s_name)

        
        return render_template('index.html')
        

@app.route('/success')
def success():
    global b_name
    return render_template('success.html',name = b_name)     
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


@app.route('/like' ,methods=['POST','GET'])
def like():
    if request.method=='POST':
        id_dict=request.get_json()
        mid=id_dict['id']
        mname=id_dict['name']        
        conn=connect_db()
        cursor=conn.cursor()
        sql="""INSERT INTO LIKED VALUES(%s,%s,%s)"""
        cursor.execute(sql,(l_email,mid,mname))
        cursor.close()
        conn.commit()
        conn.close()
        return jsonify(id_dict)
    return render_template('success.html')

@app.route('/liked_movies',methods=['GET','POST'])
def liked_movies():

    conn=connect_db()
    cursor=conn.cursor()
    sql="""select m_id,m_name from liked where u_email = %s"""
    cursor.execute(sql,[l_email])
    result=cursor.fetchall()
    print(result)
    return render_template('liked_movies.html',result=result)


@app.route('/movieboard')
def movieboard():
    conn=connect_db()
    cursor=conn.cursor()
    sql = """ select m_name,count(u_email) from liked group by m_name order by count(u_email) desc """
    cursor.execute(sql)
    y=cursor.fetchall()
    print(y)
    return render_template('movieboard.html',most_liked=y)

#@app.route('/user/<name>')
#def user_home(name):
#    return "hello %s" %name


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)



if __name__ == "__main__":
    app.run(debug=True) 

