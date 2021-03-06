import json, datetime
from app import db
from app.models.role import Role
from app.models.client_request import ClientRequest
from app.models.messages import Message
from app.models.feature_requests import FeatureRequest
from sqlalchemy.ext.declarative import DeclarativeMeta
from uuid import UUID

class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    username = db.Column(db.String(30), unique=True)
    company = db.Column(db.String(30))
    active = db.Column(db.Boolean)
    email_address = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(100))
    role = db.relationship('Role', backref='user', uselist=False)
    client_requests = db.relationship('ClientRequest', backref='user')
    messages = db.relationship('Message', backref='user')
    feature_requests = db.relationship('FeatureRequest', backref='user')

    RELATIONSHIPS_TO_DICT = True

    def __iter__(self):
        return self.to_dict().iteritems()

    def to_dict(self, rel=None, backref=None):
        if rel is None:
            rel = self.RELATIONSHIPS_TO_DICT
        res = {column.key: getattr(self, attr)
               for attr, column in self.__mapper__.c.items()}
        if rel:
            for attr, relation in self.__mapper__.relationships.items():
                # Avoid recursive loop between to tables.
                if backref == relation.table:
                    continue
                value = getattr(self, attr)
                if value is None:
                    res[relation.key] = None
                elif isinstance(value.__class__, DeclarativeMeta):
                    res[relation.key] = value.to_dict(backref=self.__table__)
                else:
                    res[relation.key] = [i.to_dict(backref=self.__table__)
                                         for i in value]
        return res

    def to_json(self, rel=None):
        def extended_encoder(x):
            if isinstance(x, datetime):
                return x.isoformat()
            if isinstance(x, UUID):
                return str(x)
        if rel is None:
            rel = self.RELATIONSHIPS_TO_DICT
        return json.dumps(self.to_dict(rel), default=extended_encoder)
