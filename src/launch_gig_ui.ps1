$env:FLASK_APP = "$PSScriptRoot\gig_flask.py"
$env:FLASK_ENV = "development"
#$env:FLASK_APP
start  http://localhost:5000/
python -m flask run