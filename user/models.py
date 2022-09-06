from db import db
class User(db.Model) :
    
    id = db.Column(db.Integer(), primary_key = True)
    email = db.Column(db.String(70), unique = True)
    password = db.Column(db.String(300))
    tags = db.relationship("Tag", backref="user")
    posts = db.relationship("Post", backref="user")

    def __repr__(self) :
        return f'{self.id}'


    def save(self) :
        db.session.add(self)
        db.session.commit()

    
    def delete(self) :
        db.session.delete(self)
        db.session.commit()

    def update(self, email, password) :
        self.email = email
        self.password = password
        db.session.commit()
    

from posts.models import Tag, Post