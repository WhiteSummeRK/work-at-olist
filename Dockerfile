# Dockerfile create for development purposes - The application will function fully on heroku.
# Run command:
# sudo docker run -p 5432:5432 --name={name_container} -v {volume_name}:/var/lib/postgresql/data {docker_image}

FROM postgres:latest

RUN apt-get update -y && apt-get upgrade -y && apt-get install -y vim

ENV POSTGRES_USER call_receiver
ENV POSTGRES_PASSWORD call_receiver123
ENV POSTGRES_DB call_receiver_db

USER postgres

EXPOSE 5432

RUN initdb && echo "host all all 0.0.0.0/0 trust" >> /var/lib/postgresql/data/pg_hba.conf
