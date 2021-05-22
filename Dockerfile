FROM python:3.8.5

ENV APP_HOME /app
ENV PATH /home/user/miniconda3/bin/:$PATH
WORKDIR $APP_HOME

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT ["python app.py"]