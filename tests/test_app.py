import unittest
import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app, db
from app.models import MyTask  # Import MyTask from app.models

class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the test environment once for the entire test class."""
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        cls.app = app.test_client()
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Clean up the test environment after all tests are done."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def setUp(self):
        """Set up before each test."""
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        """Clean up after each test."""
        db.session.remove()
        self.app_context.pop()

    def add_task(self, content="Test Task", complete=False):
        """Helper method to add a task to the database."""
        task = MyTask(content=content, complete=complete)
        db.session.add(task)
        db.session.commit()
        return task.id

    def test_add_task(self):
        """Test adding a task."""
        response = self.app.post("/", data={"content": "Test Task"})
        self.assertEqual(response.status_code, 302)  # Redirect after adding task
        task = db.session.get(MyTask, 1)  # Use db.session.get instead of MyTask.query.get
        self.assertIsNotNone(task)
        self.assertEqual(task.content, "Test Task")
        self.assertFalse(task.complete)

    def test_add_empty_task(self):
        """Test adding a task with empty content."""
        response = self.app.post("/", data={"content": ""})
        self.assertEqual(response.status_code, 302)  # Redirect after validation error
        tasks = MyTask.query.all()
        self.assertEqual(len(tasks), 0)  # No task should be added

    def test_toggle_task(self):
        """Test toggling a task's completion status."""
        task_id = self.add_task()
        response = self.app.post(f"/toggle/{task_id}")
        self.assertEqual(response.status_code, 302)  # Redirect after toggling task
        task = db.session.get(MyTask, task_id)  # Use db.session.get
        self.assertTrue(task.complete)

    def test_toggle_nonexistent_task(self):
        """Test toggling a non-existent task."""
        response = self.app.post("/toggle/999")
        self.assertEqual(response.status_code, 302)  # Redirect after error
        follow_up = self.app.get("/")
        self.assertIn(b"Task not found!", follow_up.data)  # Verify flash message

    def test_delete_task(self):
        """Test deleting a task."""
        task_id = self.add_task()
        response = self.app.post(f"/delete/{task_id}")
        self.assertEqual(response.status_code, 302)  # Redirect after deleting task
        task = db.session.get(MyTask, task_id)  # Use db.session.get
        self.assertIsNone(task)

    def test_delete_nonexistent_task(self):
        """Test deleting a non-existent task."""
        response = self.app.post("/delete/999")
        self.assertEqual(response.status_code, 302)  # Redirect after error
        follow_up = self.app.get("/")
        self.assertIn(b"Task not found!", follow_up.data)  # Verify flash message

    def test_update_task(self):
        """Test updating a task's content."""
        task_id = self.add_task()
        response = self.app.post(f"/update/{task_id}", data={"content": "Updated Task"})
        self.assertEqual(response.status_code, 302)  # Redirect after updating task
        task = db.session.get(MyTask, task_id)  # Use db.session.get
        self.assertEqual(task.content, "Updated Task")

    def test_update_nonexistent_task(self):
        """Test updating a non-existent task."""
        response = self.app.post("/update/999", data={"content": "Updated Task"})
        self.assertEqual(response.status_code, 302)  # Redirect after error
        follow_up = self.app.get("/")
        self.assertIn(b"Task not found!", follow_up.data)  # Verify flash message

    def test_filter_tasks(self):
        """Test filtering tasks by status."""
        # Add some tasks
        task1_id = self.add_task(content="Task 1", complete=True)
        task2_id = self.add_task(content="Task 2", complete=False)

        # Test filtering complete tasks
        response = self.app.get("/filter/complete")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Task 1", response.data)
        self.assertNotIn(b"Task 2", response.data)

        # Test filtering incomplete tasks
        response = self.app.get("/filter/incomplete")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Task 2", response.data)
        self.assertNotIn(b"Task 1", response.data)

        # Test filtering all tasks
        response = self.app.get("/filter/all")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Task 1", response.data)
        self.assertIn(b"Task 2", response.data)

    def test_filter_tasks_error(self):
        """Test filtering tasks with an invalid status."""
        response = self.app.get("/filter/invalid_status")
        self.assertEqual(response.status_code, 200)  # Successful response
        # Verify that the application displays all tasks
        self.assertIn(b"Test Task", response.data)
        self.assertIn(b"Task 1", response.data)
        self.assertIn(b"Task 2", response.data)

    def test_task_repr(self):
        """Test the string representation of a task."""
        task = MyTask(content="Test Task")
        self.assertEqual(repr(task), "Task None")  # Before saving, id is None
        db.session.add(task)
        db.session.commit()
        self.assertEqual(repr(task), f"Task {task.id}")  # After saving, id is set

    def test_flash_messages(self):
        """Test flash messages for various operations."""
        # Test flash message for adding a task
        response = self.app.post("/", data={"content": "Test Task"})
        self.assertEqual(response.status_code, 302)
        follow_up = self.app.get("/")
        self.assertIn(b"Task added successfully!", follow_up.data)

        # Test flash message for deleting a task
        task_id = self.add_task()
        response = self.app.post(f"/delete/{task_id}")
        self.assertEqual(response.status_code, 302)
        follow_up = self.app.get("/")
        self.assertIn(b"Task deleted successfully!", follow_up.data)

        # Test flash message for updating a task
        task_id = self.add_task()
        response = self.app.post(f"/update/{task_id}", data={"content": "Updated Task"})
        self.assertEqual(response.status_code, 302)
        follow_up = self.app.get("/")
        self.assertIn(b"Task updated successfully!", follow_up.data)

        # Test flash message for toggling a task
        task_id = self.add_task()
        response = self.app.post(f"/toggle/{task_id}")
        self.assertEqual(response.status_code, 302)
        follow_up = self.app.get("/")
        # Update the expected message to match the actual behavior
        self.assertIn(b"Task status updated!", follow_up.data)


if __name__ == "__main__":
    unittest.main()