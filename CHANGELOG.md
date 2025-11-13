# Changelog

## [2.0.0] - 2025-11-13

### 🎉 Major Release: Random Book Store

Complete rebrand and feature upgrade with automatic book rotation.

### Added
- **🔄 Auto-Refresh Feature**: Books automatically refresh every 10 minutes with new random selections from Open Library
- **APScheduler Integration**: Background scheduler for periodic book updates
- **Configurable Intervals**: Set refresh interval via `BOOKS_REFRESH_INTERVAL_MINUTES` environment variable
- **Configurable Book Count**: Set number of books via `BOOKS_COUNT` environment variable
- **Enhanced Logging**: Emoji-based console output for better visibility

### Changed
- **Rebranded** from "Bookstore" to "**Random Book Store**"
- Updated all templates with new branding
- Updated all documentation (README, QUICKSTART, DEPLOYMENT, STRUCTURE)
- Enhanced homepage with dynamic messaging about catalog rotation
- Footer now displays "Books refresh every 10 minutes!"

### Technical Details
- Added `APScheduler==3.10.4` to requirements.txt
- New `refresh_books()` function for background catalog updates
- Scheduler starts automatically on app initialization
- Graceful shutdown handling with `atexit`
- Database is completely replaced during each refresh (no stale data)

### Configuration
```bash
# Default values
BOOKS_REFRESH_INTERVAL_MINUTES=10  # Refresh every 10 minutes
BOOKS_COUNT=12                      # Fetch 12 books per refresh
```

### Console Output
```
📚 Fetching initial books from Open Library API...
✅ Successfully added 12 books from Open Library!
📚 Book refresh scheduler started (every 10 minutes)
 * Running on http://127.0.0.1:8080

# After 10 minutes...
🔄 Refreshing books from Open Library API...
✅ Successfully refreshed with 12 new books!
```

---

## [1.0.0] - 2025-11-13

### Initial Release

- Flask-based e-commerce application
- Open Library API integration
- User authentication and shopping cart
- OpenShift deployment ready
- Health check endpoints
- Real book data with covers
