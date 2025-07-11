from . import db
from datetime import datetime

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Admin {self.usuario}>'


class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

    imagens = db.relationship('ImagemProduto', back_populates='produto', cascade='all, delete-orphan')

class ImagemProduto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_arquivo = db.Column(db.String(100), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)

    produto = db.relationship('Produto', back_populates='imagens')


class Servico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

class Noticia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    resumo = db.Column(db.String(200), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    data_publicacao = db.Column(db.DateTime, default=datetime.utcnow)


class Post(db.Model):  # Notícias ou artigos
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    autor = db.Column(db.String(50), default="Admin")
    data_postagem = db.Column(db.DateTime, default=datetime.utcnow)
