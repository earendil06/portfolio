import os

import xmltodict as xmltodict
from flask import Flask, render_template, make_response

app = Flask(__name__)


def get_file_content(path):
    file = open(path, "r")
    lines = file.readlines()
    file.close()
    return "".join(lines)


def get_skills():
    return get_file_content("skills.txt").split('\n')


def get_rss_items():
    directory = "rss_items"
    contents = [get_file_content(directory + "/" + f) for f in os.listdir(directory) if f.endswith(".xml")]
    return [xmltodict.parse(s) for s in contents]


@app.route('/')
def home():
    return render_template('home.html', skills=get_skills())


@app.route('/rss')
def feed():
    rss_xml = render_template('rss.xml', items=get_rss_items())
    response = make_response(rss_xml)
    response.headers['Content-Type'] = 'application/rss+xml'
    return response


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
