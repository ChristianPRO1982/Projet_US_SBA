FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app

RUN python -m venv /opt/venv
ENV PATH="opt/venv/bin:$PATH"

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

ENV PYTHONUNBUFFERED 1

COPY . /app

EXPOSE 8001

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8001"]
# CMD ["uvicorn", "main:app", "--reload", "--port", "8001"]
