# HackathonManager
HakathonManager is a Django application that allows organizations to manage hackathons and submissions. It provides APIs for user sign-in, sign-up, logout, posting hackathons, registering for hackathons, making submissions, and more.

# Features
* User authentication and authorization
* Posting and registering for hackathons
* Submitting and reviewing submissions

# Installation
## Using Github:
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
## Using Docker:
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
