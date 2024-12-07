from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, DateTimeField, FloatField
from wtforms.validators import DataRequired, Optional, Length

class ProjectForm(FlaskForm):
    name = StringField('Project Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Create Project')

class ImageUploadForm(FlaskForm):
    image = FileField('Image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg'], 'JPEG images only!')
    ])
    title = StringField('Title', validators=[Optional(), Length(max=255)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=1000)])
    keywords = StringField('Keywords (comma-separated)', validators=[Optional(), Length(max=500)])
    copyright = StringField('Copyright', validators=[Optional(), Length(max=255)])
    author = StringField('Author', validators=[Optional(), Length(max=255)])
    created_date = DateTimeField('Creation Date', validators=[Optional()], format='%Y-%m-%d %H:%M:%S')
    latitude = FloatField('Latitude', validators=[Optional()])
    longitude = FloatField('Longitude', validators=[Optional()])
    submit = SubmitField('Upload')

class ExifEditForm(FlaskForm):
    title = StringField('Title', validators=[Optional(), Length(max=255)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=1000)])
    keywords = StringField('Keywords (comma-separated)', validators=[Optional(), Length(max=500)])
    copyright = StringField('Copyright', validators=[Optional(), Length(max=255)])
    author = StringField('Author', validators=[Optional(), Length(max=255)])
    created_date = DateTimeField('Creation Date', validators=[Optional()], format='%Y-%m-%d %H:%M:%S')
    latitude = FloatField('Latitude', validators=[Optional()])
    longitude = FloatField('Longitude', validators=[Optional()])
    submit = SubmitField('Save Changes')