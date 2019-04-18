# CSEC380-Project
## Project for Principles of Web Application Security CSEC 380
### Jonah Chrzanowski  |  Smayan Daruka  |  Tyler Olexa 

Each individual activity can be built with the respective docker-compose command.

Travis tests are run with respect to Activity 4, as this is the full working and secure version of our web application. To run the test, simply start the Docker containers using Activity 4 and then run the tests as shown below.

```
cd Activity\ 4/  
docker-compose up --build  
cd ..
pytest test.py
```
---

Activities 5, 6, and 7 are less secure applications as they involve different techniques to make the application vulnerable.

Activity 5 represents a SQL Injection.

Activity 6 represents a SSRF attack.

Activity 7 represents Remote Code Injection.

---

### DO NOT USE THIS APPLICATION FOR SECURE PURPOSES, WE ARE STUDENTS DOING A PROJECT THAT IS BUILT AROUND MAKING A WEB APPLICATION VULNERABLE.

---

Special thanks to https://sample-videos.com/ for the free videos for testing purposes <3
