from src.service_modules.db.conn import db

class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80),nullable=False)
    image_id = db.Column(db.String(80),nullable=False)
    min_disk = db.Column(db.String(80),nullable=False)
    min_ram = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.String(80),nullable=False)
    instances = db.relationship('Instances', backref='images')
    status = db.Column(db.String(80),nullable=False)

    def __repr__(self):
        return f"Images '{self.id}', '{self.name}', '{self.image_id}', '{self.min_disk}','{self.min_ram}','{self.created_at}', '{self.status}')"