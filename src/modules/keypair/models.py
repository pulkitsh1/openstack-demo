from src.service_modules.db.conn import db

class KeyPair(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80),nullable=False)
    private_key = db.Column(db.TEXT,nullable=True)
    fingerprint = db.Column(db.String(256), nullable=False)
    type = db.Column(db.String(80), nullable=False)
    public_key = db.Column(db.TEXT,nullable=False)
    instances = db.relationship('Instances', backref='key_pair')
    status = db.Column(db.String(80),nullable=False)

    def __repr__(self):
        return f"KeyPair '{self.id}', '{self.name}', '{self.private_key}', '{self.fingerprint}','{self.type}','{self.public_key}', '{self.status}')"