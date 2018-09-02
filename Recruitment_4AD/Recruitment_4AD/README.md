# recruit

A Django recruitment application for Employers, Candidates and Recruiters. This project is a work in progress.


### Preparation
1. Install dependencies `pip install -r requirements.txt`
2. Run `python manage.py makemigrations accounts`
3. Run `python manage.py makemigrations Condidtate`
4. Create database tables `python manage.py migrate`
5. Create admin account `python manage.py createsuperuser`
6. Run the Server using `python manage.py runserver`
7. Visit `http://127.0.0.1:8000/recruitment` in your browser
8. Visit `http://127.0.0.1:8000/login` in brower and username should be 'asif' and password 'mcapgcet' for Admin login
