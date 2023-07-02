from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['user_database']
collection = db['users']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Enregistrement de l'utilisateur dans la base de données
        user = {'username': username, 'password': password}
        collection.insert_one(user)
        return redirect('/login')
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Vérification des informations d'identification dans la base de données
        user = collection.find_one({'username': username, 'password': password})
        if user:
            return redirect('/profile')
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']
        # Mise à jour des informations de profil dans la base de données
        collection.update_one({}, {'$set': {'username': new_username, 'password': new_password}})
        return redirect('/profile')
    user = collection.find_one()
    return render_template('profile.html', user=user)

@app.route('/delete', methods=['POST'])
def delete():
    # Suppression du compte utilisateur de la base de données
    collection.delete_one({})
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
