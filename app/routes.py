from flask import Blueprint, render_template, redirect, url_for, flash
from . import db
from app.models import Produto, Servico, Noticia
from app.forms import ProdutoForm, ServicoForm, NoticiaForm

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

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
        produto = Produto(
            nome=form.nome.data,
            descricao=form.descricao.data,
            preco=float(form.preco.data)
        )
        db.session.add(produto)
        db.session.commit()
        flash('Produto cadastrado com sucesso!', 'success')
        return redirect(url_for('main.products'))
    return render_template('add_product.html', form=form)

@main.route('/news')
def news():
    noticias = Noticia.query.order_by(Noticia.data_publicacao.desc()).all()
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

@main.route('/contact')
def contact():
    return render_template('contact.html')

















































































