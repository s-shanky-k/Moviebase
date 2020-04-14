from flask import Flask , render_template , url_for , request ,flash , redirect ,session, json
import os
import psycopg2
from psycopg2 import Error
from flask.json import jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)
l_email=' '
b_name=' '
df=pd.DataFrame()
app.secret_key = 'super secret'
def connect_db():
    connection = psycopg2.connect(host="localhost",
                                database="movie",
                                user="postgres",
                                port="5432",
                                password="0000")
    
    try:
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
 
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]') 

    if (len(pwd)>=5) and (len(pwd)<=25) and not (pwd.isupper()) and not (pwd.islower()) and not regex.search(pwd)==None:        
        return 1
    else: 
        return 0

def initialise_df():
    global df
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.feature_extraction.text import CountVectorizer

    #READ CSV
    df=pd.read_csv('movie_dataset.csv')

    #SELECT FEATURES
    features=['keywords','cast','genres','director']

    #CREATE A COL IN DF WHICH COMBINES ALL SELECTED FEATURES
    for feature in features:
        df[feature] = df[feature].fillna('')
        
    def combine_feature(row):
        try:
            return row['keywords']+' '+row['cast']+' '+row['genres']+' '+row['director']
        except:
            print("ERROR: ",row)

    df["combined_features"]=df.apply(combine_feature,axis=1)

    df["combined_features"].head()

    #CREATE COUNT MATRIX FROM THIS NEW COMBINED COLUMN
    cv=CountVectorizer()
    count_matrix=cv.fit_transform(df['combined_features'])


    #COMPUTER THE COSINE SIMILARITY BASED ON COUNT_MATRIX
    cosine_sim=(cosine_similarity(count_matrix))  
    return(cosine_sim) 

#HELPER FUNCTIONS
def get_index_from_title(title):
    global df
    return df[df['title']==title]['index'].values[0]

def get_title_from_index(index):
    global df
    return df[df['index']==index]['title'].values[0]

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/to_login')
def to_login():
        return render_template('index.html')

#LOGIN PAGE
@app.route('/login' , methods=['GET','POST'])
def login():
    global l_email
    global b_name
    conn=connect_db()
    cursor=conn.cursor()

    if request.method == 'POST':
        l_email = request.form['email']
        l_pass_word = request.form['pass_word']
        #print(l_pass_word,l_email)
        

        cursor.execute("select u_email , u_pass_word,u_name from users")
        rows=cursor.fetchall()
        #print(rows)
        f=2
        for r in rows:
            if r[0] == l_email :
                f=1
                if r[1] == l_pass_word:
                    b_name = r[2]
                    return render_template("success.html",name = r[2],email=r[0])
                else:
                    break
                            
        return render_template("index.html",flag=f)

        
#SIGN UP PAGE
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
        
       
        return render_template('index.html')
        
#ON SUCCESSFULL LOGIN
@app.route('/success')
def success():
    global b_name
    return render_template('success.html',name = b_name)     
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

#WHEN USER LIKES A MOVIE
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



@app.route('/dislike' ,methods=['POST','GET'])
def dislike():
    if request.method=='POST':
        id_dict=request.get_json()
        mname=id_dict['name']        
        conn=connect_db()
        cursor=conn.cursor()
        sql="""DELETE FROM LIKED WHERE u_email =%s and m_name=%s"""
        cursor.execute(sql,(l_email,mname))
        cursor.close()
        conn.commit()
        conn.close()
        return jsonify(id_dict)


@app.route('/liked_movies',methods=['GET','POST'])
def liked_movies():

    conn=connect_db()
    cursor=conn.cursor()
    sql="""select m_id,m_name from liked where u_email = %s"""
    cursor.execute(sql,[l_email])
    result=cursor.fetchall()
    return render_template('liked_movies.html',result=result,l=len(result))

#FOR MOVIEBOARD
@app.route('/movieboard')
def movieboard():
    conn=connect_db()
    cursor=conn.cursor()
    sql = """ select m_name,count(u_email) from liked group by m_name order by count(u_email) desc """
    cursor.execute(sql)
    y=cursor.fetchall()
    return render_template('movieboard.html',most_liked=y)

@app.route("/recommendation")
def recommendation():
    global df
    cosine_sim = initialise_df()
    conn=connect_db()
    cursor=conn.cursor()
    sql="""select m_name from liked where u_email = %s"""
    cursor.execute(sql,[l_email])
    movie_user_likes=cursor.fetchall()
    print(movie_user_likes)
    similar_movies=[]
    ans=[]
    for i in movie_user_likes:
        #print(i[0])
        #print(df['title'].values)
        if i[0] in df['title'].values:
            #print("BOOM",i[0])
            movie_index=get_index_from_title(i[0])
            similar_movies.extend((cosine_sim[movie_index]))
    ans.extend((list(enumerate(similar_movies))))

    #GET A LIST OF SIMILAR MOVIES IN DESCENDING ORDER OF SIMILARITY SCORES
    sorted_similar_movies=sorted(ans,key=lambda x:x[1],reverse=True)

    #PRINT TITLES OF FIRST 50 MOVIE
    similar_movie_titles=[]
    i=0
    for i in range(len(movie_user_likes),len(sorted_similar_movies)):

        if sorted_similar_movies[i][0]>4803:
            similar_movie_titles.append(get_title_from_index(sorted_similar_movies[i][0]%4803))
        else:                                                     
            similar_movie_titles.append(get_title_from_index(sorted_similar_movies[i][0]))
        i=i+1
        if i==25:
            break
    print(similar_movie_titles)
    return render_template('recommendation.html',similar_movie_titles=similar_movie_titles,l=len(similar_movie_titles))       
    


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

