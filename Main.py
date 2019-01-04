#!/usr/bin/python
# -*- coding: utf-8 -*-

import newspaper
import urllib.request
import random
import csv


from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts

#wordpress login client 
client = Client('https://yourworpresswebsite/xmlrpc.php','username','password')



#function for downloading top imagesfro news article
def downloader(image_url):
    file_name = random.randrange(1,10000)
    full_file_name = str(file_name) + '.jpg'
    urllib.request.urlretrieve(image_url,full_file_name)

#using newspaper library
from newspaper import Article
#for example ,we used http://www.defencenews.in 
defencenews = newspaper.build('http://target website/',
                              memoize_articles=False)

for article in defencenews.articles:
    print (article.url)

length=(defencenews.size())
print (length)
for i in range(0,2):
    print (i)

    first_article = defencenews.articles[i]
    first_article.download()
    first_article.parse()
    #html = first_article.html
    title = first_article.title
    text = first_article.text
    image = first_article.top_image
    file_name = random.randrange(1,10000)
    full_file_name = str(file_name) + '.jpg'
    urllib.request.urlretrieve(image,full_file_name)
    csv_name = str(file_name) +'.csv'
    f = csv.writer(open(csv_name,'w', encoding='utf-8'))
    f.writerow([title,image,text])

    filename = full_file_name

    # prepare metadata
    data = {
            'name': 'picture.jpg',
            'type': 'image/jpeg',  # mimetype
    }

    # read the binary file and let the XMLRPC library encode it into base64
    with open(filename, 'rb') as img:
            data['bits'] = xmlrpc_client.Binary(img.read())

    response = client.call(media.UploadFile(data))

    attachment_id = response['id']


    post = WordPressPost()
    post.title = title
    post.content = text
    post.post_status = 'publish'
    post.thumbnail = attachment_id
    post.id = client.call(posts.NewPost(post))


    print ('Success')
