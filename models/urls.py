from shared.factories import db

class Urls(db.Model):
    __tablename__ = "urls"

    id = db.Column(db.Integer, primary_key=True)
    short_url = db.Column(db.String(50), unique=True, nullable=False)
    long_url = db.Column(db.String(500), unique=True, nullable=False)

    def __repr__(self):
        return "<Urls: {}>".format({"short_url":self.short_url, "long_url": self.long_url})
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}