CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE smtp_settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    smtp_server VARCHAR(100) NOT NULL,
    smtp_port INT NOT NULL,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE sent_emails (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    recipient_email VARCHAR(100) NOT NULL,
    subject VARCHAR(255) NOT NULL,
    body TEXT NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);


class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'mysql://username:password@localhost/mail_app_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    smtp_settings = db.relationship('SMTPSettings', backref='user', uselist=False)
    sent_emails = db.relationship('SentEmail', backref='user', lazy=True)

class SMTPSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    smtp_server = db.Column(db.String(100), nullable=False)
    smtp_port = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)

class SentEmail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SMTPSettingsForm(FlaskForm):
    smtp_server = StringField('SMTP Server', validators=[DataRequired()])
    smtp_port = StringField('SMTP Port', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Save Settings')

class SendEmailForm(FlaskForm):
    recipient_email = StringField('Recipient Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired()])
    body = StringField('Body', validators=[DataRequired()])
    submit = SubmitField('Send Email')


from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, SMTPSettingsForm, SendEmailForm
from models import db, User, SMTPSettings, SentEmail
from config import Config
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    smtp_settings_form = SMTPSettingsForm()
    send_email_form = SendEmailForm()

    if smtp_settings_form.validate_on_submit():
        smtp_settings = SMTPSettings.query.filter_by(user_id=current_user.id).first()
        if not smtp_settings:
            smtp_settings = SMTPSettings()
            smtp_settings.user_id = current_user.id
        smtp_settings.smtp_server = smtp_settings_form.smtp_server.data
        smtp_settings.smtp_port = smtp_settings_form.smtp_port.data
        smtp_settings.username = smtp_settings_form.username.data
        smtp_settings.password = smtp_settings_form.password.data
        db.session.add(smtp_settings)
        db.session.commit()
        flash('SMTP settings saved successfully', 'success')
        return redirect(url_for('dashboard'))

    if send_email_form.validate_on_submit():
        smtp_settings = SMTPSettings.query.filter_by(user_id=current_user.id).first()
        if smtp_settings:
            try:
                server = smtplib.SMTP(smtp_settings.smtp_server, smtp_settings.smtp_port)
                server.starttls()
                server.login(smtp_settings.username, smtp_settings.password)

                msg = MIMEMultipart()
                msg['From'] = smtp_settings.username
                msg['To'] = send_email_form.recipient_email.data
                msg['Subject'] = send_email_form.subject.data
                msg.attach(MIMEText(send_email_form.body.data, 'plain'))

                server.sendmail(smtp_settings.username, send_email_form.recipient_email.data, msg.as_string())
                server.quit()

                sent_email = SentEmail()
                sent_email.user_id = current_user.id
                sent_email.recipient_email = send_email_form.recipient_email.data
                sent_email.subject = send_email_form.subject.data
                sent_email.body = send_email_form.body.data
                db.session.add(sent_email)
                db.session.commit()

                flash('Email sent successfully', 'success')
                return redirect(url_for('dashboard'))
            except Exception as e:
                flash('An error occurred while sending email: ' + str(e), 'error')
        else:
            flash('SMTP settings not configured', 'error')

    return render_template('dashboard.html', smtp_settings_form=smtp_settings_form, send_email_form=send_email_form)

@app.route('/sent_emails')
@login_required
def sent_emails():
    sent_emails = SentEmail.query.filter_by(user_id=current_user.id).order_by(SentEmail.sent_at.desc()).all()
    return render_template('sent_emails.html', sent_emails=sent_emails)

if __name__ == '__main__':
    app.run(debug=True)
