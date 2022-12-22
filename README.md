# MovieCollectionManager
A movie collection manager service using Django + DRF

## Steps to setup:
1. Clone this repository using `git clone`
2. Using terminal move to the topmost `MovieCollectionManager` dir, where you can see `README.md`
3. Install the Python dependencies using `venv` or directly (not recommended) - by running `pip3 install -r requirements.txt`
4. Now do `cd MovieCollectionManager` - here you should see `mangage.py` 
5. Perform the initial migration, run `python3 manage.py migrate`
6. Create the superuser (admin) by running `python3 manage.py createsuperuser` and following the wizard
7. Perform automated tests: `python3 manage.py test`
8. Start the dev server using `python3 manage.py runserver` - this will start and expose the service on `http://localhost:8000`
9. Now you are ready to test the APIs
10. I have shared the Postman collection and the environment in `MovieCollectionManager/postman` dir, for convenience and they also include saved example responses

### Note: In case the JWT token expires, trigger the `0.1 Login user` request from the Postman collection - this should automatically update the `auth_token` env variable in Postman.
