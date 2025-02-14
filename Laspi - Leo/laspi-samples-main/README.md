# laspi-samples

python -m venv .venv
source .venv/bin/activate (ou venv/Scripts/activate)
deactivate

pip install -r requirements.txt

pip freeze > requirements.txt

uvicorn main:app --reload
streamlit run .\frontend.py