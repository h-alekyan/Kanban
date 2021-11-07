from werkzeug.security import generate_password_hash
from tests import credentials

t_user = credentials.T_User()


def test_first_entrance(client):
    """What the user should see when they first enter the app, without being logged in"""

    rv = client.get('/login')
    
    assert b'Login' in rv.data


def signup(client, email, firstname, password1, password2):
    """Signup function that returns the response"""
    return client.post('/sign-up', data={
            'email': email,
            'firstName': firstname,
            'password1': password1,
            'password2': password2,
        }, follow_redirects=True)


def login(client, username, password):
    """Login function that returns the response"""
    return client.post('/login', data=dict(
        email=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    """Logout function that returns the response"""
    return client.get('/logout', follow_redirects=True)


def test_signup(client):
    """Testing signup with a new user (we already have one user in the databse, which we use for login, logout and task manipulation tests)"""
    rv = signup(client, 'test_user2@test.com', "Tester", 'password123', 'password123' )
    assert b'Account created!' in rv.data # this message is only flashed after the user is added to the database.


def test_login(client):
    """Make sure login works with appropriate flashes for correct credentials"""
    

    rv = login(client, t_user.username, t_user.password)

    assert b'Welcome' in rv.data # User sees a welcome message only when they are logged in

    assert b'My Tasks' in rv.data # Once logged in they should see a new tab in the menu called my tasks

    assert b'Login' not in rv.data # A logged in user should not see a log in option

    assert b'Logout' in rv.data # A logged in user should see a log out option

    logout(client)

def test_incorrect_login(client):
    """Assert that the login flashes correct error messages for wrong email or password"""

    rv = login(client, f"{t_user.username}x", t_user.password)
    assert b'Email does not exist.' in rv.data

    rv = login(client, t_user.username, f'{t_user.password}x')
    assert b'Incorrect password, try again.' in rv.data


def test_logout(client):
    """Assert logout works correctly and that the user sees the right menu items"""


    login(client, t_user.username, t_user.password)

    rv = logout(client)
    assert b'Logged out successfully!' in rv.data

    assert b'Logout' not in rv.data # Logged out user should not see a logout option

    assert b'Login' in rv.data # They should see a login option

    assert b'My Tasks' not in rv.data # Should not have access to the kanban board
    
