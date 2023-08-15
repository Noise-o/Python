from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy  
# import mysql.connector

# # INICIA A CONEXÂO
# mybd = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="admin",
#     database="dbtest",
# )

# cursor = mybd.cursor()
# nome_produto = "produto 1"
# valor = "100"

# # CREATE
# comandos = (
#     f'INSERT INTO vendas (nome_produto, valor) VALUES ("{nome_produto}", {valor}) '
# )

# cursor.execute(comandos)
# mybd.commit()  # editao banco de dados

# # READ
# comandos = f"SELECT * FROM dbtest.vendas"
# cursor.execute(comandos)
# cursor.fetchall()  # leitura do banco de dados

# # UPDATE
# comandos = f'UPDATE vendas SET valor = {valor} WHERE nome_produto = "{nome_produto}"'
# cursor.execute(comandos))
# mybd.commit()

# # DELETE(comandos) = f"DELETE FROM vendas * WHERE nome_produto = {nome_produto}"
# cursor.execute(comandos)
# mybd.commit()

# # FECHA A CONEXÂO
# cursor.close()


# Deve ter em todo app em flask
app = Flask(__name__)
# mysql://usuário:senha@localhost/banco
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql://root:admin@localhost/flaskp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'amogus'
db = SQLAlchemy(app)
# CRIA UMA TABELA (pode ser criada no próprio mysql)
class Clientes(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome =  db.Column(db.String(100), nullable = False)
    email =  db.Column(db.String(100), nullable = False)
    fone =  db.Column(db.String(15), nullable = False)

    def __init__(self, nome, email, fone):
        self.nome = nome
        self.email = email
        self.fone = fone  
        
# pip install mysqlclient para usar o shell
# Digitar no shell :
#     from app import db 
#     db.create_all()

# Para inserir elementos no db
# >>> b = pessoas(nome =  'Luis', email = 'Ndynoise00@gmail.com', fone = "(38)99999-9999") 
# >>> db.session.add(b) 
# >>> db.session.commit()

# Para listar os elementos no db 
# >>> pessoa_data = pessoas.query.all()
# >>> pessoa_data
# Para listar de acordo com a coluna
# >>> for pessoas in pessoa_data:
# ...     print(pessoas.nome)
# ... 

# Para atualizar dados do db de acordo com a coluna 
# >>> upd = pessoas.query.filter_by(id=1).first()
# >>> upd
# <pessoas 1>
# >>> upd.nome= 'Atualizado'
# >>> db.session.commit()
# >>> 

# Para deletar dados no db de acordo com a coluna
# >>> delete=pessoas.query.filter_by(id=1).first()      
# >>> delete
# <pessoas 1>
# >>> db.session.delete(delete)
# >>> db.session.commit()
# >>> 


# Define o caminho da página
@app.route("/")
# Define o que será feito na página
def Index():
    pessoas = Clientes.query.all()
    return render_template("index.html", pessoas = pessoas)

# Adicionando dados
@app.route('/add/',methods = ['POST'] )
def add_cliente():
    if request.method == 'POST':
        add = Clientes(
            nome = request.form.get('nome'),
            email = request.form.get('email'),
            fone= request.form.get('fone')
        )
        db.session.add(add)
        # Adicionando Flash Messages 
        flash ("O cliente foi adicionado")
        db.session.commit()
        return redirect(url_for('Index'))
    


# Atualizando Dados
@app.route('/update/', methods = ['POST'])
def update():
    if request.method == 'POST':
        upd_data = Clientes.query.get(request.form.get('id'))

        upd_data.nome = request.form['nome']
        upd_data.email = request.form['email']       
        upd_data.fone = request.form['fone']

        flash ("O Cliente foi editado!")
        db.session.commit()
        return redirect(url_for('Index'))
# Apagando dado
@app.route('/delete/<id>/', methods =['POST', 'GET'] )
def delete(id):
    delete_data = Clientes.query.get(id)
    db.session.delete(delete_data)
    db.session.commit()
    flash('O cliente foi apagado.')
    return redirect(url_for('Index'))  
            


# permite que o site rodde de forma que não seja preciso reativar o código a cada alteração
if __name__ in "__main__":
    app.run(debug=True)
