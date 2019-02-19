# swim_log

This application allows registered users to track, log, and review analytics based on inputted data of their swims.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Python 3.3+, Virtualenv

### Installing

Make sure you have Virtualenv installed:

```
virtualenv --version
```

Install Virtualenv if you do not have it using one of these commands:
```
$ sudo apt-get install python-virtualenv

$ sudo easy_install virtualenv

$ sudo pip install virtualenv
```

Clone the repo:

```
git clone https://github.com/davidsalazkin/personal_website.git
```

## Deployment

After navigating to the project directory, activate the virtual environment:

```
source swim_log/bin/activate
```

Now you can run the project:

```
python run.py
```

When hosted locally, the project can be viewed in a browser at: http://127.0.0.1:5000/

## Built With

* [Flask](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Flask-WTForms](https://flask-wtf.readthedocs.io/en/stable/) - Form framework
* [Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/en/latest/) - Password hashing
* [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/) - Database toolkit
* [Virtualenv](http://flask.pocoo.org/docs/1.0/installation/) - Dependency management

## Authors

* **David Salazkin**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
