from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Subscription related
    subscription_type = db.Column(db.String(20), default='free')  # free, regular, vip
    subscription_expires = db.Column(db.DateTime)
    episodes_watched_today = db.Column(db.Integer, default=0)
    last_episode_date = db.Column(db.Date)
    active_devices = db.Column(db.Integer, default=0)
    
    # Relationships
    watch_history = db.relationship('WatchHistory', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def ensure_admin_vip(self):
        """Ensure admin users have VIP subscription"""
        if self.is_admin and self.subscription_type != 'vip':
            self.subscription_type = 'vip'
            self.subscription_expires = datetime.utcnow() + timedelta(days=365)
            db.session.commit()
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_subscription_active(self):
        if self.subscription_type == 'free':
            return True
        return self.subscription_expires and self.subscription_expires > datetime.utcnow()
    
    def can_watch_episode(self):
        if self.subscription_type != 'free':
            return True
        
        today = datetime.utcnow().date()
        if self.last_episode_date != today:
            self.episodes_watched_today = 0
            self.last_episode_date = today
            db.session.commit()
        
        return self.episodes_watched_today < 5
    
    def increment_episodes_watched(self):
        today = datetime.utcnow().date()
        if self.last_episode_date != today:
            self.episodes_watched_today = 1
            self.last_episode_date = today
        else:
            self.episodes_watched_today += 1
        db.session.commit()

class Anime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    genre = db.Column(db.String(100))
    rating = db.Column(db.Float, default=0.0)
    year = db.Column(db.Integer)
    poster_url = db.Column(db.String(500))
    trailer_url = db.Column(db.String(500))  # URL untuk trailer anime
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    seasons = db.relationship('AnimeSeason', backref='anime', lazy=True, cascade='all, delete-orphan')

class AnimeSeason(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    anime_id = db.Column(db.Integer, db.ForeignKey('anime.id'), nullable=False)
    season_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200))
    
    # Relationships
    episodes = db.relationship('AnimeEpisode', backref='season', lazy=True, cascade='all, delete-orphan')

class AnimeEpisode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    season_id = db.Column(db.Integer, db.ForeignKey('anime_season.id'), nullable=False)
    episode_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    torrent_url = db.Column(db.String(500))  # Magnet or torrent URL
    duration_minutes = db.Column(db.Integer)
    thumbnail_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    genre = db.Column(db.String(100))
    rating = db.Column(db.Float, default=0.0)
    year = db.Column(db.Integer)
    duration_minutes = db.Column(db.Integer)
    poster_url = db.Column(db.String(500))
    trailer_url = db.Column(db.String(500))  # URL untuk trailer movie
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    parts = db.relationship('MoviePart', backref='movie', lazy=True, cascade='all, delete-orphan')

class MoviePart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    part_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200))
    duration_minutes = db.Column(db.Integer)
    torrent_url = db.Column(db.String(500))  # Magnet or torrent URL for this part
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class WatchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content_type = db.Column(db.String(20), nullable=False)  # 'anime' or 'movie'
    content_id = db.Column(db.Integer, nullable=False)  # ID of anime episode or movie
    watched_at = db.Column(db.DateTime, default=datetime.utcnow)
    watch_time_minutes = db.Column(db.Integer, default=0)  # Time watched in minutes

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plan_type = db.Column(db.String(20), nullable=False)  # regular, vip
    duration_months = db.Column(db.Integer, nullable=False)  # 1, 3, 12
    amount_paid = db.Column(db.Integer, nullable=False)  # Amount in local currency
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    user = db.relationship('User', backref='subscriptions')
