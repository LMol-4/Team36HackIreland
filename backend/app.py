from flask import Flask
from snapshots.snapshot_runner import snapshots
from transcription.transcription_api import transcription
from evaluation.evaluation_api import evaluation

app = Flask(__name__)

app.register_blueprint(snapshots, url_prefix="/snapshots")
app.register_blueprint(transcription, url_prefix="/transcription")
app.register_blueprint(evaluation, url_prefix="/evaluation")

if __name__ == "__main__":
    app.run(debug=True)
