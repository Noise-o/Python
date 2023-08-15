from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import os  

# iNIT APP
app = Flask(__name__)
# basedir = os.path.abspath(os.path.dirname(__file__))
# DATABASE 
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql://root:admin@localhost/flaskp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'amogus'
# INIT DB
db = SQLAlchemy(app)
# INIT SCHEME
ma = Marshmallow(app)

# CLASS MODEL
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    produto= db.Column(db.String,  unique= True)
    desc = db.Column(db.String)
    preco= db.Column(db.Float) 
    qtd = db.Column(db.Integer)

    def __init__(self, id, produto, preco, qtd):
         self.id = id
         self.produto = produto
         self.preco = preco
         self.qtf = qtd

# PRODUTO SCHEMA
class ProdutoSchema(ma.Schema):
     class Meta:
        fields = ('id', 'produto', 'desc', 'preco', 'qtd')

# INIT SCHEMA
produto_schema = ProdutoSchema( )
produtos_schema = ProdutoSchema(many=True, strict = True)

# ROUTES
@app.route('/', methods = ['GET'])
def index():
        return jsonify({'msg':'Hello world'})

# RUN SERVER
if __name__ in ('__main__'):
    app.run(host='127.0.0.1', port=8000, debug=True)
 