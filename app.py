import os
from flask import Flask, render_template

app = Flask(__name__)


def get_skills():
    file = open("skills.txt", "r")
    skills = file.readlines()
    file.close()
    return skills


@app.route('/')
def home():
    return render_template('home.html', skills=get_skills())


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)