# Random Book Store - OpenShift Deployment

A dynamic Flask-based bookstore that automatically refreshes with random books from Open Library every 10 minutes, designed for deployment on OpenShift.

## Features

- **🔄 Auto-Refreshing Catalog**: Books automatically refresh every 10 minutes (configurable) with new random selections from Open Library
- **📚 Real Book Data**: Fetches actual books from Open Library API with covers, titles, authors, and ISBNs
- **🏠 Homepage**: Welcome page with featured books and cover images
- **📖 Book Catalog**: Browse all available books with pagination and cover art
- **🔍 Book Details**: Individual book pages with large cover images from Open Library
- **🔐 User Authentication**: Secure register and login with password hashing
- **🛒 Shopping Cart**: Add/remove books, update quantities (with thumbnails)
- **💳 Checkout**: Simple checkout process (demo only, no payment processing)
- **❤️ Health Checks**: Built-in liveness and readiness probes for Kubernetes/OpenShift

## Technology Stack

- **Backend**: Python 3.12, Flask 3.0, Flask-Login, Flask-SQLAlchemy
- **Scheduler**: APScheduler for automatic book rotation
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Frontend**: HTML5, CSS3, Bootstrap 5, Jinja2 templates
- **API Integration**: Open Library API for real book data
- **WSGI Server**: Gunicorn (production)
- **Container**: Red Hat UBI9 Python 3.12
- **Deployment**: OpenShift 4.x / Kubernetes 1.24+

## Project Structure

```
store-app/
├── app/
│   ├── __init__.py          # Application factory, database init
│   ├── models.py            # Database models (User, Book, CartItem)
│   ├── openlibrary.py       # Open Library API integration
│   ├── routes.py            # Flask routes and views
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css    # Custom styles
│   │   └── images/
│   │       └── book-placeholder.svg  # Fallback book cover
│   └── templates/           # Jinja2 HTML templates
│       ├── base.html        # Base layout
│       ├── index.html       # Homepage
│       ├── catalog.html     # Book catalog
│       ├── book_detail.html # Book details
│       ├── cart.html        # Shopping cart
│       ├── checkout.html    # Checkout
│       ├── login.html       # Login
│       └── register.html    # Registration
├── openshift/               # OpenShift/Kubernetes manifests
│   ├── all-in-one.yaml      # Single-file deployment
│   ├── deployment.yaml      # Deployment config
│   ├── service.yaml         # Service definition
│   ├── route.yaml           # Route (external access)
│   ├── secret.yaml          # Application secrets
│   ├── pvc.yaml            # Persistent volume claim
│   └── DEPLOYMENT.md        # Detailed deployment guide
├── config.py               # Application configuration
├── wsgi.py                 # WSGI entry point (S2I compatible)
├── Dockerfile              # Container image definition
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── QUICKSTART.md           # Quick start guide
├── .dockerignore           # Docker ignore rules
└── .gitignore              # Git ignore rules

```

## Book Data Source & Auto-Refresh

The application uses the **Open Library API** (https://openlibrary.org) to dynamically populate the catalog:

### Initial Load
- **On first run**: Automatically fetches 12 trending books from multiple subjects
- **Real data**: Actual book titles, authors, ISBNs, publication dates, and cover images
- **Cover images**: Served from Open Library's CDN (`covers.openlibrary.org`)

### Automatic Refresh
- **Every 10 minutes** (configurable): Background scheduler fetches fresh random books
- **Complete rotation**: Old books are replaced with entirely new selections

### Book Selection
- **Filtering**: Only books with ISBNs and cover images
- **Demo pricing**: Prices ($9.99-$24.99) and stock (5-30 units) are randomized for demonstration

### Configuration
Set via environment variables:
- `BOOKS_REFRESH_INTERVAL_MINUTES=10` - Refresh every 10 minutes (default)
- `BOOKS_COUNT=12` - Number of books to fetch (default)

## Testing the Application

1. Register a new account
2. Browse the catalog
3. Add books to cart
4. View and update cart
5. Complete checkout
