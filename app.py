from flask import Flask
import config
from exts import db, cors
from flask_migrate import Migrate
from models import User, Project, UserProject
from bluePrint.users import users_bp
from bluePrint.project import project_bp
from bluePrint.userproject import userproject_bp
from bluePrint.auth import auth_bp


app = Flask(__name__)
app.config.from_object(config)

app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(project_bp, url_prefix='/projects')
app.register_blueprint(userproject_bp, url_prefix='/up')
app.register_blueprint(auth_bp, url_prefix='/auth')

db.init_app(app)
cors.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def hello():
    return 'hello'

if __name__ == '__main__':
    app.run(debug=True)
