import os
from flask import Flask, request, session, render_template, jsonify
import pandas as pd
import threading
from pymongo import MongoClient
from TextProcessing import filter_word
from SideEffectThread import fetch_data_thread
from ReviewThread import process_reviews_thread

client = MongoClient("mongodb+srv://vedesh:Vedeshsb003%40@user.8fwgqcw.mongodb.net/?retryWrites=true&w=majority&appName=user")
db = client.get_database('CTS_Hackathon')
users_collection = db.get_collection('User_Info')

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key')



def webdata(s):
    medicine=s
    s = filter_word(s)
    a = s[0]
    p = "https://www.drugs.com/sfx/" + a + "-side-effects.html"
    print(p)

    urls = [p, p]

    threads = []
    results = [None,[None,None]]
    for i, url in enumerate(urls):
        if i % 2 == 0:
            t = threading.Thread(target=lambda idx, u=url: results.__setitem__(idx, fetch_data_thread(u,a)), args=(i,))
        else:
            t = threading.Thread(target=lambda idx, u=url: results.__setitem__(idx, process_reviews_thread(u,a)), args=(i,))
        threads.append(t)

    for t in threads:
        t.start()
    for t in threads:
        t.join()
    #visual=create_sentiment_bar_chart(results[1][1])
    return results[0], results[1][0],results[1][1],medicine



@app.route('/home')
def home_main():
    return render_template('HomePage.html')

@app.route('/analyze', methods=['POST','GET'])
def analyze():
    drug_name = request.form.get("drug_name", "")
    side_effects, sentiment, review_summary,medicine = webdata(drug_name)
    results = {
        "side_effects": side_effects,
        "sentiment": sentiment,
        "review_summary": review_summary,
        "medicine": medicine
    }
    return render_template('Result.html', results=results)

@app.route('/blogpage')
def blog():
    return render_template('blog.html')

@app.route('/', methods=['GET', 'POST'])
def intro():
    return render_template('IntroPage.html')

@app.route('/login', methods=['GET','POST'])
def loginpage():
    return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
def login():
    msg = ''
    print(request.method)
    print(request.form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        print("hi")
        try:
            username = request.form['username']
            password = request.form['password']
            user = users_collection.find_one({'username': username})
            if user and user['password'] == password:
                session['loggedin'] = True
                session['username'] = user['username']
                print("hi")
                return render_template('HomePage.html')    
            else:
                msg = 'Incorrect username/password!'
        except:
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)


@app.route('/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html')

@app.route('/search_suggestions', methods=['GET'])
def search_suggestions():
    query = request.args.get('query', '')
    df = pd.read_csv('drug_name.csv') 
    suggestions = df[df['drugName'].str.contains(query, case=False, na=False)]['drugName'].tolist()
    return jsonify(suggestions)

@app.route('/logout')
def logout():
    """session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)"""
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if users_collection.find_one({'username': username}) and users_collection.find_one({'password': password}):
            msg="User Already Exist!"
        else:
            users_collection.insert_one({'username': username, 'password': password,'email':email})
            msg = 'You have successfully registered!'

    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('login.html', msg=msg)
