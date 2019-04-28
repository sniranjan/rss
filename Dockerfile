FROM python:3
COPY requirements.txt /emx/requirements.txt
RUN pip install -r /emx/requirements.txt
WORKDIR /emx
COPY . /emx
ENV PATH /emx:$PATH
CMD ["gunicorn", "--config","gunicorn.conf","app:app()"]