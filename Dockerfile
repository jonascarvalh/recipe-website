FROM python:3.11
WORKDIR /opt/app
RUN python3 -m venv venv
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
RUN python manage.py migrate
EXPOSE 8000
# RUN python manage.py runserver --insecure
ENTRYPOINT [ "python", "manage.py" ]
CMD [ "runserver", "0.0.0.0:8000" ]