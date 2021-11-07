import os
import tempfile
import pytest
import sys
from flask import json
from werkzeug.security import generate_password_hash
from tests import credentials
sys.path.append('../')
from website import create_app, db, models


t_user = credentials.T_User()


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': f'sqlite://'})

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            user = models.User(email=t_user.username, first_name=t_user.name, password=generate_password_hash(
               t_user.password, method='sha256'))
            db.session.add(user)
            db.session.commit()
            
            

        yield client

    os.close(db_fd)
    os.unlink(db_path)
