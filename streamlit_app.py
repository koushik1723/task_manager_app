import streamlit as st
import requests

# ----------------------------------
# CONFIG
# ----------------------------------
API_URL = "http://127.0.0.1:8000"  # Local FastAPI backend

st.set_page_config(page_title="Employee Task Management System", page_icon="🧑‍💼", layout="wide")


# ----------------------------------
# LOGIN FUNCTION
# ----------------------------------
def login_page():
    st.title("🧑‍💼 Employee Task Management System")
    st.subheader("🔐 Login")

    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")

    if st.button("Login"):
        response = requests.post(
            f"{API_URL}/auth/login",
            data={"username": username, "password": password}
        )

        if response.status_code == 200:
            data = response.json()
            token = data["access_token"]
            role = data["role"]

            st.session_state.token = token
            st.session_state.username = username
            st.session_state.role = role

            st.success("Login successful!")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password.")


# ----------------------------------
# ADMIN FUNCTIONS
# ----------------------------------
def admin_create_user():
    st.subheader("➕ Create New User (Admin)")

    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")
    role = st.selectbox("Role:", ["admin", "employee"])

    if st.button("Create User"):
        response = requests.post(
            f"{API_URL}/users/",
            json={"username": username, "password": password, "role": role},
            headers={"Authorization": f"Bearer {st.session_state.token}"}
        )

        if response.status_code == 200:
            st.success(f"User '{username}' created successfully!")
        else:
            st.error(response.text)


def admin_create_task():
    st.subheader("📝 Create New Task")

    title = st.text_input("Task Title:")
    description = st.text_area("Description:")
    status = st.selectbox("Status:", ["pending", "in_progress", "completed"])
    owner_id = st.number_input("Assign To (Employee ID):", min_value=1)

    if st.button("Create Task"):
        response = requests.post(
            f"{API_URL}/tasks/",
            json={
                "title": title,
                "description": description,
                "status": status,
                "owner_id": owner_id
            },
            headers={"Authorization": f"Bearer {st.session_state.token}"}
        )
        if response.status_code == 200:
            st.success("Task created successfully!")
        else:
            st.error(response.text)


def admin_view_tasks():
    st.subheader("📋 All Tasks")

    response = requests.get(
        f"{API_URL}/tasks/",
        headers={"Authorization": f"Bearer {st.session_state.token}"}
    )

    if response.status_code == 200:
        tasks = response.json()

        for task in tasks:
            st.write(f"### 🆔 Task ID: {task['id']}")
            st.write(f"📌 Title: {task['title']}")
            st.write(f"📝 Description: {task['description']}")
            st.write(f"📅 Status: `{task['status']}`")
            st.write(f"👤 Assigned to User ID: {task['owner_id']}")
            st.write("---")
    else:
        st.error(response.text)


# ----------------------------------
# EMPLOYEE FUNCTIONS
# ----------------------------------
def employee_view_tasks():
    st.subheader("🧑‍🔧 My Tasks")

    response = requests.get(
        f"{API_URL}/tasks/me",
        headers={"Authorization": f"Bearer {st.session_state.token}"}
    )

    if response.status_code == 200:
        tasks = response.json()

        for task in tasks:
            st.write(f"### Task ID: {task['id']}")
            st.write(f"📌 Title: {task['title']}")
            st.write(f"📝 Description: {task['description']}")
            st.write(f"📅 Status: `{task['status']}`")

            new_status = st.selectbox(
                f"Update Task {task['id']} Status:",
                ["pending", "in_progress", "completed"],
                key=f"status_{task['id']}"
            )

            if st.button(f"Update Task {task['id']}", key=f"btn_{task['id']}"):
                update_response = requests.patch(
                    f"{API_URL}/tasks/{task['id']}/status",
                    json={"status": new_status},
                    headers={"Authorization": f"Bearer {st.session_state.token}"}
                )

                if update_response.status_code == 200:
                    st.success("Task updated successfully!")
                    st.experimental_rerun()
                else:
                    st.error(update_response.text)

            st.write("---")
    else:
        st.error(response.text)


# ----------------------------------
# DASHBOARDS
# ----------------------------------
def admin_dashboard():
    st.title("👨‍💼 Admin Dashboard")

    menu = ["Create User", "Create Task", "View All Tasks"]
    choice = st.sidebar.radio("Admin Menu", menu)

    if choice == "Create User":
        admin_create_user()
    elif choice == "Create Task":
        admin_create_task()
    elif choice == "View All Tasks":
        admin_view_tasks()


def employee_dashboard():
    st.title("👨‍🔧 Employee Dashboard")
    employee_view_tasks()


# ----------------------------------
# APP ROUTER
# ----------------------------------
if "token" not in st.session_state:
    login_page()

else:
    role = st.session_state.role

    if role == "admin":
        admin_dashboard()
    else:
        employee_dashboard()

    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.experimental_rerun()
