from flask import request,Flask, render_template
from bs4 import BeautifulSoup as bs
from urllib.request import Request,urlopen
import re

app = Flask(__name__)
@app.route('/')
def addRegion():
    return render_template('Website WordCount.html')


@app.route('/output_data', methods=['POST','GET'])

def output_data():
    unique_links=[]
    link_len={}
    out_arr=[]
    if request.method == 'POST':
        url = request.form['url']
        main = re.sub(r"([\w:///.]+com|info|in|org)([\w///?/=/&/_-]*)",r"\1",url,0, re.MULTILINE | re.UNICODE | re.IGNORECASE)
        req =Request(main, headers={'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/11.04 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30"})
        sample=urlopen(req)
        soap=bs(sample,"lxml")
        for data in soap.find_all('a', href=True):
            links=data['href']
            links=links if links.startswith(main) else (str(main)+str(links) if links.startswith( '/' ) else str(main)+"/"+str(links))
            if(links in unique_links):
                continue
            unique_links.append(links)
            req =Request(links, headers={'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/11.04 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30"})
            sample1=urlopen(req)
            soap1=bs(sample1,"lxml")
            [x.extract() for x in soap1.findAll(['script', 'style'])]
            data=soap1.text
            stri=re.sub('[.,/!"@:+*&^%~#=-_]','',data)
            stri=stri.split()
            num_word=len(stri)
            if(num_word<5):
                continue
            link_len['link']=links
            link_len['wordCount']=num_word
            out_arr.append(link_len)
            print(out_arr)
        return(out_arr)

if __name__ == '__main__':
   app.run(debug = True,host='192.168.43.164')
