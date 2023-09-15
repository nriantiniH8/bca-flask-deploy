from flask import abort
from models.note_model import Note
from models.person_model import Person, PersonSchema
from config import db

# /api/people
def read_all():
    people = Person.query.outerjoin(Note).all()
    # print(people)
    person_schema = PersonSchema(many=True)
    data =  person_schema.dump(people)
    # print(data)
    return data


def read_one(person_id):
    person = (
        Person.query.filter(Person.person_id == person_id)
        .outerjoin(Note)
        .one_or_none()
    )
    
    # Did we find a person?
    if person is not None:

        # Serialize the data for the response
        person_schema = PersonSchema()
        data = person_schema.dump(person)
        return data

    # Otherwise, nope, didn't find that person
    else:
        abort(404, f"Person not found for Id: {person_id}")

def update(person_id, person_data):
    
    print(type(person_data), "Type person data")
    
    
    # Ambil 1 data dari database yang mempunyai idp erson_id
    updated_person = Person.query.get(person_id)
    
    if updated_person is None:
        abort(
            404,
            f"Person not found for Id: {person_id}"
        )
    else:
        
        person_schema = PersonSchema()
        updated_person.fname = person_data['fname']
        updated_person.lname = person_data['lname']
        
        updated = updated_person.update()

        return person_schema.dump(updated)
