# Quick Start Guide

Get the Random Book Store app running in minutes! Watch the catalog automatically refresh with new books every 10 minutes.

## Run Locally

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd store-app
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python wsgi.py
```

**First run output:**
```
📚 Fetching initial books from Open Library API...
✅ Successfully added 12 books from Open Library!
📚 Book refresh scheduler started (every 10 minutes)
 * Running on http://127.0.0.1:8080
```

### 5. Access the App

Open your browser to: **http://localhost:8080**

### 6. Test the App

1. Click "Register" and create an account
2. Browse the catalog (12 real books from Open Library!)
3. Add books to cart
4. View cart and checkout
5. Wait 10 minutes and refresh - see entirely new books!

## Reset Database (Optional)

Get fresh books from Open Library:

```bash
rm random-book-store.db
python wsgi.py
```

---

## Configuration

### Change Refresh Interval

Set how often books refresh (default: 10 minutes):

```bash
# Refresh every 5 minutes
export BOOKS_REFRESH_INTERVAL_MINUTES=5
python wsgi.py

# Or in OpenShift
oc set env deployment/random-book-store BOOKS_REFRESH_INTERVAL_MINUTES=5
```

### Change Book Count

Set how many books to fetch (default: 12):

```bash
export BOOKS_COUNT=20
python wsgi.py
```

---

## Deployment

See the [DEPLOYMENT.md](./DEPLOYMENT.md) guide for instructions on deploying to OpenShift.
