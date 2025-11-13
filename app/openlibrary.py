"""
Open Library API integration module
Fetches book data from openlibrary.org
"""
import requests
import random
from typing import List, Dict, Optional


def fetch_trending_books(subject: str = "fiction", limit: int = 50) -> List[Dict]:
    """
    Fetch trending books from Open Library API

    Args:
        subject: Subject category (e.g., 'fiction', 'science', 'history')
        limit: Number of books to fetch

    Returns:
        List of book dictionaries with title, author, isbn, etc.
    """
    url = "https://openlibrary.org/search.json"
    params = {
        "subject": subject,
        "sort": "trending",
        "limit": limit,
        "fields": "key,title,author_name,cover_i,first_publish_year,isbn,number_of_pages_median,publisher"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get('docs', [])
    except Exception as e:
        print(f"Error fetching books from Open Library: {e}")
        return []


def fetch_books_from_multiple_subjects(subjects: List[str], books_per_subject: int = 20) -> List[Dict]:
    """
    Fetch books from multiple subjects

    Args:
        subjects: List of subject categories
        books_per_subject: Number of books to fetch per subject

    Returns:
        Combined list of books from all subjects
    """
    all_books = []
    for subject in subjects:
        books = fetch_trending_books(subject, books_per_subject)
        all_books.extend(books)
    return all_books


def get_cover_url(cover_id: Optional[int], size: str = "M") -> str:
    """
    Generate Open Library cover URL

    Args:
        cover_id: Cover image ID from API
        size: S (small), M (medium), or L (large)

    Returns:
        Cover image URL or placeholder
    """
    if cover_id:
        return f"https://covers.openlibrary.org/b/id/{cover_id}-{size}.jpg"
    return "/static/images/book-placeholder.svg"


def parse_book_for_database(book_data: Dict) -> Optional[Dict]:
    """
    Parse Open Library book data into database-ready format

    Args:
        book_data: Raw book data from API

    Returns:
        Dictionary with keys: title, author, description, price, isbn, cover_image, stock
    """
    # Skip books without essential data
    if not book_data.get('title') or not book_data.get('author_name'):
        return None

    # Get first author
    author = book_data['author_name'][0] if book_data.get('author_name') else "Unknown Author"

    # Get ISBN (prefer ISBN-13, fallback to ISBN-10)
    isbn_list = book_data.get('isbn', [])
    isbn = None
    if isbn_list:
        # Prefer 13-digit ISBN
        isbn_13 = [i for i in isbn_list if len(i) == 13]
        isbn_10 = [i for i in isbn_list if len(i) == 10]
        isbn = isbn_13[0] if isbn_13 else (isbn_10[0] if isbn_10 else isbn_list[0])

    # Generate a simple description from available data
    description_parts = []
    if book_data.get('first_publish_year'):
        description_parts.append(f"First published in {book_data['first_publish_year']}.")
    if book_data.get('publisher'):
        publishers = book_data['publisher'][:2]  # First 2 publishers
        description_parts.append(f"Published by {', '.join(publishers)}.")
    if book_data.get('number_of_pages_median'):
        description_parts.append(f"Approximately {book_data['number_of_pages_median']} pages.")

    description = " ".join(description_parts) if description_parts else "A great book from Open Library's collection."

    # Random price between $9.99 and $24.99
    price = round(random.uniform(9.99, 24.99), 2)

    # Random stock between 5 and 30
    stock = random.randint(5, 30)

    # Get cover image
    cover_image = get_cover_url(book_data.get('cover_i'))

    return {
        'title': book_data['title'][:200],  # Limit to model field length
        'author': author[:100],  # Limit to model field length
        'description': description,
        'price': price,
        'isbn': isbn,
        'cover_image': cover_image,
        'stock': stock
    }


def fetch_random_books_for_store(count: int = 12) -> List[Dict]:
    """
    Fetch random books suitable for the bookstore

    Args:
        count: Number of books to fetch

    Returns:
        List of database-ready book dictionaries
    """
    # Define subjects to fetch from
    subjects = [
        "fiction",
        "science_fiction",
        "mystery",
        "romance",
        "fantasy",
        "history",
        "biography",
        "science"
    ]

    # Fetch books from random subjects
    selected_subjects = random.sample(subjects, min(4, len(subjects)))
    all_books = fetch_books_from_multiple_subjects(selected_subjects, books_per_subject=30)

    # Parse and filter books
    parsed_books = []
    for book_data in all_books:
        parsed = parse_book_for_database(book_data)
        if parsed and parsed['isbn']:  # Only include books with ISBN
            parsed_books.append(parsed)

    # Remove duplicates based on ISBN
    seen_isbns = set()
    unique_books = []
    for book in parsed_books:
        if book['isbn'] not in seen_isbns:
            seen_isbns.add(book['isbn'])
            unique_books.append(book)

    # Shuffle and return requested count
    random.shuffle(unique_books)
    return unique_books[:count]
