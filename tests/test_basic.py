def register_and_login_student(client):
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

def login_admin(client):
    client.post(
        "/admin/login",
        data={"admin_code": "test-admin-code"},
        follow_redirects=True,
    )

def test_admin_can_review_submission(client):
    register_and_login_student(client)

    client.post(
        "/submissions/week/1",
        data={
            "submission_url": "https://example.com/week-1",
            "note": "My week 1 work",
        },
        follow_redirects=True,
    )

    client.get("/logout")
    login_admin(client)

    response = client.get("/admin/submissions/1/review")

    assert response.status_code == 200
    assert b"Review Week 1 Submission" in response.data
    assert b"https://example.com/week-1" in response.data
    assert b"My week 1 work" in response.data

def test_admin_can_save_feedback_and_student_can_view_it(client):
    register_and_login_student(client)

    client.post(
        "/submissions/week/1",
        data={
            "submission_url": "https://example.com/week-1",
            "note": "My week 1 work",
        },
        follow_redirects=True,
    )

    client.get("/logout")
    login_admin(client)

    client.post(
        "/admin/submissions/1/review",
        data={"feedback": "Strong start. Add more explanation."},
        follow_redirects=True,
    )

    client.get("/admin/logout")

    client.post(
        "/login",
        data={
            "email": "student@example.com",
            "cohort_code": "ROOT2026",
        },
        follow_redirects=True,
    )

    response = client.get("/submissions/week/1")

    assert response.status_code == 200
    assert b"Strong start. Add more explanation." in response.data

def test_admin_can_send_suppressed_reminders(client):
    register_and_login_student(client)
    client.get("/logout")
    login_admin(client)

    response = client.post(
        "/admin/reminders/week/1",
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Sent 1 reminder email(s) for Week 1." in response.data

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

def test_admin_dashboard_requires_admin_login(client):
    response = client.get("/admin/")

    assert response.status_code == 302
    assert "/admin/login" in response.headers["Location"]

def test_admin_can_log_in(client):
    response = client.post(
        "/admin/login",
        data={"admin_code": "test-admin-code"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Admin dashboard" in response.data

def test_admin_dashboard_shows_registered_students(client):
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
        "/admin/login",
        data={"admin_code": "test-admin-code"},
        follow_redirects=True,
    )

    response = client.get("/admin/")

    assert response.status_code == 200
    assert b"Test Student" in response.data
    assert b"student@example.com" in response.data
    