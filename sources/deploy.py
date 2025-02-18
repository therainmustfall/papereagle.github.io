# *- code: utf-8 -*

import json
import os
import subprocess
import datetime
'''
# initiating for a complete blogs list
articles = []
for file in os.listdir():
    # searching for markdown files
    if file.endswith(".md"):
        with open(file, encoding='utf-8') as post:
            post = post.readlines()
            title = ""
            date = ""
            # title and date are in the first five lines
            for line in post[:5]:
                if line.startswith('title:'):
                    title = line.split(":")[1].strip()
                if line.startswith('date'):
                    date = line.split(":")[1].strip().split()[0].strip()
            # append article information to articles
            articles.append({"title":title, "date": date,"content":"".join(post[5:])})

# using json.dumps to convert post into a json string
ct = json.dumps({"post":articles})
with open('db.json','w') as df:
    df.write(ct)
    
'''
dbs = None
date = None
with open('db.json') as blogs:
    # loading all articles from db
    try:
        dbs = json.loads(blogs.read())
    except:
        dbs = json.loads('{"post":[{"title":"","date":""}]}')

# searching for markdown files
for file in os.listdir("."):
    if file.endswith(".md"):
        new_post = True
        with open(file,'r',encoding="utf-8") as post:
            post = post.readlines()

            # searching title and date
            title = None
            date = None
            for line in post[:5]:
                if line.startswith('title:'):
                    title = line.split(":")[1].strip()
                if line.startswith('date'):
                    date = line.split(":")[1].strip().split()[0].strip()
            if not title or not date:
                continue
            
            # checking if there is a matching title in the post
            for blog in dbs['post']:
                if blog['title'] == title and blog['date'] == date:
                    new_post = False 
                    break
            if new_post:
                # replacing spaces with hyphens
                title = title.replace(" ","-")
                new_article = {"title":title,"date":date,"content":"".join(post[5:])}
                old_post = dbs['post']
                old_post.append(new_article)
                new_dbs = json.dumps({'post':old_post})
                with open('db.json','w') as post_list:
                    post_list.write(new_dbs)

                # Getting and formatting date , string parsing to time   
                dt = datetime.datetime.strptime(date,"%Y-%m-%d")
                year = str(dt.year)
                month = str("{:0>2d}".format(dt.month))
                day = str("{:0>2d}".format(dt.day))

                # new html file would be put in content/year/month/day/title/ folder
                blog_url = os.path.join(os.path.pardir,'content',year,month,day,title)
                
                if not os.path.exists(blog_url):
                    os.makedirs(blog_url)

                # normalizing the blog url   
                blog_url = blog_url.replace(os.sep,"/")

                # convering md file to html
                cmd = 'pandoc ' + file + " -s -o \"" + blog_url + "/index.html\" --template=./default.html"
                print(cmd)
                subprocess.call(cmd,shell=True)

                # updating the homepage index.html
                pos = None
                ct = None
                with open('../index.html',encoding='utf-8') as page:
                    ct = page.read()
                    # locating same year 
                    ltag = "<h3>" + str(year) + "</h3>"
                    pos = ct.find(ltag)

                # inserting article link, title and date between year tag and remaining content    
                new_content = ct[:pos+len(ltag)] + "\n<span><a href =\"" + os.path.join('content',year,month,day,title) + "\">" + title + "</a></span>\n<span class='date'>" + dt.strftime("%Y-%m-%d") + "</span>" + ct[pos+len(ltag):]
                # flushing and updating index.html
                with open('../index.html','w',encoding='utf-8') as page:
                    page.write(new_content)

# Changing directory to parent folder and then using subprocess to add, commit and push the changes             
os.chdir('../')
subprocess.call("git add .",shell=True)
subprocess.call("git commit -m \"add new record " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +  "\"",shell=True)
subprocess.call("git push -u origin master",shell=True)
