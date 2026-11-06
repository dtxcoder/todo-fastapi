def test_get_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "running"}

def test_get_tasks(client):
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert response.json() == []

def test_get_task_by_id(client):
    payload = {
        "task_name": "pytest",
        "finished": False,
        }
    
    post_response = client.post("/tasks/", json=payload)
    
    assert post_response.status_code == 201

    task_id = post_response.json()["id"]
    
    get_response = client.get(f"/tasks/{task_id}")
    data = get_response.json()

    assert get_response.status_code == 200
    assert data["task_name"] == "pytest"
    assert data["finished"] == False
    assert "id" in data

def test_get_missing_task(client):
    response = client.get("/tasks/999999")

    assert response.status_code == 404

def test_post_task(client):
    payload = {
        "task_name": "pytest",
        "finished": False,
    }

    response = client.post("/tasks/", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert data["task_name"] == "pytest"
    assert data["finished"] == False
    assert 'id' in data

def test_patch_task(client):
    post_payload = {
        "task_name": "pytest",
        "finished": False,
    }

    post_response = client.post("/tasks/", json=post_payload)

    assert post_response.status_code == 201

    task_id = post_response.json()["id"]

    patch_payload = {
        "task_name": "py",
        "finished": True,
    }

    patch_response = client.patch(f"/tasks/{task_id}", json=patch_payload)

    assert patch_response.status_code == 200

    patch_data = patch_response.json()

    assert patch_data["task_name"] == "py"
    assert patch_data["finished"] is True

    get_response = client.get(f"/tasks/{task_id}")

    assert get_response.status_code == 200

    get_data = get_response.json()

    assert get_data["task_name"] == "py"
    assert get_data["finished"] is True

def test_patch_task_null(client):
    post_payload = {
            "task_name": "pytest",
            "finished": False,
        }
    
    post_response = client.post("/tasks/", json=post_payload)
    
    assert post_response.status_code == 201
    
    task_id = post_response.json()["id"]
    
    patch_payload = {
            "task_name": None,
            "finished": None,
        }
    
    patch_response = client.patch(f"/tasks/{task_id}", json=patch_payload)
    
    assert patch_response.status_code == 422

def test_patch_task_ignores_unknown_fields(client):
    post_payload = {
                "task_name": "pytest",
                "finished": False,
            }
        
    post_response = client.post("/tasks/", json=post_payload)
        
    assert post_response.status_code == 201
        
    task_id = post_response.json()["id"]
        
    patch_payload = {
                "task_name": "py",
                "finished": True,
                "user": "test_user"
            }
        
    patch_response = client.patch(f"/tasks/{task_id}", json=patch_payload)
        
    assert patch_response.status_code == 200

    get_response = client.get(f"/tasks/{task_id}")

    assert get_response.status_code == 200

    get_data = get_response.json()

    assert get_data["task_name"] == "py"
    assert get_data["finished"] is True
    assert "user" not in get_data

def test_patch_task_with_partial_payload(client):
    post_payload = {
                    "task_name": "pytest",
                    "finished": False,
                }
            
    post_response = client.post("/tasks/", json=post_payload)
            
    assert post_response.status_code == 201
        
    task_id = post_response.json()["id"]
            
    patch_payload = {
        "finished": True
        }
            
    patch_response = client.patch(f"/tasks/{task_id}", json=patch_payload)
            
    assert patch_response.status_code == 200
    
    get_response = client.get(f"/tasks/{task_id}")
    
    assert get_response.status_code == 200
    
    get_data = get_response.json()
    
    assert get_data["task_name"] == "pytest"
    assert get_data["finished"] is True

def test_patch_missing_task(client):
    payload = {"finished": "true"}
    response = client.patch("/tasks/999999", json=payload)

    assert response.status_code == 404

def test_patch_task_empty_payload(client):
    post_payload = {
        "task_name": "pytest",
        "finished": False,
        }
    
    post_response = client.post("/tasks/", json=post_payload)

    task_id = post_response.json()["id"]

    response = client.patch(f"/tasks/{task_id}", json={})

    data = response.json()

    assert response.status_code == 200
    assert data["task_name"] == "pytest"
    assert data["finished"] is False

def test_delete_task(client):
    post_payload = {
        "task_name": "pytest",
        "finished": False,
        }
            
    post_response = client.post("/tasks/", json=post_payload)
            
    assert post_response.status_code == 201
        
    task_id = post_response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}")

    assert delete_response.status_code == 204

    get_response = client.get(f"/tasks/{task_id}")

    assert get_response.status_code == 404

def test_delete_missing_task(client):
    delete_response = client.delete("/tasks/999999")
    assert delete_response.status_code == 404

def create_task(client, task_name: str, finished: bool = False):
    response = client.post(
        "/tasks/",
        json={"task_name": task_name, "finished": finished},
    )
    assert response.status_code == 201
    return response.json()


def test_get_tasks_with_default_pagination(client):
    for i in range(15):
        create_task(client, f"Task {i}")

    response = client.get("/tasks/")

    assert response.status_code == 200
    assert len(response.json()) == 10


def test_get_tasks_with_limit(client):
    for i in range(5):
        create_task(client, f"Task {i}")

    response = client.get("/tasks/?limit=3")

    assert response.status_code == 200
    assert len(response.json()) == 3


def test_get_tasks_with_offset(client):
    created_tasks = [
        create_task(client, f"Task {i}")
        for i in range(5)
    ]

    response = client.get("/tasks/?offset=2")

    assert response.status_code == 200
    assert [task["id"] for task in response.json()] == [
        task["id"] for task in created_tasks[2:]
    ]


def test_get_tasks_with_limit_and_offset(client):
    created_tasks = [
        create_task(client, f"Task {i}")
        for i in range(10)
    ]

    response = client.get("/tasks/?limit=3&offset=4")

    assert response.status_code == 200
    assert [task["id"] for task in response.json()] == [
        task["id"] for task in created_tasks[4:7]
    ]


def test_get_tasks_with_offset_beyond_available_records(client):
    for i in range(3):
        create_task(client, f"Task {i}")

    response = client.get("/tasks/?offset=10")

    assert response.status_code == 200
    assert response.json() == []


def test_get_tasks_with_limit_equal_to_one(client):
    for i in range(3):
        create_task(client, f"Task {i}")

    response = client.get("/tasks/?limit=1")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_tasks_with_zero_limit(client):
    response = client.get("/tasks/?limit=0")

    assert response.status_code == 422


def test_get_tasks_with_negative_limit(client):
    response = client.get("/tasks/?limit=-1")

    assert response.status_code == 422


def test_get_tasks_with_negative_offset(client):
    response = client.get("/tasks/?offset=-1")

    assert response.status_code == 422


def test_get_tasks_with_maximum_limit(client):
    for i in range(100):
        create_task(client, f"Task {i}")

    response = client.get("/tasks/?limit=100")

    assert response.status_code == 200
    assert len(response.json()) == 100


def test_get_tasks_with_limit_above_maximum(client):
    response = client.get("/tasks/?limit=101")

    assert response.status_code == 422