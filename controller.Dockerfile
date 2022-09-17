FROM python:3.8.5-slim-buster
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY templates ./templates
COPY controller.py seed_db.py model.py schema.py helper.py db.py ./
CMD ["python", "controller.py"]