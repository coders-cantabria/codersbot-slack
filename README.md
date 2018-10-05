# codersbot-slack
Chatbot for slack

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

This bot uses [Python](https://www.python.org/downloads/) specifically version 3.6 so you'll need to make sure you are using the correct version of Python. We'll also use a number of python packages you can install through pip.

Here's a list of what we'll need:

- **[Python](https://www.python.org/downloads/)**, the programming language we're going to use.
- **[Pip](https://pip.pypa.io/en/stable/installing/)**, the Python package manager we'll use for installing packages we need.

Once you've installed Python and pip, you can install all additional dependent libraries using pip and the requirements.txt file included in this project, 
including [Flask](http://flask.pocoo.org/), a web development micro framework for Python and [python-slackclient](http://python-slackclient.readthedocs.io/en/latest/), a Slack client for Python.

```
pip install -r requirements.txt
```

We're going to use [ngrok](https://ngrok.com/) to expose our webserver to internet. This is mandatory to Slack API, which requires to use an HTTPS server.


## Deployment

To run the project locally and links to Slack you have to run our app.py

```
python app.py
```

Then we use ngrok to expose our webserver to internet with following command:
```
ngrok http 5000
```


## Authors

* **Pablo Vila** - *Initial work* - [pablovila](https://github.com/pablovila)

See also the list of [contributors](https://github.com/coders-cantabria/codersbot-slack/graphs/contributors) who participated in this project.
