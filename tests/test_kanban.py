from tests import credentials

t_user = credentials.T_User()
t_task = credentials.T_Task()

def login(client, username, password):
    """Login function that returns the response"""
    return client.post('/login', data=dict(
        email=username,
        password=password
    ), follow_redirects=True)

def add_task(client, title, descr, stat):

    """Function to add task and return the response"""

    return client.post('/', data=dict(
        title=title,
        descr=descr,
        stat = stat,
    ), follow_redirects=True)

def move_task(client, taskId, newstat):

    """Function to move a task and return the response"""
     
    client.post('/move-task', data='{ "taskId": "%i", "newStatus": "%s" }' % (taskId, newstat),
    follow_redirects=True)
    return client.get('/kanban')

def delete_task(client, taskId):

    """Function to delete a task and return the response"""

    client.post('/delete-task', data='{ "taskId": "%i" }' % (taskId),
    follow_redirects=True)
    return client.get('/kanban')

def test_add_task(client):

    "asserting that a task is added"

    login(client, t_user.username, t_user.password)
    
    rv = add_task(client, "another"+t_task.title, t_task.descr, t_task.stat)
    assert b'Task added!' in rv.data


def test_move_task(client):

    """asserting that a task is moved""" 
    
    login(client, t_user.username, t_user.password)
    add_task(client, "another"+t_task.title, t_task.descr, t_task.stat)

    rv = move_task(client, 1, "doing")
    assert b"moveTask(1, \'todo\')" in rv.data # if the status of the task has changed to doing, than the moving options should only be todo and done
    assert b"moveTask(1, \'done\')" in rv.data

def test_delete_task(client):

    """asserting that a task is deleted"""

    login(client, t_user.username, t_user.password)
    add_task(client, "another"+t_task.title, t_task.descr, t_task.stat)
    
    rv = delete_task(client, 1)
    assert b"deleteTask(1)" not in rv.data 

    

    