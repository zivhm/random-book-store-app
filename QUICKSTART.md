# Quick Start Guide

Get the Random Book Store app running in minutes! Watch the catalog automatically refresh with new books every 10 minutes.

## Run Locally (Development)

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
rm random-bookstore.db
python wsgi.py
```

---

## Deploy to OpenShift

### Option 1: Quick Deploy (Container Image)

```bash
# 1. Build container
podman build -t random-bookstore:latest .

# 2. Tag for your registry
podman tag random-bookstore:latest quay.io/<your-username>/random-bookstore:latest

# 3. Push to registry
podman push quay.io/<your-username>/random-bookstore:latest

# 4. Update image in deployment
sed -i 's|image: bookstore:latest|image: quay.io/<your-username>/random-bookstore:latest|' openshift/all-in-one.yaml

# 5. Deploy everything
oc apply -f openshift/all-in-one.yaml

# 6. Get your app URL
oc get route random-bookstore
```

Visit the URL and your app is live! 🎉

### Option 2: Source-to-Image (S2I)

Let OpenShift build the container for you:

```bash
# Create app from Git
oc new-app python:3.12~https://github.com/<your-repo>/store-app --name=random-bookstore

# Expose externally
oc expose svc/random-bookstore

oc get route random-bookstore
```

### Option 3: Docker Build & Deploy

```bash
# Build with Docker
docker build -t random-bookstore:latest .
docker tag random-bookstore:latest <registry>/random-bookstore:latest
docker push <registry>/random-bookstore:latest

# Update and deploy
oc apply -f openshift/all-in-one.yaml
```

---

## Verification

### Check Deployment Status

```bash
# View pods
oc get pods

# View logs
oc logs -f deployment/random-bookstore

# Check route
oc get route random-bookstore```

### Test Health Endpoints

```bash
ROUTE=$(oc get route random-bookstore -o jsonpath='{.spec.host}')

# Liveness probe
curl https://$ROUTE/health

# Readiness probe
curl https://$ROUTE/ready
```

---

## Next Steps

1. **Register an account** on your deployed app
2. **Browse the catalog** - See real books from Open Library
3. **Customize** - Modify code and redeploy

## Need Help?

- **Detailed deployment**: See `openshift/DEPLOYMENT.md`
- **App overview**: See `README.md`
- **Troubleshooting**: Check pod logs with `oc logs -f deployment/random-bookstore`

---

**Built with ❤️ using Flask, Open Library API, APScheduler, and OpenShift**

## Configuration

### Change Refresh Interval

Set how often books refresh (default: 10 minutes):

```bash
# Refresh every 5 minutes
export BOOKS_REFRESH_INTERVAL_MINUTES=5
python wsgi.py

# Or in OpenShift
oc set env deployment/random-bookstore BOOKS_REFRESH_INTERVAL_MINUTES=5
```

### Change Book Count

Set how many books to fetch (default: 12):

```bash
export BOOKS_COUNT=20
python wsgi.py
```
