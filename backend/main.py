from flask import Flask
import os
from database import db
import workers
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from cache import cache


app=Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "database_files/library_management.db")
app.config["CELERY_BROKER_URL"] = "redis://localhost:6379/1"
app.config["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/2"

app.config["CACHE_TYPE"]='RedisCache'
app.config["CACHE_REDIS_URL"]='redis://localhost:6379/3'
app.config["CACHE_DEFAULT_TIMEOUT"]=200
app.config["REDIS_URL"] = "redis://localhost:6379"
app.config["broker_url"] = "redis://localhost:6379/0"
app.config["result_backend"] = "redis://localhost:6379/0"
app.config["broker_connection_retry_on_startup"] = True

db.init_app(app)

app.config["JWT_SECRET_KEY"]="supersecretkey"
jwt=JWTManager(app)


app.app_context().push()


celery=workers.celery
celery.conf.update(broker_url=app.config["CELERY_BROKER_URL"], result_backend=app.config["CELERY_RESULT_BACKEND"])
celery.Task=workers.ContextTask
app.app_context().push()
cache.init_app(app)
app.app_context().push()

CORS(app)


from controllers import *
from backend import *

if __name__=="__main__":
    app.run(host="localhost", port=8080, debug=True)