from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp, ValidationError, Optional
from app.models import User


# 登入表單
class LoginForm(FlaskForm):
    username = StringField('帳號', validators=[DataRequired()])
    password = PasswordField('密碼', validators=[DataRequired()])
    remember = BooleanField('記住我')
    submit = SubmitField('登入')


# 註冊表單
class RegisterForm(FlaskForm):
    username = StringField('帳號', validators=[DataRequired(),
        Regexp('^[A-Za-z][A-Za-z0-9]*$',
               message='帳號格式：大寫或小寫英文字母開頭，可包括數字，不含特殊符號'),
        Length(3, 15, message='帳號長度為3至15字元')])
    password = PasswordField('密碼', validators=[DataRequired(),
        EqualTo('password2', message='輸入的密碼不一致'),
        Length(6, 20, message='密碼長度為6至20字元')])
    password2 = PasswordField('再次確認密碼', validators=[DataRequired(),
        Length(6, 20, message='密碼長度為6至20字元')])
    email = StringField('信箱', validators=[Optional(),
        Email(message='信箱格式有誤')])
    submit = SubmitField('註冊')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('帳號已存在')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('信箱已被註冊')


# 變更密碼表單
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('請輸入舊密碼', validators=[DataRequired()])
    new_password = PasswordField('請輸入新密碼', validators=[DataRequired(),
        EqualTo('new_password2', message='輸入的新密碼不一致'),
        Length(6, 20, message='密碼長度為6至20字元')])
    new_password2 = PasswordField('再次確認新密碼', validators=[DataRequired(),
        Length(6, 20, message='密碼長度為6至20字元')])
    submit = SubmitField('變更密碼')


# 修改信箱表單
class EditEmailForm(FlaskForm):
    password = PasswordField('請輸入密碼以進行操作', validators=[DataRequired()])
    new_email = StringField('請輸入新信箱', validators=[DataRequired(),
        EqualTo('new_email2', message='輸入的新信箱不一致'),
        Email(message='信箱格式有誤')])
    new_email2 = StringField('再次確認新信箱', validators=[DataRequired(),
        Email(message='信箱格式有誤')])
    submit = SubmitField('修改信箱')

    def validate_new_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('信箱已被註冊')


# 請求寄出重置密碼信件表單
class RequestResetForm(FlaskForm):
    email = StringField('註冊信箱', validators=[DataRequired(),
        Email(message='信箱格式有誤')])
    submit = SubmitField('確認送出')

    def validate_email(self, field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('信箱不存在')


# 重置密碼表單
class ResetPasswordForm(FlaskForm):
    new_password = PasswordField('請輸入新密碼', validators=[DataRequired(),
        EqualTo('new_password2', message='輸入的新密碼不一致'),
        Length(6, 20, message='密碼長度為6至20字元')])
    new_password2 = PasswordField('再次確認新密碼', validators=[DataRequired(),
        Length(6, 20, message='密碼長度為6至20字元')])
    submit = SubmitField('重置密碼')