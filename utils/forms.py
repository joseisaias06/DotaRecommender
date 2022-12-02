from flask_wtf import FlaskForm
from wtforms import RadioField, SelectField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired
from utils.variables import choice


class DotaForm(FlaskForm):
    user_id = BooleanField('Recomendar Con Base Estadísticas Personales', default=False)
    side = RadioField('Elegir su lado:', choices=[('Radiant', 'Radiant'), ('Dire', 'Dire')],
                      validators=[DataRequired()], default='Radiant')
    radiant_hero_1 = SelectField(u'Elegir Primer Héroe Radiant:', choices=choice, validators=[DataRequired()])
    radiant_hero_2 = SelectField(u'Elegir Segundo Héroe Radiant:', choices=choice)
    radiant_hero_3 = SelectField(u'Elegir Tercer Héroe Radiant:', choices=choice)
    radiant_hero_4 = SelectField(u'Elegir Cuarto Héroe Radiant:', choices=choice)
    radiant_hero_5 = SelectField(u'Elegir Quinto Héroe Radiant:', choices=choice)
    dire_hero_1 = SelectField(u'Elegir Primer Héroe Dire', choices=choice)
    dire_hero_2 = SelectField(u'Elegir Segundo Héroe Dire:', choices=choice)
    dire_hero_3 = SelectField(u'Elegir Tercer Héroe Dire:', choices=choice)
    dire_hero_4 = SelectField(u'Elegir Cuarto Héroe Dire:', choices=choice)
    dire_hero_5 = SelectField(u'Elegir Quinto Héroe Dire:', choices=choice)
    submit = SubmitField('Obtener Recomendación')
