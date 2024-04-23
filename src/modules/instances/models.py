from src.service_modules.db.conn import db

class Instances(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80),nullable=False)
    created_at = db.Column(db.String(80),nullable=True)
    network_id = db.Column(db.Integer,db.ForeignKey('network.id'))
    image_id = db.Column(db.Integer,db.ForeignKey('images.id'))
    flavor_id = db.Column(db.Integer,db.ForeignKey('flavors.id'))
    keypair_id = db.Column(db.Integer,db.ForeignKey('key_pair.id'))
    status = db.Column(db.String(80),nullable=False)
    

    def __repr__(self):
        return f"Instances '{self.id}', '{self.name}', '{self.network_id}', '{self.image_id}','{self.flavor_id}','{self.created_at}', '{self.status}')"