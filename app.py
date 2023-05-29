from flask import jsonify, request
from datetime import datetime
from config import db, app

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, text):
        self.text = text

@app.route('/')
def index():
    return 'Notebook API'

@app.route('/notes', methods=['POST'])
def create_note():
    text = request.json.get('text')
    if not text:
        return jsonify({'error': 'Text is required'}), 400
    note = Note(text)
    db.session.add(note)
    db.session.commit()
    return jsonify({'message': 'Note created', 'note_id': note.id}), 201

@app.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    note = Note.query.get(note_id)
    if not note:
        return jsonify({'error': 'Note not found'}), 404
    text = request.json.get('text')
    if not text:
        return jsonify({'error': 'Text is required'}), 400
    note.text = text
    db.session.commit()
    return jsonify({'message': 'Note updated'})

@app.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    note = Note.query.get(note_id)
    if not note:
        return jsonify({'error': 'Note not found'}), 404

    db.session.delete(note)
    db.session.commit()
    return jsonify({'message': 'Note deleted'})

@app.route('/notes', methods=['GET'])
def get_all_notes():
    with app.app_context():
        notes = Note.query.all()
        results = []
        for note in notes:
            note_data = {
                'id': note.id,
                'text': note.text,
                'date_added': note.date_added
            }
            results.append(note_data)
    return jsonify(results)

@app.route('/notes/<int:note_id>', methods=['GET'])
def get_id_notes(note_id):
    note = Note.query.get_or_404(note_id)
    return jsonify({'id': note.id, 'text': note.text, 'date_added': note.date_added})


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()
