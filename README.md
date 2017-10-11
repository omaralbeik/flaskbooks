
<p align="left">
  <img src="https://github.com/omaralbeik/flask-books/blob/master/screenshots/logo.jpg?raw=true" title="flask-books">
</p>

A very light social network for sharing books built using Flask and Python 3

## Main Features

### Web Endpoints
  - `/books`: All books (homepage).
  - `/books/new`: Create a new book.
  - `/book/book_id`: Book page.
  - `/book/book_id/edit`: Edit book.
  - `/book/book_id/delete`: Delete book.
  - `/genres`: All genres.
  - `/genres/new`: Create a new genre.
  - `/genre/genre_id`: Genre page.
  - `/genre/genre_id/edit`: Edit genre.
  - `/genre/genre_id/delete`: Delete genre.
  - `/users`: All users.
  - `/user/user_id`: User page.
  - `/user/user_id/edit`: Update user info.  
  - `/auth`: Login page.

### RESTful Endpoints
- `/books/JSON`: All books JSON.
- `/book/book_id/JSON`: Book JSON.
- `/genres/JSON`: All genres JSON.
- `/genre/genre_id/JSON`: Genre JSON.
- `/users/JSON`: All users JSON.
- `/user/user_id/JSON`: User JSON.  


## How to Run

### Setup a Google+ authentication app
1. go to https://console.developers.google.com/project and login with your Google account.
2. Create a new project
3. Select "API's and Auth -> Credentials -> Create a new OAuth client ID" from the project menu
4. Select Web Application
5. On the consent screen, type in a product name and save.
6. In Authorized javascript origins add: http://0.0.0.0:5000 and http://localhost:5000
7. Click create client ID
8. Click download JSON and save it into the root director of this project.
9. Rename the JSON file "client_secret.json"
10. Replace the old client_secret.json file with yours

### Run on a Vagrant virtual machine:
Please ensure you have [Python](https://www.python.org/), [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/wiki/Downloads) installed. This project uses a pre-congfigured Vagrant virtual machine which has all required packages installed.

1. In the root directory, use the command `vagrant up`, this will install the vagrant machine.
2. Once it's complete, type `vagrant ssh` to login to the VM.
3. In the vm, `cd /vagrant/flaskbooks`
4. type `make` to install dependencies and setup the database
5. type `python3 application.py` to start the server.


### Run on your Linux server:
1. Use [this tutorial](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-16-04?utm_content=how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-16-04) from digitalocean to set up your Nginx and run the application on Ubuntu 16.04
2. type `make` to install dependencies and setup the database

### Open in your browser
Now you can open in a webpage by going to either: http://0.0.0.0:5000, http://localhost:5000, or your set domain


## Project Structure
 - [static](https://github.com/omaralbeik/flask-books/tree/master/static): Bootstrap, images, styles
 - [templates](https://github.com/omaralbeik/flask-books/tree/master/templates): html templates
 - [application.py](https://github.com/omaralbeik/flask-books/blob/master/application.py): Flask application
 - [client_secrets.json](https://github.com/omaralbeik/flask-books/blob/master/client_secrets.json): Google client secrets / **replace this with yours**
 - [dbhelpers.py](https://github.com/omaralbeik/flask-books/blob/master/dbhelpers.py): common helper functions for database objects
 - [helpers.py](https://github.com/omaralbeik/flask-books/blob/master/helpers.py): common helper functions
 - [model.py](https://github.com/omaralbeik/flask-books/blob/master/model.py): data model objects


## Data Model
flask-books stores data using [SQLite3](https://www.sqlite.org/) and [SQLAlchemy](https://www.sqlalchemy.org/) for object mapping.

### Model objects:
- User
- Book
- Genre
- Like

### Model Diagram
[model.py](https://github.com/omaralbeik/flask-books/blob/master/model.py)
<p align="left">
  <img src="https://github.com/omaralbeik/flask-books/blob/master/screenshots/model.jpg?raw=true" title="model">
</p>


## Support the project
**Please star the project to let me know you liked it!**


## Get involved:
Your feedback is always appreciated and welcomed. Please send me an email to **[omaralbeik@gmail.com](mailto:omaralbeik@gmail.com)** if you have any questions,
or fork the project and get your hand dirty with the code and submit a Pull Request :)
