from flask import Flask, render_template, flash, redirect, url_for
from flask_bootstrap import Bootstrap 
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import input_required, Email, Length 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, current_user, UserMixin, logout_user



app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql://root:admin@localhost/flaskp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'amogus'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#Formulário de login com flask-Wtforms
class loginForm(FlaskForm):
    username = StringField('Usuário', validators=[ input_required(), Length( min = 4, max = 15)])
    password = PasswordField('Senha', validators = [input_required(), Length( min = 6, max = 80 )])
    lembrar = BooleanField('Lembrar')  
    
#Formulário de cadastro com flask-Wtform
class registerForm(FlaskForm):
    email = StringField( 'E-mail' , validators=[ input_required(), Email(message='Email inválido'), Length(max= 64)])
    username = StringField('Usuário', validators=[ input_required(), Length( min = 4, max = 15)])
    password = PasswordField('Senha', validators = [input_required(), Length(max = 80)])
 
class Users(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username= db.Column(db.String(15),  unique= True)
    password= db.Column(db.String(100), unique= True) 
    email = db.Column(db.String(64), unique = True)

    def __init__(self, username, password, email):
        self.username =  username
        self.password = password
        self.email = email

@login_manager.user_loader
def user_loader(user_id):
    return Users.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/', methods = ['GET', 'POST'])
def login():
    form = loginForm()

    #Teste se está passando as informações coletadas no formulário
    if form.validate_on_submit():
        user = Users.query.filter_by(username = form.username.data).first()
        flash('Nome do usuário ou senha inválidos')
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.lembrar.data)
                return redirect(url_for('dashboard'))
        

    #     return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form = form)

@app.route('/sign_up/', methods = ['GET', 'POST'])
def sign_up():
    form = registerForm()

    if form.validate_on_submit():
        # criptografia de senhas
        pwhash = generate_password_hash(form.password.data, method='sha256')
        new = Users( username = form.username.data, password = pwhash, email = form.email.data  )
        db.session.add(new)
        db.session.commit()
        flash('Usuário cadastrado!')
        # teste
        # return '<h1>' + form.username.data + " " + form.password.data + " " + form.email.data + '</h1>'

    return render_template('sign_up.html', form = form)

@app.route('/dashboard/')
@login_required
def dashboard():
    return render_template('dashboard.html', name = current_user.username)

@app.route('/logoff/')
@login_required
def log_off():
    logout_user()
    return redirect(url_for('index'))

if __name__ in '__main__':
    app.run(debug = True)