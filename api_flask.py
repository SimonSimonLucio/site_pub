from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean
from werkzeug.utils import secure_filename
from datetime import datetime
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///__fracigma_creds__.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '1234'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'fracigma'


class Solicitacoes(db.Model):
    __tablename__ = "solicitacoes"
    id = db.Column(db.Integer, primary_key=True)
    pedido = db.Column(db.String(250), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    nome = db.Column(db.String(250), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    sexo = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    telefone = db.Column(db.String(250), nullable=False)
    nacionalidade = db.Column(db.String(50), nullable=False)
    data_recebimento = db.Column(db.String(200), nullable=False)


class Topicos(db.Model):
    __tablename__ = "topicos"
    id = db.Column(db.Integer, primary_key=True)
    topico = db.Column(db.String(150), nullable=False)


class Publicacoes(db.Model):
    __tablename__ = "publicacoes"
    id = db.Column(db.Integer, primary_key=True)
    titulo1 = db.Column(db.String(150), nullable=False)
    conteudo1 = db.Column(db.Text, nullable=False)
    titulo2 = db.Column(db.String(150), nullable=False)
    conteudo2 = db.Column(db.Text, nullable=False)
    titulo3 = db.Column(db.String(150), nullable=False)
    conteudo3 = db.Column(db.Text, nullable=False)
    _date_ = db.Column(db.String(50), nullable=False)
    _image_1_ = db.Column(db.String(200), nullable=False)
    _image_2_ = db.Column(db.String(200), nullable=False)
    _image_3_ = db.Column(db.String(200), nullable=False)


class Credentials(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(70), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    key_remember = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Credentials {self.username}>'


class Messages(db.Model):
    __tablename__ = "messages_clinet"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phonenumber = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    _date_time_ = db.Column(db.String(50), nullable=False)


@app.route('/Assuntos/<id>')
def en(id):
    position = id.find('n-b')
    id = id[position+3:]
    print(id)
    topicos = Topicos.query.all()
    conteudo = Publicacoes.query.get(int(id))
    if conteudo:
        return render_template('inicio.html', topicos=topicos, conteudo=conteudo)
    else:
        return redirect(url_for('index'))


UPLOAD_FOLDER = 'static/images/'
ALLOWED_EXTENNSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENNSIONS


@app.route('/privado/deletar_sms/<id>', methods=['POST'])
@login_required
def deletar_sms(id):
    delde = Messages.query.get(int(id))
    db.session.delete(delde)
    db.session.commit()
    db.session.close()
    return redirect(url_for('not_know'))


@app.route('/Franklin_Gothic_Medium_Arial_Narrow_Arial_sans-serif')
def fracigma():
    return render_template('logar.html')


@login_manager.user_loader
def load_user(user_id=1):
    return Credentials.query.get(int(user_id))


@app.route('/principal')
def redir():
    return redirect(url_for('index'))


@app.route('/início')
def redir1():
    return redirect(url_for('index'))


@app.route('/inicio')
def redir2():
    return redirect(url_for('index'))


@app.route('/download_file')
def download_sgs():
    return send_file('static/files/fracigma-gs_instalador_x64_v1.1.exe', as_attachment=True)


@app.route('/')
def index():
    topicos = Topicos.query.all()
    conteudo = Publicacoes.query.get(1)
    return render_template('inicio.html', topicos=topicos, conteudo=conteudo)


@app.route('/Produtos/Pedir-Site')
def request_site():
    pedido = 'Pedido de Site'
    return render_template('pedir.html', pedido=pedido)


@app.route('/Produtos/Pedir-Bot-Automação')
def request_bot():
    pedido = 'Pedido de Bot/Automação'
    return render_template('pedir.html', pedido=pedido)


@app.route('/Produtos/Pedir-Sistema')
def request_oobjto():
    pedido = 'Pedido de Sistemas para Negócios'
    return render_template('pedir.html', pedido=pedido)


@app.route('/Produtos')
def download():
    return render_template('produtos.html')


@app.route('/Sobre')
def about_fracigma():
    return render_template('sobre.html')


@app.route('/Sobre/Políticas-Privacidades')
def politicas_privacidae():
    return render_template('sobre1.html')
    

@app.route('/Sobre/Nossos-Interesses')
def nossos_interesses():
    return render_template('sobre2.html')


@app.route('/Contato')
def contact():
    return render_template("contato.html")


@app.route('/request_service', methods=['POST'])
def enviar_pedidos():
    pedido = request.form['pedido']
    descricao = request.form['descricao']
    nome = request.form['nome']
    idade = request.form['idade']
    sexo = request.form['genero']
    email = request.form['email']
    telefone = request.form['telefone']
    nacionalidade = request.form['contry']
    data_recebimento = request.form['data_de_entrega']

    new_request = Solicitacoes(
        pedido=pedido,
        descricao=descricao,
        nome=nome,
        idade=idade,
        sexo=sexo,
        email=email,
        telefone=telefone,
        nacionalidade=nacionalidade,
        data_recebimento=data_recebimento
    )
    db.session.add(new_request)
    db.session.commit()
    db.session.close()
    return redirect(url_for('download'))


@app.route('/auth', methods=['GET', 'POST'])
def add_todo():
    if request.method == 'POST':# usuario1 = Credentials.query.filter_by(username='franciscosimaofelicianofranco_da_fracigma_lda@gmail.com').first()
        username = request.form['username']
        password = request.form['password']
        try:
            creds = Credentials.query.filter_by(username=username).first()
            user = f'{creds.username}'
            passw = f'{creds.password}'
            if creds and password == passw:
                login_user(creds)
                messages = Messages.query.all()
                return redirect(url_for('not_know'))
            else:
                return render_template('logar.html', error='Credenciais iválidas!')
        except AttributeError:
            return render_template('logar.html', error='Usuário não cadastrado!')


'''@app.route('/privado/solicitações/<id>')
@login_required
def solic(id):
    pedidos = Solicitacoes.query.all()
    pedido = Solicitacoes.query.get(id)
    return render_template('requests.html', pedidos=pedidos, pedido=pedido)'''


# else:
# return redirect(url_for('solicitacoes'))
@app.route('/solic/<id>')
@login_required
def eng(id):
    pedidos = Solicitacoes.query.all()
    pedido = Solicitacoes.query.get(int(id))
    if pedidos:
        return render_template('requests.html', pedidos=pedidos, pedido=pedido)
    else:
        return redirect(url_for('solicitacoes'))


@app.route('/privado/solicitações')
@login_required
def solicitacoes():
    pedidos = Solicitacoes.query.all()
    pedido = Solicitacoes.query.get(1)
    return render_template('requests.html', pedidos=pedidos, pedido=pedido)


@app.route('/logout')
@login_required
def logoout():
    logout_user()
    return redirect(url_for('fracigma'))


@app.route('/privado')
@login_required
def not_know():
    messages = Messages.query.all()
    return render_template('not_see.html', messages=messages)


@app.route('/privado/publicar')
@login_required
def publications():
    return render_template('publicar.html')


@app.route('/publicate', methods=['POST'])
@login_required
def publicate():
    _date_ = request.form['date_and_time']
    titulo1 = request.form['title1']
    titulo2 = request.form['title2']
    titulo3 = request.form['title3']
    conteudo1 = request.form['conteudo1']
    conteudo2 = request.form['conteudo2']
    conteudo3 = request.form['conteudo3']
    _image_1_ = request.files['primeira_imagem']
    _image_2_ = request.files['segunda_imagem']
    _image_3_ = request.files['terceira_imagem']

    if allowed_file(_image_1_.filename) and allowed_file(_image_1_.filename) and allowed_file(_image_1_.filename):
        filename1 = secure_filename(_image_1_.filename)
        filename2 = secure_filename(_image_2_.filename)
        filename3 = secure_filename(_image_3_.filename)
        _image_1_.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
        _image_2_.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
        _image_3_.save(os.path.join(app.config['UPLOAD_FOLDER'], filename3))

        public = Publicacoes(
            titulo1=titulo1,
            conteudo1=conteudo1,
            titulo2=titulo2,
            conteudo2=conteudo2,
            titulo3=titulo3,
            conteudo3=conteudo3,
            _date_=_date_,
            _image_1_=os.path.join(app.config['UPLOAD_FOLDER'], filename1),
            _image_2_=os.path.join(app.config['UPLOAD_FOLDER'], filename2),
            _image_3_=os.path.join(app.config['UPLOAD_FOLDER'], filename3)

    )
        db.session.add(public)
        db.session.commit()
        db.session.close()

    topico = request.form['topico']
    topic = Topicos(topico=topico)
    db.session.add(topic)
    db.session.commit()
    db.session.close()
    return redirect(url_for('not_know'))


@app.route('/message', methods=['POST'])
def received_message():
    name = request.form['fullname']
    email = request.form['email']
    phonenumber = request.form['phonenumber']
    message = request.form['message']
    data = datetime.now().date()
    hora = datetime.now().hour
    minute = datetime.now().minute
    _date_time_ = f"{data} {hora}:{minute}"
    save_message = Messages(name=name, email=email, phonenumber=phonenumber, message=message, _date_time_=_date_time_)
    db.session.add(save_message)
    db.session.commit()
    db.session.close()
    # print(f"Nome: {name}\nEmail: {email}\nTelefone: {phonenumber}\nMensagem:\n{message}"
    # )
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    