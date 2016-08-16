from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(Form):
    lat = StringField('lat', validators=[DataRequired()])
    lon = StringField('lon', validators=[DataRequired()])
    dtg = StringField('dtg', validators=[DataRequired()])
