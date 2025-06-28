from app.models import Produto
from app.forms import ProdutoForm
from flask import redirect, url_for, flash
from .forms import ServicoForm
from .models import Servico
from flask import Blueprint, render_template
from .models import Servico  # importa o modelo
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/services')
def services():
    servicos = Servico.query.order_by(Servico.data_criacao.desc()).all()
    return render_template('services.html', servicos=servicos)
@main.route('/news')
def news():
    return render_template('news.html')
@main.route('/contact')
def contact():
    return render_template('contact.html')
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

















































































