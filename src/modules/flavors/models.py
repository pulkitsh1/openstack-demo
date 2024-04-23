from src.service_modules.db.conn import db

class Flavors(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80),nullable=False)
    flavor_id = db.Column(db.String(80),nullable=False)
    ram = db.Column(db.Integer,nullable=False)
    vcpus = db.Column(db.Integer,nullable=False)
    created_at = db.Column(db.String(80),nullable=True)
    is_public = db.Column(db.String(80),nullable=False)
    instances = db.relationship('Instances', backref='flavors')
    is_disabled = db.Column(db.String(80),nullable=False)

    def __repr__(self):
        return f"flavors '{self.id}', '{self.name}', '{self.flavor_id}', '{self.ram}', '{self.vcpus}','{self.created_at}','{self.is_public}', '{self.is_disabled}')"