'''from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///__fracigma_creds__.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Credentials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(70), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    key_remember = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Credencials {self.username}>"



@app.route('/')
def index():
    with app.app_context():
        # administrator = Credentials(username="franciscosimaofelicianofranco_da_fracigma_lda@gmail.com", password="__happyy_19_years__", key_remember="pouco_tempo_depois...")
        # db.session.add(administrator)
        # db.session.commit()
        usuario1 = Credentials.query.filter_by(username='franciscosimaofelicianofranco_da_fracigma_lda@gmail.com').first()
        admin = usuario1.username
        # for user in creds:
        #    admin += f'Id: {user.id} Usuario: {user.username} Senha: {user.password} Forgot_pass: {user.key_remember}'
    return f'{usuario1.password}'


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)'''

from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///seu_banco_de_dados.db'
db = SQLAlchemy(app)


class Imagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    caminho = db.Column(db.String(200))

    def __repr__(self):
        return f"Imagem('{self.nome}', '{self.caminho}')"


UPLOAD_FOLDER = 'caminho/para/a/pasta/das/imagens'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            nova_imagem = Imagem(nome=filename, caminho=os.path.join(app.config['UPLOAD_FOLDER'], filename))
            db.session.add(nova_imagem)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('upload.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


