from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class ServicoForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired(), Length(max=100)])
    descricao = TextAreaField('Descrição', validators=[DataRequired()])
    submit = SubmitField('Cadastrar Serviço')
    
class ProdutoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(max=100)])
    descricao = TextAreaField('Descrição', validators=[DataRequired()])
    preco = StringField('Preço', validators=[DataRequired()])
    submit = SubmitField('Cadastrar Produto')
    
class NoticiaForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired(), Length(max=100)])
    resumo = StringField('Resumo', validators=[DataRequired(), Length(max=200)])
    conteudo = TextAreaField('Conteúdo', validators=[DataRequired()])
    submit = SubmitField('Publicar Notícia')

