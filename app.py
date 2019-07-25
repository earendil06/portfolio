import os

import markdown2
from flask import Flask, render_template, make_response

from core.entities import Blog
from core.utils import get_file_lines

app = Flask(__name__)
PORT = 5000
RSS_DIRECTORY = "rss_items"
FILE_SKILLS = "skills.txt"


def get_skills():
    return ''.join(get_file_lines(FILE_SKILLS)).split('\n')


def get_blogs():
    blog_list = [Blog(RSS_DIRECTORY + "/" + f) for f in os.listdir(RSS_DIRECTORY) if f.endswith(".md")]
    return [b for b in blog_list if b.is_valid()]


@app.route('/')
def home():
    return render_template('home.html', skills=get_skills(), blogs=get_blogs())


@app.route('/blog/<string:id>')
def blog(id):
    items = [item for item in get_blogs() if item.id() == id]
    if len(items) == 0:
        return home()
    return render_template('blog.html', content=markdown2.markdown(items[0].content()), blogs=get_blogs())


@app.route('/rss', methods=['GET'])
def rss():
    rss_xml = render_template('rss.xml', items=get_blogs())
    response = make_response(rss_xml)
    response.headers['Content-Type'] = 'application/rss+xml'
    return response


if __name__ == '__main__':
    port = int(os.environ.get('PORT', PORT))
    app.run(host='0.0.0.0', port=port)
