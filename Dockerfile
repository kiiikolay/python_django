FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /app

EXPOSE 8000

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip "poetry==2.1.2"
# RUN pip install -r requirements.txt
RUN poetry config virtualenvs.create false --local
COPY pyproject.toml poetry.lock ./
run poetry install

COPY mysite .

# CMD ["python", "manage.py", "runserver"]
CMD ["qunicorn", "mysite.wsgi:application", "--build", "0.0.0.0:8000"]

