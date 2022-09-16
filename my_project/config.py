# file to configure flask, loaded into our flask application
# using the line: app.config.from_pyfile("config.py") in website.py
from os import environ

# These variables be available to your application to use.
# Things that may be different on different computers, like a path to a file,
# should go in here. This is all available in GitHub, so be careful.

# For example, you can add the port you wish to run on as a variable.
# This can then be used when running the code.
MY_PORT = "5000"

#DATABASE_PASSWORD = environ.get("DB_PASSWORD")

SQLALCHEMY_DATABASE_URI = "sqlite:///lottery.db"

SQLALCHEMY_TRACK_MODIFICATIONS = False  # TODO google das noch mal

SECRET_KEY = "cc2e80bcdacafd93c0dc468f5318416d8ba00a836a938598287c717170fb4a99"