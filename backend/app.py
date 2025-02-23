from flask import Flask
from flask_cors import CORS 
from snapshots.snapshot_runner import snapshots
from transcription.transcription_api import transcription
from evaluation.evaluation_api import evaluation
from bodylanguage.eyecontactscore import contact_score
from questions.questiongeneration import question_generation
from questions.answerfeedback import answer_feedback

app = Flask(__name__)
CORS(app)  # Enabling CORS

app.register_blueprint(snapshots, url_prefix="/snapshots")
app.register_blueprint(transcription, url_prefix="/transcription")
app.register_blueprint(evaluation, url_prefix="/evaluation")
app.register_blueprint(contact_score, url_prefix="/contact-score")
app.register_blueprint(question_generation, url_prefix="/question_generation")
app.register_blueprint(answer_feedback, url_prefix="/answer-feedback")
if __name__ == "__main__":
    app.run(debug=True)
