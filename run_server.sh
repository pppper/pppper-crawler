source .venv/bin/activate
export PYTHONPATH=.
export FLASK_APP=server
export FLASK_ENV=development
python -m flask run --host=0.0.0.0 --port=5000
