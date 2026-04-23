from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def set_password(self, plaintext: str) -> None:
        self.password_hash = generate_password_hash(plaintext)

    def check_password(self, plaintext: str) -> bool:
        return check_password_hash(self.password_hash, plaintext)

    def __repr__(self):
        return f'<User {self.username}>'


class QueryLog(db.Model):
    """
    Records analysis querys submitted through UI and provides searchable history of user interactions
    """
    __tablename__ = 'query_log'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    query_type = db.Column(db.String(50), nullable=False)   # analysis, location
    location = db.Column(db.String(100), nullable=True)     # location filter
    min_temp = db.Column(db.Float, nullable=True)           # temp filter params
    max_temp = db.Column(db.Float, nullable=True)
    min_rainfall = db.Column(db.Float, nullable=True)
    rain_today = db.Column(db.String(10), nullable=True)    # Yes, No, or None
    result_count = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f'<QueryLog {self.id} {self.query_type} @ {self.timestamp}>'


class LocationStats(db.Model):
    """
    Cache computed statistics /location so they arent recalculated with every request. Invaildated if data is reloaded
    """
    __tablename__ = 'location_stats'

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), unique=True, nullable=False)
    total_records = db.Column(db.Integer, nullable=False)
    avg_max_temp = db.Column(db.Float, nullable=True)
    avg_min_temp = db.Column(db.Float, nullable=True)
    avg_rainfall = db.Column(db.Float, nullable=True)
    max_temp_ever = db.Column(db.Float, nullable=True)
    min_temp_ever = db.Column(db.Float, nullable=True)
    rainy_days = db.Column(db.Integer, nullable=True)
    rainy_day_pct = db.Column(db.Float, nullable=True)
    avg_wind_speed = db.Column(db.Float, nullable=True)
    computed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<LocationStats {self.location}>'
