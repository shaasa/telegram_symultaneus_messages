from app import db
from datetime import datetime

# Tabella di associazione per la relazione many-to-many tra Group e User
group_users = db.Table('group_users',
                       db.Column('group_id', db.Integer, db.ForeignKey('groups.id'), primary_key=True),
                       db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
                       )

class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relazione many-to-many con User
    users = db.relationship('User', secondary=group_users, lazy='subquery',
                            backref=db.backref('groups', lazy=True))

    def __repr__(self):
        return f'<Group {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'user_count': len(self.users)
        }

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.String(20), unique=True, nullable=False, index=True)
    username = db.Column(db.String(100), index=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    display_name = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_interaction = db.Column(db.DateTime)

    def __repr__(self):
        return f'<User {self.display_name or self.username or self.telegram_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'telegram_id': self.telegram_id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'display_name': self.display_name,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_interaction': self.last_interaction.isoformat() if self.last_interaction else None
        }

    @property
    def full_name(self):
        if self.display_name:
            return self.display_name
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        if self.first_name:
            return self.first_name
        if self.username:
            return f"@{self.username}"
        return f"User {self.telegram_id}"

class MessageLog(db.Model):
    __tablename__ = 'message_logs'

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    message_text = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(20), default='pending', nullable=False, index=True)  # pending, sent, failed
    error_message = db.Column(db.Text)
    telegram_message_id = db.Column(db.String(50))  # ID del messaggio su Telegram se inviato

    group = db.relationship('Group', backref='message_logs')
    user = db.relationship('User', backref='message_logs')

    def to_dict(self):
        return {
            'id': self.id,
            'group_id': self.group_id,
            'user_id': self.user_id,
            'message_text': self.message_text,
            'sent_at': self.sent_at.isoformat(),
            'status': self.status,
            'error_message': self.error_message,
            'telegram_message_id': self.telegram_message_id
        }