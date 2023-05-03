from os import path, getenv

basedir = path.abspath(path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = f'postgresql://{getenv("POSTGRES_USER", "postgres")}:{getenv("POSTGRES_PASSWORD", "postgres")}@{getenv("POSTGRES_HOST", "db")}:5432/{getenv("POSTGRES_DB", "postgres")}'
    SECRET_KEY = getenv('SECRET', "Wm<n]Q8f#^^Fzj(")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
