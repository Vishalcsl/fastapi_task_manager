import json
from fastapi import status


def test_create_job(client, normal_user_token_headers):
    data = {
        "title": "Finish building task manager",
        "description": "python fastapi docker",
        "date_posted": "2021-12-22",
        "completion_by": "2021-12-23",
        "location": "Varanasi, India",
        }
    response = client.post("/tasks/create-task/",data=json.dumps(data), headers=normal_user_token_headers)
    assert response.status_code == 200 
    assert response.json()["title"] == "Finish building task manager"
    assert response.json()["description"] == "python fastapi docker"

def test_read_task(client):
    data = {
        "title": "Task2",
        "description": "description for task2",
        "date_posted": "2021-12-22",
        "completion_by": "2021-12-23",
        "location": "Varanasi, India",
        }
    response = client.post("/tasks/create-task/",json.dumps(data))

    response = client.get("/tasks/get/1")
    assert response.status_code == 200
    assert response.json()['title'] == "Task2"


def test_read_owner_tasks(client):
    data = {
        "title": "Task3",
        "description": "description for task3",
        "date_posted": "2021-12-22",
        "completion_by": "2021-12-23",
        "location": "Varanasi, India",
        }
    response = client.post("/tasks/create-task/",json.dumps(data))
    response = client.post("/tasks/create-task/",json.dumps(data))

    response = client.get("/tasks/task-details/1")
    assert response.status_code == 200
    assert response.json()[0] 
    assert response.json()[1]


def test_update_a_task(client):
    data={
        "title": "Task4",
        "description": "description for task4",
        "date_posted": "2021-12-22",
        "completion_by": "2021-12-24",
        "location": "Varanasi, India",
    }

    client.post("/tasks/create-task/", json.dumps(data))
    data["title"] = "New Task4"
    response = client.put("/tasks/update/1", json.dumps(data))
    assert response.json()["msg"] == "Successfully updated data."


def test_delete_a_task(client):
    data={
        "title": "Task5",
        "description": "description for task5",
        "date_posted": "2021-12-22",
        "completion_by": "2021-12-24",
        "location": "Hyderabad, India",
    }

    client.post("/tasks/create-task/", json.dumps(data))
    msg= client.delete("/tasks/delete/1")
    response = client.get("/tasks/get/1/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
