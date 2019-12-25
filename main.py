from flask import Flask, g
from user import app_user
from file import app_file

app = Flask(__name__)

app.register_blueprint(app_user)
app.register_blueprint(app_file)


@app.route('/')
def index():
    return 'hello, world'

if __name__ == '__main__':
    print(app.url_map)
    app.run(host='0.0.0.0', port=8080)
