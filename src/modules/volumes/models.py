from src.service_modules.db.conn import db

class Volume(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80),nullable=False)
    volume_id = db.Column(db.String(80),nullable=False)
    size = db.Column(db.Integer,nullable=False)
    description = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.String(80),nullable=False)
    status = db.Column(db.String(80),nullable=False)

    def __repr__(self):
        return f"Volume '{self.id}', '{self.name}', '{self.size}', '{self.description}','{self.volume_type}','{self.created_at}', '{self.status}')"