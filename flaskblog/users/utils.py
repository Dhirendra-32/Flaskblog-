import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from flaskblog import mail
from flask import current_app

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _,f_extn = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_extn
    picture_path = os.path.join(current_app.root_path,'static/profile_pics',picture_fn)
    output_size =(125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn
    
#send mail fucntion
def send_reset_mail(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',sender=os.environ.get('EMAIL_USER'),recipients=[user.email])
    msg.body = f""" To reset your password, visit following links :{url_for('users.reset_token',token=token,_external = True)}"""
    mail.send(msg)
