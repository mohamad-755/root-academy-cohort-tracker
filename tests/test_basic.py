def test_homepage_loads(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Welcome to Root Academy" in response.data


def test_student_can_register_and_login(client, auth):
    register_response = auth.register()

    assert b"Registration successful" in register_response.data

    login_response = auth.login()

    assert b"Test Student" in login_response.data
    assert b"Curriculum" in login_response.data


def test_curriculum_requires_login(client):
    response = client.get("/curriculum/")

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_logged_in_student_can_view_curriculum(client, auth):
    auth.register()
    auth.login()

    response = client.get("/curriculum/")

    assert response.status_code == 200
    assert b"Week 1" in response.data
    assert b"Week 2" in response.data


def test_student_can_submit_weekly_work(client, auth):
    auth.register()
    auth.login()

    response = client.post(
        "/submissions/week/1",
        data={
            "submission_url": "https://example.com/week-1",
            "note": "My Week 1 submission",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Submission saved" in response.data

def test_logged_in_student_can_view_submissions_dashboard(client, app):
    client.post(
        "/register",
        data={
            "name": "Test Student",
            "email": "student@example.com",
            "cohort_code": "ROOT2026",
        },
        follow_redirects=True,
    )

    client.post(
        "/login",
        data={
            "email": "student@example.com",
            "cohort_code": "ROOT2026",
        },
        follow_redirects=True,
    )

    response = client.get("/submissions/")

    assert response.status_code == 200
    assert b"My submissions" in response.data
    assert b"Week 1" in response.data
    assert b"Missing" in response.data