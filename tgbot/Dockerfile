FROM python:3.11-slim
LABEL author='hakaton_team_1' version=1
WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir
COPY . ./
CMD ["python", "manage.py", "runserver", "0:8000"]
