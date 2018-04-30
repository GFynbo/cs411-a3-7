# CS411 A3 Group 7
CS411 Group Project

Installation Instructions
----
- pip install Django==1.11 
- pip install social-auth-core
- pip install social-auth-app-django
- pip install psycopg2
- pip install dotenv

Run Instructions 
----
1. Set up PostgreSQL (database instructions below)
2. run `python3 manage.py migrate`
3. run `python manage.py runserver`
4. Should be running on http://127.0.0.1:8000/

Database Instructions 
----
Create a database using postgres with a database named `mypantry` and a user named `mypantry` with full database access. Add to the `.env` file and put in the `/MyPantry/MyPantry` directory.

---
#### Contributors
*Gavin, Rachel, Uthrash, Ivanna*
