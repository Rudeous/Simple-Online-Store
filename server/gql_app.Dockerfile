FROM python:3.8.5-slim-buster
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY gql_app.py seed_db.py model.py schema.py helper.py db.py ./
CMD ["python", "gql_app.py"]