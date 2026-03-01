from flask import Blueprint, render_template, request, redirect, url_for, session, flash

auth = Blueprint('auth', __name__)


USERS = {
    'admin': 'admin123',
    'prof':  'prof123',
}



@auth.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('auth.home'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
    
        print(f">>> username reçu : '{username}'")
        print(f">>> password reçu : '{password}'")
        print(f">>> USERS : {USERS}")

        if username in USERS and USERS[username] == password:
            session['user'] = username
            flash(f'Bienvenue, {username} !', 'success')
            return redirect(url_for('auth.home'))
        else:
            flash("Nom d'utilisateur ou mot de passe incorrect.", 'danger')

    return render_template('auth/login.html')



@auth.route('/logout')
def logout():
    username = session.pop('user', None)
    if username:
        flash(f'Au revoir, {username} ! Vous avez été déconnecté.', 'info')
    return redirect(url_for('auth.login'))




@auth.route('/')
def home():
    return render_template('auth/home.html')
