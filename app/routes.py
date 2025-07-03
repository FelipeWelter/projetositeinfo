import os
import feedparser
from flask import current_app, Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.utils import secure_filename
from app.models import Produto, Servico, Noticia
from app.forms import ProdutoForm, ServicoForm, NoticiaForm
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/admin')
def admin():
    return render_template('admin.html')

@main.route('/services')
def services():
    servicos = Servico.query.order_by(Servico.data_criacao.desc()).all()
    return render_template('services.html', servicos=servicos)

@main.route('/add-service', methods=['GET', 'POST'])
def add_service():
    form = ServicoForm()
    if form.validate_on_submit():
        novo = Servico(titulo=form.titulo.data, descricao=form.descricao.data)
        db.session.add(novo)
        db.session.commit()
        flash('Serviço cadastrado com sucesso!', 'success')
        return redirect(url_for('main.services'))
    return render_template('add_service.html', form=form)

@main.route('/products')
def products():
    produtos = Produto.query.order_by(Produto.data_cadastro.desc()).all()
    return render_template('products.html', produtos=produtos)

@main.route('/add-product', methods=['GET', 'POST'])
def add_product():
    form = ProdutoForm()
    if form.validate_on_submit():
        filename = None
        if form.imagem.data:
            filename = secure_filename(form.imagem.data.filename)
            caminho = os.path.join(current_app.root_path, 'static/uploads', filename)
            form.imagem.data.save(caminho)
        produto = Produto(
            nome=form.nome.data,
            descricao=form.descricao.data,
            preco=float(form.preco.data),
            imagem=filename
        )
        db.session.add(produto)
        db.session.commit()
        flash('Produto cadastrado com sucesso!', 'success')
        return redirect(url_for('main.products'))
    return render_template('add_product.html', form=form)

@main.route('/edit-product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    produto = Produto.query.get_or_404(id)
    form = ProdutoForm(obj=produto)
    if form.validate_on_submit():
        produto.nome = form.nome.data
        produto.descricao = form.descricao.data
        produto.preco = float(form.preco.data)
        if form.imagem.data:
            filename = secure_filename(form.imagem.data.filename)
            caminho = os.path.join(current_app.root_path, 'static/uploads', filename)
            form.imagem.data.save(caminho)
            produto.imagem = filename
        db.session.commit()
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('main.products'))
    return render_template('add_product.html', form=form)

@main.route('/delete-product/<int:id>')
def delete_product(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    flash('Produto removido com sucesso!', 'success')
    return redirect(url_for('main.products'))

@main.route('/news')
def news():
    feed = feedparser.parse('https://www.tecmundo.com.br/rss')
    noticias = feed.entries[:5]
    return render_template('news.html', noticias=noticias)

@main.route('/add-news', methods=['GET', 'POST'])
def add_news():
    form = NoticiaForm()
    if form.validate_on_submit():
        noticia = Noticia(
            titulo=form.titulo.data,
            resumo=form.resumo.data,
            conteudo=form.conteudo.data
        )
        db.session.add(noticia)
        db.session.commit()
        flash('Notícia publicada com sucesso!', 'success')
        return redirect(url_for('main.news'))
    return render_template('add_news.html', form=form)

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        nome = request.form['nome']
        mensagem = request.form['mensagem']
        print(f'Nova mensagem de {nome}: {mensagem}')
        flash('Mensagem enviada com sucesso!', 'success')
        return redirect(url_for('main.contact'))
    return render_template('contact.html')

@main.route('/buscar', methods=['GET'])
def buscar():
    termo = request.args.get('q', '')
    resultados = Produto.query.filter(Produto.nome.ilike(f'%{termo}%')).all()
    return render_template('search.html', termo=termo, resultados=resultados)
