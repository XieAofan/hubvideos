from flask import Flask, render_template,request,redirect
from flask import url_for
import json
import requests
from bs4 import BeautifulSoup


class spider():
    def __init__(self) -> None:
        self.video_list_web = []
        self.web_list = []
        self.video_list = []

    def sort(self):
        t = 0
        for i in self.video_list_web:
            t = t+len(i)
        a = t
        web_right =[]
        for i in self.video_list_web:
            web_right.append(len(i)/a)
        t=0
        while True:
            if t*20 >= a-1:
                break
            l=0
            for i in web_right:
                if i !=0:
                    video_list_site =self.video_list_web[l]
                    n =20*i//1
                    self.video_list.append(video_list_site[:n])
                l = l+1
    
    def spider(self, url):
        header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/92.0.4515.107 Safari/537.36"}
        response = requests.get(url=url, headers=header)
        response.encoding = 'Utf-8'
        soup = BeautifulSoup(response.text,features="html.parser")
        print(soup.text)
        print(soup.find_all(id='center-content-list index-center-content-list no_padding'))

s=spider()
s.spider('https://www.2fdff.com/index/home.html')


app = Flask(__name__)


@app.route("/",methods=["GET"])
def sp_i():
    try:
        username=request.args.get("username")
        return render_template("index.html",username=username)
    except:
        return redirect(url_for("sp_l"))


@app.route("/login",methods=["GET"])
def sp_l():
    return render_template("login.html")


@app.route("/login",methods=["POST"])
def sp_p():
    username = request.form.get('username')
    password = request.form.get('password')
    if username=="xieaofan" and password=="666666":
        return redirect("/?username="+str(username))
    return render_template("secret/login.html",message="账号或密码错误",username=username)


@app.route("/jdlypage",methods=["GET"])
def sp_jdly():
    page = request.args.get("page")
    if page == None:
        page=1
    page=int(page)
    f=open("model/lists.txt","r")
    data = f.read()
    f.close()
    data = json.loads(data)
    data=data[page-1]
    nr=""
    for i in data['url']:
        nr=nr+'<img width="100%" src="'+str(i)+'">'
    if len(data['url'])==0:
        nr="404-NOT FOUNG"
    bpage = '<a href="jdlypage?page='+str(page-1)+'">上一页</a>'
    nextpage = '<a href="jdlypage?page='+str(page+1)+'">下一页</a>'
    return render_template("secret/jdlypage.html", next=nextpage,b=bpage,title=data['title'],nr=nr)

if __name__ == 'main__':
    app.run(
        host='0.0.0.0',
        port=80,
    )