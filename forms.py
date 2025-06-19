from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, FloatField, SelectField, URLField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, Optional, ValidationError
from models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirm Password', 
                             validators=[DataRequired(), EqualTo('password')])
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered.')

class AnimeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description')
    genre = StringField('Genre', validators=[Length(max=100)])
    rating = FloatField('Rating', validators=[Optional(), NumberRange(min=0, max=10)])
    year = IntegerField('Year', validators=[Optional(), NumberRange(min=1900, max=2030)])
    poster_url = URLField('Poster URL')
    trailer_url = URLField('Trailer URL')

class AnimeSeasonForm(FlaskForm):
    season_number = IntegerField('Season Number', validators=[DataRequired(), NumberRange(min=1)])
    title = StringField('Season Title', validators=[Length(max=200)])

class AnimeEpisodeForm(FlaskForm):
    episode_number = IntegerField('Episode Number', validators=[DataRequired(), NumberRange(min=1)])
    title = StringField('Episode Title', validators=[Length(max=200)])
    description = TextAreaField('Description')
    torrent_url = URLField('Torrent/Magnet URL', validators=[DataRequired()])
    duration_minutes = IntegerField('Duration (minutes)', validators=[Optional(), NumberRange(min=1)])
    thumbnail_url = URLField('Thumbnail URL')

class MovieForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description')
    genre = StringField('Genre', validators=[Length(max=100)])
    rating = FloatField('Rating', validators=[Optional(), NumberRange(min=0, max=10)])
    year = IntegerField('Year', validators=[Optional(), NumberRange(min=1900, max=2030)])
    duration_minutes = IntegerField('Duration (minutes)', validators=[Optional(), NumberRange(min=1)])
    poster_url = URLField('Poster URL')
    trailer_url = URLField('Trailer URL')

class MoviePartForm(FlaskForm):
    part_number = IntegerField('Part Number', validators=[DataRequired(), NumberRange(min=1)])
    title = StringField('Part Title', validators=[Length(max=200)])
    duration_minutes = IntegerField('Duration (minutes)', validators=[Optional(), NumberRange(min=1)])
    torrent_url = URLField('Torrent/Magnet URL', validators=[DataRequired()])
