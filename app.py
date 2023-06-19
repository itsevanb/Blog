from flask import Flask, render_template, request, redirect, url_for
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

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        #get data from form
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')
        #save data to json file then load data to index page
        try:
            with open('data.json', 'r') as f:
                data = json.load(f)
        except Exception as e:
            print(f"Error reading file: {e}")
            data = []

        new_data = {'id': len(data) + 1, 'author': author, 'title': title, 'content': content}
        data.append(new_data)
        try:
            with open('data.json', 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error writing file: {e}")
            return "Error saving data"

        return redirect(url_for('index'))
    
    
    return render_template('add.html')


if __name__ == '__main__':
    app.run()