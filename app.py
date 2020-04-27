import os
import markdown2
import urllib.request
import xmltodict
import json
from flask import Flask, render_template, make_response, redirect, url_for

from core.entities import Picture, Blog
from core.utils import get_file_lines

app = Flask(__name__)
PORT = 5000
FILE_SKILLS = "skills.txt"
MAX_DRONE_PICTURE_PER_PAGE = 3


def get_skills():
    return ''.join(get_file_lines(FILE_SKILLS)).split('\n')


def get_blogs():
    url = "https://raw.githubusercontent.com/earendil06/blog/master/publish.json"
    stream = urllib.request.urlopen(url)
    data = stream.read()
    stream.close()
    items = json.loads(data)
    blog_list = [Blog(b['title'], b['date'], b['filename']) for b in items]
    return blog_list


@app.route('/')
def home():
    return render_template('home.html', skills=get_skills(), blogs=get_blogs())


@app.route('/blog/<string:id>')
def blog(id):
    items = [item for item in get_blogs() if item.id() == id]
    if len(items) == 0:
        return redirect(url_for('.home'))
    return render_template('blog.html', content=markdown2.markdown(items[0].content()), blogs=get_blogs())


@app.route('/rss', methods=['GET'])
def rss():
    rss_xml = render_template('rss.xml', items=get_blogs())
    response = make_response(rss_xml)
    response.headers['Content-Type'] = 'application/rss+xml'
    return response


def get_pictures():
    url = 'https://www.flickr.com/services/feeds/photos_public.gne?id=186291426@N04&lang=en-us&format=rss_200'
    stream = urllib.request.urlopen(url)
    data = stream.read()
    stream.close()
    items = list(xmltodict.parse(data)['rss']['channel']['item'])
    pictures = [Picture(item['title'], item['media:content']['@url']) for item in items]
    return pictures


@app.route('/drone', methods=['GET'])
def drone():
    return redirect(url_for('.drone_page', page=1))


@app.route('/drone/<int:page>', methods=['GET'])
def drone_page(page):
    pictures = get_pictures()
    groups = [pictures[i:i + MAX_DRONE_PICTURE_PER_PAGE] for i in range(0, len(pictures), MAX_DRONE_PICTURE_PER_PAGE)]
    if page < 1 or page > len(groups):
        return redirect(url_for('.home'))
    return render_template('drone.html', pictures=groups[page - 1], page=page, n_pages=len(groups))


@app.route('/health', methods=['GET'])
def health():
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', PORT))
    app.run(host='0.0.0.0', port=port)
