#pull image
FROM python:3.9.6-alpine

#create directory and dedicated app user
RUN mkdir -p /home/appuser/staticfiles
RUN addgroup -S appuser && adduser -S appuser -G appuser

#env vars
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#change the working directory
WORKDIR /home/appuser

#install psycopg2 dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

#update packages and install dependencies  
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

#copy app content into container
COPY . .

COPY ./entrypoint.sh .
RUN chmod +x ./entrypoint.sh

#change files ownership and switch to dedicated app user
RUN chown -R appuser:appuser /home/appuser
USER appuser

#expose port
EXPOSE 8000

CMD ["sh", "/home/appuser/entrypoint.sh"]