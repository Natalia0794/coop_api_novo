from tkinter import E
from flask import Flask, Response, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:myRoot-1234@localhost/coop-studios'

db = SQLAlchemy(app)

class Jogos(db.Model):
    codigo = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(255))
    descricao = db.Column(db.String(255))
    valor = db.Column(db.String(10))
    link = db.Column(db.String(255))

    def to_json(self):
        return {"codigo": self.codigo, 
                "nome": self.nome, 
                "descricao": self.descricao,
                "valor": self.valor, 
                "link": self.link}

class Cadastro(db.Model):
    codigo = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    cpf = db.Column(db.String(11))
    rua = db.Column(db.String(255))
    numero = db.Column(db.Integer)
    cep = db.Column(db.String(12))
    bairro = db.Column(db.String(255))
    cidade = db.Column(db.String(255))
    uf = db.Column(db.String(2))
    referencia = db.Column(db.String(255))
    ddd = db.Column(db.Integer)
    telefone = db.Column(db.String(9))
    password = db.Column(db.String(255), nullable=False)

    def to_json(self):
        return {"mensagem": "Usuario cadastrado / atualizado com sucesso"}



@app.route("/produto/<codigo>", methods=['GET'])
def seleciona_produto(codigo):
    produto_objeto = Jogos.query.filter_by(codigo=codigo).first()
    produto_json = produto_objeto.to_json()

    return gera_response(200, "jogo", produto_json, "ok")



@app.route("/cadastro", methods=['POST'])
def cadastro():
    body = request.get_json()

    try:
        cadastro = Cadastro(codigo=body["codigo"], nome=body["nome"], email=body["email"], password=body["password"])
        db.session.add(cadastro)
        db.session.commit()
        return gera_response(201, "cadastro", cadastro.to_json(), "Sucesso")
    except Exception as e:
        print(e)
        return gera_response(400, "cadastro", {}, "Erro ao cadastrar usuário")



@app.route("/cadastro/<codigo>", methods=['PUT'])
def atualiza_cadastro(codigo):
    cadastro_objeto = Cadastro.query.filter_by(codigo=codigo).first()
    body = request.get_json()

    try:
        if("nome" in body):
            cadastro_objeto.nome = body["nome"]
        if("email" in body):
            cadastro_objeto.email = body["email"]
        if("cpf" in body):
            cadastro_objeto.cpf = body["cpf"]
        if("rua" in body):
            cadastro_objeto.rua = body["rua"]
        if("numero" in body):
            cadastro_objeto.numero = body["numero"]
        if("cep" in body):
            cadastro_objeto.cep = body["cep"]
        if("bairro" in body):
            cadastro_objeto.bairro = body["bairro"]
        if("cidade" in body):
            cadastro_objeto.cidade = body["cidade"]
        if("uf" in body):
            cadastro_objeto.uf = body["uf"]
        if("referencia" in body):
            cadastro_objeto.referencia = body["referencia"]
        if("ddd" in body):
            cadastro_objeto.ddd = body["ddd"]
        if("telefone" in body):
            cadastro_objeto.telefone = body["telefone"]
        if("password" in body):
            cadastro_objeto.password = body["password"]
        
        db.session.add(cadastro_objeto)
        db.session.commit()

        return gera_response(201, "cadastro", cadastro_objeto.to_json(), "Sucesso")
    
    except Exception as e:
        print(e)
        return gera_response(400, "cadastro", {}, "Erro ao buscar usuário ou usuario não cadastrado")



@app.route("/login", methods=['POST'])
def login():
    body = request.get_json()
    login = Cadastro.query.filter_by(email=body['email']).first()


    if(body['email'] == login.email \
        and body["password"] == login.password):
        return gera_response(200, "login", {}, "Login efetuado com sucesso!")
    else:
        return gera_response(400, "login", {}, "Dados inválidos!")



def gera_response(status, nome_do_conteudo, conteudo, mensagem):
    body = {}
    body[nome_do_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json",)

app.run()