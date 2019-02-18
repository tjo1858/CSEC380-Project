FROM mysql:5.7

ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=db
ENV MYSQL_USER=admin
ENV MYSQL_PASSWORD=root

COPY database.sql /docker-entrypoint-initdb.d/database.sql

EXPOSE 3306
