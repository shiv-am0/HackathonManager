# HackathonManager
HakathonManager is a Django application that allows organizations to manage hackathons and submissions. It provides APIs for user sign-in, sign-up, logout, posting hackathons, registering for hackathons, making submissions, and more.

# Features
* User authentication and authorization
* Posting and registering for hackathons
* Submitting and reviewing submissions

# Installation
### Using Github:
1. Clone the repository:
```bash
git clone https://github.com/shiv-am0/HackathonManager.git
```
2. Install the dependencies:
```bash
pip install -r requirements.txt
```
3. Set up the database:
```bash
python manage.py makemigrations
python manage.py migrate
```
4. Run the server:
```bash
python manage.py runserver
```
### Using Docker:
1. Visit the following link to get docker for your operating system: https://docs.docker.com/get-docker/
2. Pull the docker image from docker hub using the following command.
```bash
docker pull shivam001/hackathon-manager
```
3. Run the docker container using the following command.
```bash
docker run -d -p 8000:8000 shivam001/hackathon-manager
```
4. The endpoints can be hit on `localhost:8000`.
5. To stop the currently running container, use the following command:
```bash
docker stop <container-name>
```
# API
* The base URL is: `http://localhost:8000/`.
* Modify the Request Headers as given: `Content-Type: application/x-www-form-urlencoded`.
* The Postman settings can be found and imported from [postman-endpoints/HackathonManagement.postman_collection.json](https://github.com/shiv-am0/HackathonManager/tree/master/postman-endpoints).

# Usage
1. The Users home can be reached using the API endpoint `/users/`.
2. Sign up for an account using the API endpoint `/users/signup/`.
3. Sign in to your account using the API endpoint `/users/signin/`.
4. Log out of your account using the API endpoint `/users/logout/`.
5. The Hackathons home can be reached using the API endpoint `/users/hackathons/`.
6. Post a new hackathon using the API endpoint `/users/hackathon/post_hackathon`.
7. Register for a hackathon using the API endpoint `/users/hackathons/register_for_hackathon`.
8. Get all hackathons using the API endpoint `/users/hackathons/get_hackathons`.
9. Delete a hackathon using the API endpoint `/users/hackathons/delete_hackathon`.
10. The Submissions home can be reached using the API endpoint `/users/hackathons/submissions`.
11. Get all submissions using the API endpoint `/users/hackathons/submissions/get_all_submissions`.
12. Make submission to a registered hackathon using the API endpoint `/users/hackathons/submissions/make_submission`.
13. Delete a submission using the API endpoint `/users/hackathons/submissions/delete_submission`.

# License
HakathonManager is licensed under the [MIT License](https://opensource.org/license/mit/).
