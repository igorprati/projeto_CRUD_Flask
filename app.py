from flask import (Flask, render_template, Blueprint, request)
from flask_sqlalchemy import SQLAlchemy
from datetime import date



app = Flask(__name__)
bp = Blueprint('app', __name__)

# ckeditor

# CONECTAR AO BANCO DE DADOS
user = 'hhwggbrf'
password = 'c6REDmJm_Zj0PCXVcs6G5NMtQ3OyZnGf'
host = 'tuffi.db.elephantsql.com'
database = 'hhwggbrf'

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# INSTANCIAR VARIÁVEL NO SQLALCHEMY
db = SQLAlchemy(app)

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # data_post = db.Column(db.Date, nullable=False)
    titulo = db.Column(db.String(255), nullable=False)
    assunto = db.Column(db.String(255), nullable=False)
    imagem_url = db.Column(db.String(255), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    
    
    def __init__(self, titulo, assunto, imagem_url, conteudo): # PRECISA SER NA ORDEM DO FORMULÁRIO
        self.titulo = titulo
        self.assunto = assunto
        self.imagem_url = imagem_url
        self.conteudo = conteudo
        

    @staticmethod
    def todos_posts():
        return Posts.query.order_by(Posts.id.desc()).all()

    @staticmethod
    def tres_posts():
        return Posts.query.order_by(Posts.id.desc()).limit(3).all()

    @staticmethod
    def post_selecionado(post_id):
        return Posts.query.get(post_id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def deletar(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, new_data):
        self.titulo = new_data.titulo
        self.assunto = new_data.assunto
        self.imagem_url = new_data.imagem_url
        self.conteudo = new_data.conteudo
        self.save()


@bp.route('/')
def index():
    tres_posts = Posts.tres_posts()
    posts = Posts.todos_posts()

    if len(posts) == 0:
        posts = 0
    else:
        posts = Posts.todos_posts()
    
    return render_template(
        'index.html',
        tresPosts = tres_posts,
        posts = posts
    )

@bp.route('/blog')
def blog():
    posts = Posts.todos_posts()
    data_atual = date.today()

    return render_template(
        'blog.html',
        todosPosts = posts,
        data_atual = data_atual
    )


@bp.route('/post/<post_id>')
def post_individual(post_id):
    post = Posts.post_selecionado(post_id)

    return render_template(
        'post.html',
        post = post
    )

@bp.route('/create', methods=('GET', 'POST'))
def criar_post():
    id_atribuido = None

    if request.method == 'POST':
        form = request.form
        post = Posts(form['titulo'], form['assunto'], form['imagem_url'], form['conteudo'])
        post.save()
        id_atribuido = post.id

    return render_template(
        'create.html',
        id_atribuido = id_atribuido,
    )

@bp.route('/update/<post_id>', methods=('GET', 'POST'))
def update(post_id):
    sucesso = None
    post = Posts.post_selecionado(post_id)

    if request.method == 'POST':
        form = request.form

        new_data = Posts(form['titulo'], form['assunto'], form['imagem_url'], form['conteudo'])

        post.update(new_data)
        sucesso = True
        

    return render_template(
        'update.html',
        post = post,
        sucesso = sucesso
    )

@bp.route('/deletar/<post_id>', methods=('GET', 'POST'))
def deletar(post_id):
  sucesso = None
  post = Posts.post_selecionado(post_id)

  if request.method == 'POST':   
    post.deletar()
    sucesso = True

  return render_template(
      'deletar.html',
      post = post,
      sucesso = sucesso
    )

    

app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=True)


