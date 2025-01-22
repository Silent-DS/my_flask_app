Here’s an improved version of your `README.md` file. It includes more details, better formatting, and additional sections to make it more informative and user-friendly.

---

# My Flask Task App

A simple and efficient Flask application for managing tasks. This app allows you to add, update, delete, and toggle tasks, as well as filter them by completion status. It uses SQLite as the database for storing tasks.

---

## Features

- **Add Tasks**: Easily add new tasks with a description.
- **Update Tasks**: Modify the content of existing tasks.
- **Delete Tasks**: Remove tasks you no longer need.
- **Toggle Task Status**: Mark tasks as complete or incomplete.
- **Filter Tasks**: View tasks based on their completion status (all, complete, or incomplete).
- **SQLite Database**: Lightweight and easy-to-use database for storing tasks.

---

## Installation

Follow these steps to set up the application on your local machine.

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Silent-DS/MY_FLASK_APP.git
   cd MY_FLASK_APP
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**:
   ```bash
   flask db upgrade
   ```

5. **Run the application**:
   ```bash
   flask run
   ```

6. **Access the app**:
   Open your browser and go to `http://127.0.0.1:5000`.

---

## Usage

### Adding a Task
1. Enter the task description in the input field.
2. Click **Add Task**.

### Updating a Task
1. Click the **Update** button next to the task you want to modify.
2. Enter the new task description and click **Update**.

### Deleting a Task
1. Click the **Delete** button next to the task you want to remove.

### Toggling Task Status
1. Click the **Mark Complete** or **Mark Incomplete** button to toggle the task's status.

### Filtering Tasks
- Use the filter options at the top of the page to view:
  - **All Tasks**
  - **Complete Tasks**
  - **Incomplete Tasks**

---

## Project Structure

```
MY_FLASK_APP/
├── app/
│   ├── __init__.py         # Flask application factory
│   ├── models.py           # Database models
│   ├── routes.py           # Application routes
│   ├── templates/          # HTML templates
│   └── static/             # Static files (CSS, JS, etc.)
├── tests/                  # Unit tests
│   └── test_app.py
├── migrations/             # Database migrations
├── requirements.txt        # Project dependencies
├── config.py               # Configuration settings
└── README.md               # Project documentation
```

---

## Running Tests

To ensure the application works as expected, run the included unit tests:

```bash
python -m unittest discover tests
```

---


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
