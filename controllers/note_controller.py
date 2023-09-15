from models.note_model import Note, NoteSchema
from models.person_model import Person, PersonSchema
from flask import abort
from config import db

# GET /notes
# [
#     { 
#          "note_id": 1,
#          "content": "aaa", timestamp:"....",
#          "person": {lname: "...", fname: "...", "person_id": "..."}
#     }
# ]
def read_all():
    notes =  Note.query.join(Person).all()
    
    note_schema = NoteSchema(many=True)
    results = note_schema.dump(notes)
    
    return results

# ===== POST /people/{person_id}/notes ========
# parameter path: person_id
# request body: note => {"content": "ccccc"}
# response {content: ",,,", person: {....}, note_id: "...", person_id:".."}
def create(person_id, note):
    # 1. find person dengan id person_id
    person = (
        Person.query.filter(Person.person_id == person_id)
        .outerjoin(Note)
        .one_or_none()
    )
    
    # 2. if person not extst abort
    if person is None:
        abort (404, f"Person with id {person_id} is not found")
        
    # 3. if person exists, add new note to person
    content = note.get('content')
    new_note = Note(content = content, person_id = person.person_id)
    
    person.notes.append(new_note)
    
    person.save()
    # db.session.commit()
    
    note_schema = NoteSchema()
    result = note_schema.dump(new_note)
    
    return result
    


# GET /people/{person_id}/notes/{note_id}
# parameter path: person_id, note_id
# response: {content: ",,,", person: {....}, note_id: "...", person_id:".."}
def read_one(person_id, note_id):
    note = ( 
            Note.query.join(Person, Person.person_id == Note.person_id)
                    .filter(Note.note_id == note_id) 
                    # .filter(Person.person_id == Note.person_id) 
                    .one_or_none()
    )
    
    # print(note, "<<<<<<<")
    
    if note is None: 
        abort(404, f"note with id {note_id} own by person {person_id} is not found")
    
    note_schema = NoteSchema()
    result = note_schema.dump(note)
    
    return result



# PUT /people/{person_id}/notes/{note_id}
# req body: {content: "dweeedew"} note
# response: {content: ",,,", person: {....}, note_id: "...", person_id:".."}
def update(person_id, note_id, note):
    found_note = ( 
            Note.query.join(Person)
                    .filter(Note.note_id == note_id) 
                    .filter(Note.person_id == person_id) 
                    .one_or_none()
    )
    
    if found_note is None:
        abort(404, f"note with id {note_id} own by person {person_id} is not found")
    
    found_note.content = note.get('content')
    
    # db.session.merge(found_note)
    # db.session.commit()
    
    content = note.get('content')
    found_note.update(content)
    
    note_schema = NoteSchema()
    result = note_schema.dump(found_note)
    
    return result
    
    
    
# DELETE /people/{person_id}/notes/{note_id}

