"""
Bookshelf Forms
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class PdfForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    creator = StringField('Creator', render_kw={'disabled':''})
    producer = StringField('Producer', render_kw={'disabled':''})
    creation_date = StringField('Creation date', render_kw={'disabled':''})
    modification_date = StringField('Modification date', render_kw={'disabled':''})
    author = StringField('Author', validators=[DataRequired()])
    formatted_size = StringField('Size', render_kw={'disabled':''})
    extension = StringField('Extension', render_kw={'disabled':''})
    submit = SubmitField('Save')
