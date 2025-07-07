from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, SubmitField, PasswordField, MultipleFileField
from wtforms.validators import DataRequired, Length, NumberRange
from flask_wtf.file import FileAllowed, FileField



class LoginForm(FlaskForm):
    usuario = StringField('Usuário', validators=[DataRequired(), Length(max=50)])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6, max=100)])
    submit = SubmitField('Entrar')

class ServicoForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired(), Length(max=100)])
    descricao = TextAreaField('Descrição', validators=[DataRequired()])
    submit = SubmitField('Cadastrar Serviço')
    
class ProdutoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    descricao = TextAreaField('Descrição', validators=[DataRequired()])
    preco = DecimalField('Preço', validators=[DataRequired(), NumberRange(min=0)])
    
    imagens = MultipleFileField('Imagens', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Apenas arquivos de imagem são permitidos.')
    ])
    
    submit = SubmitField('Cadastrar')

class NoticiaForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired(), Length(max=100)])
    resumo = StringField('Resumo', validators=[DataRequired(), Length(max=200)])
    conteudo = TextAreaField('Conteúdo', validators=[DataRequired()])
    submit = SubmitField('Publicar Notícia')

