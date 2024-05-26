


FROM python:3.11

EXPOSE 8000 


ADD requirements.txt .

RUN python -m pip install -r requirements.txt




CMD [“python”, “./main.py”] 