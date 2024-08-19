import praw
from bs4 import BeautifulSoup
import requests



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

def fetch_reddit_data(drug_name, max_posts=5):
        j=[]
        posts = []
        for submission in reddit.subreddit('all').search(drug_name, limit=max_posts):
            posts.append(submission.title + " " + submission.selftext)
            j.append(posts)
        return j

reddit = praw.Reddit(client_id='no8hReHJd7iLCkHTv5qrew',
                     client_secret='x7aLi6jBnvO45g7Pv1iKnZoWs-tpGw',
                     user_agent='your_user_agent')