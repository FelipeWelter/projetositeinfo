import os
import feedparser
from flask import current_app, Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.utils import secure_filename
from app.models import Produto, Servico, Noticia
from app.forms import ProdutoForm, ServicoForm, NoticiaForm
from . import db
from flask import session, send_from_directory
from app.forms import LoginForm
from app.models import Admin
from werkzeug.security import check_password_hash
from app.models import ImagemProduto
from flask_login import login_required

main = Blueprint('main', __name__)

def login_required(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'admin_id' not in session:
            return redirect(url_for('main.login'))
        return func(*args, **kwargs)
    return wrapper


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(usuario=form.usuario.data).first()
        if admin and check_password_hash(admin.senha, form.senha.data):
            session['admin_id'] = admin.id
            return redirect(url_for('main.admin'))
        flash('Usuário ou senha inválidos.', 'danger')
    return render_template('login.html', form=form)

@main.route('/logout')
def logout():
    session.clear()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('main.login'))

@main.route('/admin')
@login_required
def admin():
    if 'admin_id' not in session:
        return redirect(url_for('main.login'))
    
    admin = Admin.query.get(session['admin_id'])
    if not admin:
        flash('Administrador não encontrado.', 'danger')
        return redirect(url_for('main.login'))

    produtos = Produto.query.order_by(Produto.data_cadastro.desc()).all()
    servicos = Servico.query.order_by(Servico.data_criacao.desc()).all()
    noticias = Noticia.query.order_by(Noticia.data_publicacao.desc()).all()

    return render_template('admin.html', admin=admin, produtos=produtos, servicos=servicos, noticias=noticias)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/admin-services')
@login_required
def admin_services():
    servicos = Servico.query.order_by(Servico.data_criacao.desc()).all()
    return render_template('admin_services.html', servicos=servicos)

@main.route('/services')
def services():
    servicos = Servico.query.order_by(Servico.data_criacao.desc()).all()
    return render_template('services.html', servicos=servicos)

@main.route('/add-service', methods=['GET', 'POST'])
@login_required
def add_service():
    form = ServicoForm()
    if form.validate_on_submit():
        novo = Servico(titulo=form.titulo.data, descricao=form.descricao.data)
        db.session.add(novo)
        db.session.commit()
        return redirect(url_for('main.admin'))
    return render_template('add_service.html', form=form)








@main.route('/products')
def products():
    produtos = Produto.query.order_by(Produto.data_cadastro.desc()).all()
    return render_template('products.html', produtos=produtos)

@main.route('/admin-products')
@login_required
def admin_products():
    produtos = Produto.query.order_by(Produto.data_cadastro.desc()).all()
    return render_template('admin_products.html', produtos=produtos)

@main.route('/add-product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProdutoForm()
    if form.validate_on_submit():
        produto = Produto(
            nome=form.nome.data,
            descricao=form.descricao.data,
            preco=float(form.preco.data)
        )
        db.session.add(produto)
        db.session.flush()  # para pegar produto.id antes do commit

        # Salva as imagens (se houver)
        for imagem in form.imagens.data:
            if imagem and imagem.filename:
                filename = secure_filename(imagem.filename)
                caminho = os.path.join(current_app.root_path, 'static/uploads', filename)
                imagem.save(caminho)

                nova_imagem = ImagemProduto(nome_arquivo=filename, produto_id=produto.id)
                db.session.add(nova_imagem)
        db.session.commit()
        return redirect(url_for('main.admin'))
    return render_template('add_product.html', form=form)



@main.route('/edit-product/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    produto = Produto.query.get_or_404(id)
    form = ProdutoForm(obj=produto)

    if form.validate_on_submit():
        produto.nome = form.nome.data
        produto.descricao = form.descricao.data
        produto.preco = float(form.preco.data)

        # Adiciona novas imagens, se houver
        for imagem in form.imagens.data:
            if imagem and imagem.filename:
                filename = secure_filename(imagem.filename)
                caminho = os.path.join(current_app.root_path, 'static/uploads', filename)
                imagem.save(caminho)

                nova_imagem = ImagemProduto(nome_arquivo=filename, produto_id=produto.id)
                db.session.add(nova_imagem)

        db.session.commit()
        return redirect(url_for('main.admin_products'))

    return render_template('add_product.html', form=form, produto=produto)


@main.route('/delete-product/<int:id>')
@login_required
def delete_product(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    return redirect(url_for('main.admin_products'))

@main.route('/news')
def news():
    feed = feedparser.parse('https://www.tecmundo.com.br/rss')
    noticias = feed.entries[:5]
    return render_template('news.html', noticias=noticias)

@main.route('/add-news', methods=['GET', 'POST'])
@login_required
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
        return redirect(url_for('main.news'))
    return render_template('add_news.html', form=form)

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        nome = request.form['nome']
        mensagem = request.form['mensagem']
        print(f'Nova mensagem de {nome}: {mensagem}')
        return redirect(url_for('main.contact'))
    return render_template('contact.html')

@main.route('/buscar', methods=['GET'])
def buscar():
    termo = request.args.get('q', '')
    resultados = Produto.query.filter(Produto.nome.ilike(f'%{termo}%')).all()
    return render_template('search.html', termo=termo, resultados=resultados)

