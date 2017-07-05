
<p align="left">
  <img src="https://github.com/omaralbeik/flask-books/blob/master/screenshots/logo.jpg?raw=true" title="flask-books">
</p>

A very light social network for sharing books built using Flask

## Live Demo
[omaralbeik.com](http://omaralbeik.com)

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
  - `/genre/user_id`: User page.  
  - `/auth`: User page.

### RESTful Endpoints
- `/books/JSON`: All books JSON.
- `/book/book_id/JSON`: Book JSON.
- `/genres/JSON`: All genres JSON.
- `/genre/genre_id/JSON`: Genre JSON.
- `/users/JSON`: All users JSON.
- `/genre/user_id/JSON`: User JSON.  


## How to Run
Please ensure you have [Python](https://www.python.org/), [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/wiki/Downloads) installed. This project uses a pre-congfigured Vagrant virtual machine which has all required packages installed.

### Setup a Google+ authentication app
1. go to https://console.developers.google.com/project and login with your Google account.
2. Create a new project
3. Select "API's and Auth -> Credentials -> Create a new OAuth client ID" from the project menu
4. Select Web Application
5. On the consent screen, type in a product name and save.
6. In Authorized javascript origins add:
    http://0.0.0.0:5000
    http://localhost:5000
7. Click create client ID
8. Click download JSON and save it into the root director of this project.
9. Rename the JSON file "client_secret.json"
10. Replace the old client_secret.json file with yours

### Setup the Database & Start the Server
1. In the root directory, use the command `vagrant up`, this will install the vagrant machine.
2. Once it's complete, type `vagrant ssh` to login to the VM.
3. In the vm, cd /vagrant/flask-books
5. type `python database_setup.py` this will create the empty database.
6. type `python lots_of_books.py` this will fill the database with some pre-entered books and users.
7. type `python application.py` to start the server.

### Open in your browser
Now you can open in a webpage by going to either:
    http://0.0.0.0:5000
    http://localhost:5000


## Project Structure
 - [static](https://github.com/omaralbeik/flask-books/tree/master/flask_books/static): Bootstrap, images, styles
 - [templates](https://github.com/omaralbeik/flask-books/tree/master/flask_books/templates): html templates
 - [application.py](https://github.com/omaralbeik/flask-books/blob/master/flask_books/application.py): Flask application
 - [client_secrets.json](https://github.com/omaralbeik/flask-books/blob/master/flask_books/client_secrets.json): Google client secrets / **replace this with yours**
 - [database_setup.py](https://github.com/omaralbeik/flask-books/blob/master/flask_books/database_setup.py): set up database for the first time
 - [dbhelpers.py](https://github.com/omaralbeik/flask-books/blob/master/flask_books/dbhelpers.py): common helper functions for database objects
 - [helpers.py](https://github.com/omaralbeik/flask-books/blob/master/flask_books/helpers.py): common helper functions
 - [lots_of_books.py](https://github.com/omaralbeik/flask-books/blob/master/flask_books/lots_of_books.py): creates some books, for testing
 - [model.py](https://github.com/omaralbeik/flask-books/blob/master/flask_books/model.py): data model objects


## Data Model
flask-books stores data using [SQLite3](https://www.sqlite.org/) and [SQLAlchemy](https://www.sqlalchemy.org/) for object mapping.

### Model objects:
- User
- Book
- Genre
- Like

### Model Diagram
[model.py](https://github.com/omaralbeik/flask-books/blob/master/flask_books/model.py)
<p align="left">
  <img src="https://github.com/omaralbeik/flask-books/blob/master/screenshots/model.jpg?raw=true" title="model">
</p>


## Support the project
**Please star the project to let me know you liked it!**


## Get involved:
Your feedback is always appreciated and welcomed. Please send me an email to **[omaralbeik@gmail.com](mailto:omaralbeik@gmail.com)** if you have any questions,
or fork the project and get your hand dirty with the code and submit a Pull Request :)
