from flask import Flask
from snapshots.snapshot_runner import snapshots

app = Flask(__name__)

app.register_blueprint(snapshots, url_prefix="/snapshots")

@app.route("/")
def hello_world():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)  
