from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET'])
def greet():
    return "Hello, welcome to my Flask app!"

if __name__ == '__main__':
    app.run(port=7000)
