# *- code: utf-8 -*

import json
import os
import subprocess
import datetime
'''
# initiating for a complete blogs list
articles = []
for file in os.listdir():
    if file.endswith(".md"):
        with open(file, encoding='utf-8') as post:
            post = post.readlines()
            title = ""
            date = ""
            for line in post[:5]:
                if line.startswith('title:'):
                    title = line.split(":")[1].strip()
                if line.startswith('date'):
                    date = line.split(":")[1].strip().split()[0].strip()
            articles.append({"title":title, "date": date,"content":"".join(post[5:])}) 
ct = json.dumps({"post":articles})
with open('db.json','w') as df:
    df.write(ct)
    
'''
dbs = None
date = None
with open('db.json') as blogs:
    try:
        dbs = json.loads(blogs.read())
    except:
        dbs = json.loads('{"post":[{"title":"","date":""}]}')

for file in os.listdir("."):
    if file.endswith(".md"):
        new_post = True
        with open(file,'r',encoding="utf-8") as post:
            post = post.readlines()
            title = None
            date = None
            for line in post[:5]:
                if line.startswith('title:'):
                    title = line.split(":")[1].strip()
                if line.startswith('date'):
                    date = line.split(":")[1].strip().split()[0].strip()
            if not title or not date:
                continue
            for blog in dbs['post']:
                if blog['title'] == title and blog['date'] == date:
                    new_post = False 
                    break
            if new_post:
                new_article = {"title":title,"date":date,"content":"".join(post[5:])}
                old_post = dbs['post']
                old_post.append(new_article)
                new_dbs = json.dumps({'post':old_post})
                with open('db.json','w') as post_list:
                    post_list.write(new_dbs)
                    
                dt = datetime.datetime.strptime(date,"%Y-%m-%d")
                year = str(dt.year)
                month = str("{:0>2d}".format(dt.month))
                day = str("{:0>2d}".format(dt.day))
                blog_url = os.path.join(os.path.pardir,'content',year,month,day,title)
                
                if not os.path.exists(blog_url):
                    os.makedirs(blog_url)
                    
                blog_url = blog_url.replace(os.sep,"/")
                cmd = 'pandoc ' + file + " -s -o \"" + blog_url + "/index.html\" --template=default.html5"
                print(cmd)
                subprocess.call(cmd,shell=True)
                pos = None
                ct = None
                with open('../index.html',encoding='utf-8') as page:
                    ct = page.read()
                    ltag = "<h3>" + str(year) + "</h3>"
                    pos = ct.find(ltag)
     
                new_content = ct[:pos+len(ltag)] + "\n<span><a href =\"" + os.path.join('content',year,month,day,title) + "\">" + title + "</a></span>\n<span class='date'>" + dt.strftime("%Y-%m-%d") + "</span>" + ct[pos+len(ltag):]
                with open('../index.html','w',encoding='utf-8') as page:
                    page.write(new_content)
              
os.chdir('../')
subprocess.call("git add .",shell=True)
subprocess.call("git commit -m \"add new record " + datetime.datetime.today().strftime("%Y-%m-%d") +  "\"",shell=True)
subprocess.call("git push -u origin master",shell=True)
