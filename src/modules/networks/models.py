from src.service_modules.db.conn import db

class Network(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80),nullable=False)
    network_id = db.Column(db.String(160),nullable=False)
    created_at = db.Column(db.String(80),nullable=False)
    subnets= db.relationship('Subnet', backref='network')
    instances = db.relationship('Instances', backref='network')
    status = db.Column(db.String(80),nullable=False)

    def __repr__(self):
        return f"Network '{self.id}','{self.network_name}','{self.created_at}')"
    
class Subnet(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80),nullable=False)
    ip_version = db.Column(db.Integer, nullable=False)
    cidr = db.Column(db.String(80),nullable=False)
    gateway_ip = db.Column(db.String(80),nullable=True)
    network_id = db.Column(db.Integer,db.ForeignKey('network.id'))
    status = db.Column(db.String(80),nullable=False)

    def __repr__(self):
        return f"Subnets '{self.id}','{self.name}', '{self.ip_version}','{self.cidr}','{self.gateway_ip}','{self.network_id}')"