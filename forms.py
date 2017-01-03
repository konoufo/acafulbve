# -*- coding:utf8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class ProjectForm(FlaskForm):
    id = StringField('id', validators=[DataRequired()])


class BVEForm(FlaskForm):
    input_1 = StringField()