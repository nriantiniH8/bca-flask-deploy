from datetime import datetime
from config import db, ma
from marshmallow import fields


class Person(db.Model):
    __tablename__ = 'person'
    person_id = db.Column(
        db.Integer,
        primary_key=True
    )
    lname = db.Column(db.String(32))
    fname = db.Column(db.String(32))
    timestamp = db.Column(
        db.DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow
    )
    notes = db.relationship(
        'Note',
        backref='person',
        cascade='all, delete,delete-orphan' ,
        single_parent=True,
        order_by='desc(Note.timestamp)'
    )
    
    def update(self):
        db.session.merge(self)
        db.session.commit()
        
        return self
    
    def save(self):
        db.session.commit()

class PersonNoteSchema(ma.SQLAlchemyAutoSchema):
    note_id = fields.Integer()
    person_id = fields.Int()
    content = fields.String()
    timestamp = fields.String()    

class PersonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Person
        sqla_session = db.session
        
    notes = fields.Nested(PersonNoteSchema, many=True)
    
    
    
    
    
    
    # note = ma.Pluck(PersonNoteSchema, 'note', many=True)

# with flask_app.app_context():
#     person = (
#         Person.query.filter(Person.person_id == 1)
#         .join(Note)
#         .one_or_none()
#     )
#     person_schema = PersonSchema()
#     result = person_schema.dump(person)
#     print(result)
    
    # person = Person(fname="Monty", lname="monty@python.org")
    # notes = Note(content="Something Completely Different", person_id=person.person_id)
    # person = Person(fname="Monty", lname="monty@python.org", notes=[notes])
    
    # result = PersonSchema().dump(person)
    # print(result)
    