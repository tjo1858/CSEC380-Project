FROM mysql:5.7
RUN sudo service mysql stop
COPY database.sql /docker-entrypoint-initdb.d/database.sql
EXPOSE 3306
