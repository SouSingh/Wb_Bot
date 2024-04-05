FROM python:3-slim-buster

RUN mkdir /code

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

ENV OPENAI_API_KEY="""

COPY . .

CMD ["uvicorn", "code:app", "--host=0.0.0.0", "--port=80"]