"""
Message Model
"""
from datetime import datetime
from app import db


class Message(db.Model):
    """Direct message between users and creators."""
    
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('creators.id'), nullable=False, index=True)
    subject = db.Column(db.String(255), nullable=True)
    body = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    is_replied = db.Column(db.Boolean, default=False)
    reply_body = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    replied_at = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<Message {self.id} - {self.subject}>'
    
    def mark_as_read(self):
        """Mark message as read."""
        self.is_read = True
    
    def reply(self, reply_text):
        """Reply to message."""
        self.reply_body = reply_text
        self.is_replied = True
        self.replied_at = datetime.utcnow()
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'sender': self.sender.to_dict() if self.sender else None,
            'subject': self.subject,
            'body': self.body,
            'is_read': self.is_read,
            'is_replied': self.is_replied,
            'reply_body': self.reply_body,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
