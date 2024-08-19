from flask import Flask, request, render_template, jsonify
import pandas as pd
import threading
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
import string
from flask import Flask, render_template, request,session
import os
from groq import Groq
from textblob import TextBlob
import praw
from gtts import gTTS
import pygame




client = MongoClient("mongodb+srv://vedesh:Vedeshsb003%40@user.8fwgqcw.mongodb.net/?retryWrites=true&w=majority&appName=user")
db = client.get_database('CTS_Hackathon')
users_collection = db.get_collection('User_Info')

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key')

l=[]
reddit = praw.Reddit(client_id='no8hReHJd7iLCkHTv5qrew',
                     client_secret='x7aLi6jBnvO45g7Pv1iKnZoWs-tpGw',
                     user_agent='your_user_agent')


def genai(initial):
    client = Groq(api_key="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")
    chat_completion = client.chat.completions.create(
        messages=[
                {
                    "role": "user",
                    "content": initial,
                }
                ],
        model="llama3-8b-8192",
            )
    response=chat_completion.choices[0].message.content
    return response
        

        


def filter_word(n):
    print(n, 'input')
    res = []
    for i in [n]:
        t, st = [], ''
        for j in i:
            if j in string.punctuation or j.isspace():
                if not st.strip().isspace():
                    t.append(st.strip())
                st = ''
            else:
                st += j
        t.append(st.strip())
        res.append('-'.join(list(filter(lambda x: x != '', t))))
    return res


def review(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    c = soup.find_all('div', class_="ddc-sidebox ddc-sidebox-rating")
    for i in c:
        a = (i.find('a')['href'])
    url = "https://www.drugs.com" + a+"?search=&sort_reviews=time_on_medication#reviews"
    print(url)
    review_response = requests.get(url)
    review_soup = BeautifulSoup(review_response.content, 'html.parser')
    cont = review_soup.find_all('div', class_='ddc-comment ddc-box ddc-mgb-2')
    v = []
    po = []
    for i in cont:
        v.append(i.find('p').text)
    for i in range(len(v)):
        result = v[i].split('"')[1::2]
        po.append(result)
    for i in range(2,6):
        url_many="https://www.drugs.com" + a+"?search=&sort_reviews=time_on_medication&page="+str(i)
        print(url_many)
        review_response = requests.get(url_many)
        review_soup = BeautifulSoup(review_response.content, 'html.parser')
        cont = review_soup.find_all('div', class_='ddc-comment ddc-box ddc-mgb-2')
        for i in cont:
            v.append(i.find('p').text)
        for i in range(len(v)):
            result = v[i].split('"')[1::2]
            po.append(result)
    print(len(po))
    if len(po)==0:
        raise Exception("NO REVIEW")
    return po


def webdata(s):
    medicine=s
    s = filter_word(s)
    a = s[0]
    p = "https://www.drugs.com/sfx/" + a + "-side-effects.html"
    print(p)

    # Thread to fetch data concurrently
    def fetch_data_thread(url,a):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                l.append(s)
                result=soup.get_text()
            else:
                print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            #initial = "give only side effect details in bulletin points from data: " + result
            prompt = f"""
            Instructions:
                1. Extract and list only the side effects mentioned in the data provided.
                2. Ensure that the response should be categorized and contains only the names of the category name, such as "pain", "urinary problem", "digestive problem", "skin" etc.
                3. Do not include any other words, phrases, or explanations in the response.
                4. Each side effect should be unique. Do not list any repeated words or phrases.
                5. Exclude words that have the same or similar meanings (e.g., do not list both "fever" and "high temperature"—only include one).
                6. instead of index numbers of the reviews replace it with * symbol
                

            ## Data:
            {result}

            ### effects:
            """
            gen=genai(prompt)
            effect_list=[]
            list_effect=[]
            effect=''
            for i in gen:
                if i!='*':
                    effect+=i
                elif i=='*':
                    list_effect.append(effect)
                    effect_list.append(list_effect)
                    list_effect=[]
                    effect=''
            if effect:
                list_effect.append(effect)
                effect_list.append(list_effect)
            return effect_list
        except:
            drug=a
            prompt_drug=f"""Instructions:
                1. List all the known side effects associated with the given medicine.
                2. Provide the side effects in a simple, clear format without any additional explanations or unrelated information.
                3. Ensure the list is comprehensive, including both common and rare side effects.
                4. Do not include any repeated words, similar words, or words with similar synonyms in the response. Each side effect should be unique.
                5. instead using numbers to represent index use * character

                ### Medicine:
                {drug}

                ### Side Effects:"""
            effects=genai(prompt_drug)
            effect_list=[]
            list_effect=[]
            effect=''
            for i in effects:
                if i!='*':
                    effect+=i
                elif i=='*':
                    list_effect.append(effect)
                    effect_list.append(list_effect)
                    list_effect=[]
                    effect=''
            if effect:
                list_effect.append(effect)
                effect_list.append(list_effect)
            return effect_list

    def fetch_reddit_data(drug_name, max_posts=5):
        j=[]
        posts = []
        for submission in reddit.subreddit('all').search(drug_name, limit=max_posts):
            posts.append(submission.title + " " + submission.selftext)
            j.append(posts)
        return j


    def t_ex(text):
        text2 = []
        s = ''
        for i in text:
            if i != '.':
                s += i
            elif i == '.':
                text2.append(s)
                s = ''
        if s:
            text2.append(s)
        return text2

    def sentiment_analyze(a):
        for sen in a:
            s1=TextBlob(sen).sentiment.polarity
            s2=TextBlob(sen).sentiment.subjectivity
            return s1
    
    def senti_process(data,senti_counts):
        a1=sentiment_analyze(data)
        if a1==0.0:
            senti_counts[1]+=1
        elif a1>=0.0:
            senti_counts[0]+=1
        elif a1<=-0.0:
            senti_counts[2]+=1
        return senti_counts
            
        
    def senti_summary(tex):
        d={}
        prompt = f"""Instructions:
                            1. Read the provided data carefully.
                            2. Summarize all the reviews to create an easy-to-understand overview of the medicine.
                            3. Highlight the overall sentiment, key strengths, weaknesses, and common experiences mentioned in the reviews.
                            4. Ensure the summary is clear, informative, and helps users understand the medicine's effects and user experiences.
                            5. Structure the response so that each highlighted word (such as strengths, weaknesses, etc.) is followed by the summary in the next line.
                            6. Underline each key word (such as Overall Sentiment, Strengths, Weaknesses, and Common Experiences) to make them stand out like titles.

                        ### Data:
                        {tex}

                        Comprehensive Review Summary:

                        **Overall Sentiment:** 
                        [Summary of overall sentiment]

                        **Strengths:**  
                        [Summary of strengths]

                        **Weaknesses:** 
                        [Summary of weaknesses]

                        **Common Experiences:** 
                        [Summary of common experiences]

                        """
        fir=genai(prompt)
        main_list=[]
        list_review=[]
        review=''
        for i in fir:
            if i!='*':
                review+=i
            elif i=='*':
                list_review.append(review.strip("\n"))
                main_list.append(list_review)
                list_review=[]
                review=''
        if review:
            list_review.append(review)
            main_list.append(list_review)
        return main_list            
        
    

    # Thread to process reviews concurrently
    def process_reviews_thread(url,a):
        senti_counts=[0,0,0]
        try:
            reddit=fetch_reddit_data(a)
            for i in reddit:
                text=t_ex(i)
                reddit_senti=senti_process(text,senti_counts)
            print(reddit_senti)
            d = review(url)
            for i in d:
                s=''
                for j in i:  
                    s+=j
                c=t_ex(s)
                drugs_senti=senti_process(c,senti_counts)
            print(drugs_senti)
            tex = ''
            for i in range(0,len(d),7):
                for j in d[i]:
                    tex += j
            summary=senti_summary(tex)
            r=[]
            r.append(drugs_senti)
            r.append(summary)
            return r

        except:
            tex=a
            summary_list=[]
            for i in range(10):
                prompt_list=[]
                prompt=f"""Instructions:
                        1. Analyze the provided data to understand the context of the medicine.
                        2. Generate realistic user reviews that reflect typical experiences with the medicine.
                        3. Ensure the reviews cover various aspects, including overall sentiment, key strengths, weaknesses, and common experiences.
                        4. Write the reviews in a way that they sound authentic and represent different perspectives.
                        5. ensure that the response does not have any special characters
                        6. instead of index numbers of the reviews replace it with * symbol

                        ### Data:
                        {tex}

                        ### Generated User Reviews List:

                            reviews
                        """
                syn_review=genai(prompt)
                prompt_list.append(syn_review)
                summary_list.append(prompt_list)
            # print(summary_list)
            for i in summary_list:
                s=''
                for j in i:  
                    s+=j
                c=t_ex(s)
                except_senti=senti_process(c,senti_counts)
            print(except_senti)
            exe_tex=''
            for i in summary_list:
                for j in i:
                    exe_tex+=j
            r=[]
            r.append(except_senti)
            r.append(senti_summary(exe_tex))
            return r
                

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
    return render_template('index.html')

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
    return render_template('mac_book_air_1.html', results=results)

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
                return render_template('index.html')    
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
    return jsonify(suggestions)  # Return top 10 suggestions

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

@app.route('/speechreview',methods=['GET','POST'])
def speechreview():
    if request.method == 'POST':
        review_summary = request.form.get('review_summary')
        speech(review_summary)
    return print1()

def speech(data):
        
    tts = gTTS(text=data, lang='en')
    tts.save("output.mp3")

    # Step 2: Initialize pygame mixer
    pygame.mixer.init()

    # Step 3: Load the MP3 file
    pygame.mixer.music.load("output.mp3")

    # Step 4: Play the MP3 file
    pygame.mixer.music.play()

    # Step 5: Implement pause and resume functionality
    is_paused = False

    while pygame.mixer.music.get_busy():
        command = input("Enter 'p' to pause, 'r' to resume, 'q' to quit: ")

        if command.lower() == 'p':
            pygame.mixer.music.pause()
            is_paused = True
            print("Paused")
            
        elif command.lower() == 'r' and is_paused:
            pygame.mixer.music.unpause()
            is_paused = False
            print("Resumed")
            
        elif command.lower() == 'q':
            pygame.mixer.music.stop()
            print("Stopped")
            break
        """engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        voices = engine.getProperty('voices')

        for voice in voices:
            if 'male' in voice.name.lower() and 'english' in voice.languages:
                engine.setProperty('voice', voice.id)
                break
        clean_text = text.replace('#', ',').replace('*',',').replace('_',',')
        engine.say(clean_text)
        engine.runAndWait()
        return print1()
"""
def print1():
    print("hi")

if __name__ == '__main__':
    app.run(debug=True)
