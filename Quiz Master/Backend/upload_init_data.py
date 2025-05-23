from main import app
from application.sec import datastore
from application.models import db, Subject, Chapter, Quiz, User
from flask_security.utils import hash_password
import uuid
from datetime import datetime

# Example subjects and chapters
subjects_with_chapters = [
    {
        "name": "Mathematics",
        "description": "Study of numbers, quantities, and shapes.",
        "chapters": [
            {"name": "Algebra", "description": "Introduction to variables, equations, and expressions."},
            {"name": "Geometry", "description": "Study of shapes, angles, and measurements."},
        ]
    },
    {
        "name": "Science",
        "description": "Study of the natural world through experiments and observations.",
        "chapters": [
            {"name": "Physics", "description": "Study of matter, motion, and energy."},
            {"name": "Biology", "description": "Study of living organisms and ecosystems."},
        ]
    },
    {
        "name": "History",
        "description": "Study of past events and civilizations.",
        "chapters": [
            {"name": "Ancient History", "description": "Exploring early civilizations and empires."},
            {"name": "Modern History", "description": "Understanding significant events in modern times."},
        ]
    },
]

# Example quizzes
quizzes = [
    {
        "name": "Quiz1",
        "chapter_name": "Algebra",
        "date_of_quiz": "2025-01-15 10:00:00",
        "time_duration": "01:00",
        "remarks": "Basic algebra quiz for beginners."
    },
    {
        "name": "Quiz2",
        "chapter_name": "Physics",
        "date_of_quiz": "2025-01-20 12:00:00",
        "time_duration": "00:45",
        "remarks": "Physics quiz on motion and energy."
    }
]

with app.app_context():
    # Create the database tables
    db.create_all()

    # Create roles
    datastore.create_role(name="admin", description="User is an Admin")
    datastore.create_role(name="user", description="User is a User")
    db.session.commit()

    # Create admin user
    if not datastore.find_user(email="admin@gmail.com"):
        datastore.create_user(
            fullname="Admin User",
            email="admin@gmail.com",
            password=hash_password("admin"),
            roles=["admin"],
            qualification="N/A",
            dob=None,
            fs_uniquifier = str(uuid.uuid4()),
            active=True
        )
        print("Admin user created successfully.")

    # Add subjects, chapters, and quizzes
    for subject_data in subjects_with_chapters:
        subject = Subject.query.filter_by(name=subject_data["name"]).first()
        if not subject:
            subject = Subject(name=subject_data["name"], description=subject_data["description"])
            db.session.add(subject)
            db.session.flush()  # Ensures we can reference the subject_id immediately

            for chapter_data in subject_data["chapters"]:
                chapter = Chapter(
                    name=chapter_data["name"],
                    description=chapter_data["description"],
                    subject_id=subject.subject_id
                )
                db.session.add(chapter)
                db.session.flush()

                # Add quizzes for the chapter

                for quiz_data in quizzes:
                    if quiz_data["chapter_name"] == chapter.name:
                        # Convert date_of_quiz string to a datetime object
                        date_of_quiz = datetime.strptime(quiz_data["date_of_quiz"], "%Y-%m-%d %H:%M:%S")

                        # Create the Quiz object
                        quiz = Quiz(
                            name=quiz_data["name"],
                            chapter_id=chapter.chapter_id,
                            date_of_quiz=date_of_quiz,  # Use the converted datetime object
                            time_duration=quiz_data["time_duration"],
                            remarks=quiz_data["remarks"]
                        )
                        db.session.add(quiz)  # Add to session


    db.session.commit()
    print("Database initialized successfully!")
