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
        {}
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

        new_data = {'id': len(data) + 1, 'author': author, 'title': title, 'content': content, 'like': 0}
        data.append(new_data)
        
        try:
            with open('data.json', 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error writing file: {e}")
            return "Error saving data"

        return redirect(url_for('index'))
    
    
    return render_template('add.html')

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading file: {e}")
        data = []

    data = [post for post in data if post['id'] != id]

    try:
        with open('data.json', 'w') as f:
            json.dump(data, f)
    except Exception as e:
        print(f"Error writing file: {e}")
        return "Error saving data"
    
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading file: {e}")
    
    post = next((post for post in data if post['id'] == id), None)

    if request.method == 'POST':
        #update the post in the JSON file
        #redirect back to index page
        post_update = request.form
        post['title'] = post_update['title']
        post['author'] = post_update['author']
        post['content'] = post_update['content']

        try:
            with open('data.json', 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error writing file: {e}")
            return "Error saving data"
        return redirect(url_for('index'))

    
    return render_template('update.html', post=post)

@app.route('/like/<int:id>', methods=['POST'])
def like(id):
    #adds like button to post
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading file: {e}")
    
    post = next((post for post in data if post['id'] == id), None)

    if post:
        if 'likes' not in post:
            post['likes'] = 0 
        post['likes'] += 1

        try:
            with open('data.json', 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error writing file: {e}")
            return "Error saving data"
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()