FROM python:3.8.5

ENV APP_HOME /app
WORKDIR $APP_HOME

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["app.py"]
