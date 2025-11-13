from flask import Flask
from flask_login import LoginManager
from config import Config
from app.models import db, User
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

login_manager = LoginManager()
scheduler = BackgroundScheduler()

def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)

    # Create tables
    with app.app_context():
        db.create_all()
        # Add sample books if database is empty
        from app.models import Book
        if Book.query.count() == 0:
            init_sample_data()

    # Start background scheduler for periodic book refresh
    if not scheduler.running:
        refresh_interval = app.config['BOOKS_REFRESH_INTERVAL_MINUTES']
        scheduler.add_job(
            func=lambda: refresh_books(app),
            trigger='interval',
            minutes=refresh_interval,
            id='refresh_books',
            name='Refresh books from Open Library',
            replace_existing=True
        )
        scheduler.start()
        print(f"📚 Book refresh scheduler started (every {refresh_interval} minutes)")

        # Shut down the scheduler when exiting the app
        atexit.register(lambda: scheduler.shutdown())

    return app

def refresh_books(app):
    """Background task to refresh books from Open Library API"""
    with app.app_context():
        from app.models import Book, db
        from app.openlibrary import fetch_random_books_for_store

        try:
            print("🔄 Refreshing books from Open Library API...")
            books_count = app.config['BOOKS_COUNT']

            # Delete all existing books
            Book.query.delete()

            # Fetch new books
            books_data = fetch_random_books_for_store(count=books_count)

            if not books_data:
                print("⚠️  Could not fetch new books, keeping database empty")
                return

            # Add new books
            for book_data in books_data:
                book = Book(
                    title=book_data['title'],
                    author=book_data['author'],
                    description=book_data['description'],
                    price=book_data['price'],
                    isbn=book_data['isbn'],
                    cover_image=book_data['cover_image'],
                    stock=book_data['stock']
                )
                db.session.add(book)

            db.session.commit()
            print(f"✅ Successfully refreshed with {len(books_data)} new books!")

        except Exception as e:
            print(f"❌ Error refreshing books: {e}")
            db.session.rollback()

def init_sample_data():
    """Initialize database with books from Open Library API"""
    from app.models import Book, db
    from app.openlibrary import fetch_random_books_for_store

    print("📚 Fetching initial books from Open Library API...")
    try:
        # Fetch books from Open Library
        books_data = fetch_random_books_for_store(count=12)

        if not books_data:
            print("Warning: Could not fetch books from API, using fallback data")
            # Fallback to a few hardcoded books if API fails
            books_data = [
                {
                    'title': "The Great Gatsby",
                    'author': "F. Scott Fitzgerald",
                    'description': "A classic American novel set in the Jazz Age",
                    'price': 12.99,
                    'isbn': "9780743273565",
                    'stock': 15,
                    'cover_image': "/static/images/book-placeholder.svg"
                },
                {
                    'title': "To Kill a Mockingbird",
                    'author': "Harper Lee",
                    'description': "A gripping tale of racial injustice and childhood innocence",
                    'price': 14.99,
                    'isbn': "9780061120084",
                    'stock': 20,
                    'cover_image': "/static/images/book-placeholder.svg"
                }
            ]

        # Add books to database
        for book_data in books_data:
            book = Book(
                title=book_data['title'],
                author=book_data['author'],
                description=book_data['description'],
                price=book_data['price'],
                isbn=book_data['isbn'],
                cover_image=book_data['cover_image'],
                stock=book_data['stock']
            )
            db.session.add(book)

        db.session.commit()
        print(f"✅ Successfully added {len(books_data)} books from Open Library!")

    except Exception as e:
        print(f"❌ Error initializing sample data: {e}")
        db.session.rollback()
