FROM python:3.13-rc-slim
WORKDIR /app
COPY ./back_end/requirements.txt .
RUN pip install -r requirements.txt
COPY ./back_end/ .
CMD ["uvicorn", "project.app:app", "--host", "0.0.0.0", "--port", "8000"]