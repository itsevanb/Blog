from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/')
#load data from json file
def index():
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading file: {e}")
        data = []

    return render_template('index.html', posts=data)

@app.route('/save')
def save_data():
    data = [
        {'id': 1, 'author': "John Doe", 'title': "First Post", 'content': "This is my first post"},
        {'id': 2, 'author': "Jane Doe", 'title': "Second Post", 'content': "This is my second post"},
    ]

    try:
        with open('data.json', 'w') as f:
            json.dump(data, f)
    except Exception as e:
        print(f"Error writing file: {e}")
        return "Error saving data"
        

if __name__ == '__main__':
    app.run()