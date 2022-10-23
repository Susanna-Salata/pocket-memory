# start by pulling the python image
FROM python:3.9-alpine3.16

RUN mkdir /app
# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install libfi library
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev \
    && apk add libffi-dev

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app


# set environmetn variables
ENV JWT_SECRET_KEY=qwerty
ENV JWT_REFRESH_SECRET_KEY=ytrew
ENV MONGO_CONNECTION_STRING=mongodb+srv://VadymKu:k*V190821@cluster0.nrqiq.mongodb.net/?retryWrites=true&w=majority

EXPOSE 8000

# Run the image as a non-root user
RUN adduser -D myuser
USER myuser

#CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD ["gunicorn", "-b", "127.0.0.1:8000", "app:app"]
# $PORT is set by Heroku
#CMD gunicorn --bind 0.0.0.0:$PORT wsgi
CMD uvicorn app:app --host 0.0.0.0 --port $PORT