from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend/templates')

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('../db/anime.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_media_list(media_type='anime', page=1, search_query='', genre_filter='all'):
    conn = get_db_connection()
    c = conn.cursor()
    
    # If 'all' is selected, combine results from all tables
    if media_type == 'all':
        # Get results from all tables
        anime_query = "SELECT * FROM anime WHERE 1=1"
        movies_query = "SELECT * FROM movies WHERE 1=1"
        series_query = "SELECT * FROM best_series WHERE 1=1"
        
        # Add filters if applicable
        if search_query:
            anime_query += f" AND LOWER(title) LIKE LOWER('%{search_query}%')"
            movies_query += f" AND LOWER(title) LIKE LOWER('%{search_query}%')"
            series_query += f" AND LOWER(title) LIKE LOWER('%{search_query}%')"
            
        if genre_filter != 'all':
            anime_query += f" AND genre LIKE '%{genre_filter}%'"
            movies_query += f" AND genre LIKE '%{genre_filter}%'"
            series_query += f" AND genre LIKE '%{genre_filter}%'"
        
        # Execute queries and combine results
        c.execute(anime_query)
        anime_results = c.fetchall()
        c.execute(movies_query)
        movies_results = c.fetchall()
        c.execute(series_query)
        series_results = c.fetchall()
        
        # Combine and sort results
        media_list = sorted(
            anime_results + movies_results + series_results,
            key=lambda x: x['rating'],
            reverse=True
        )
        
        # Get unique genres from all tables
        c.execute("SELECT DISTINCT genre FROM anime")
        anime_genres = {row[0] for row in c.fetchall()}
        c.execute("SELECT DISTINCT genre FROM movies")
        movies_genres = {row[0] for row in c.fetchall()}
        c.execute("SELECT DISTINCT genre FROM best_series")
        series_genres = {row[0] for row in c.fetchall()}
        genres = list(anime_genres.union(movies_genres).union(series_genres))
        
        # Calculate pagination
        total_results = len(media_list)
        per_page = 8
        total_pages = (total_results + per_page - 1) // per_page
        offset = (page - 1) * per_page
        
        # Apply pagination
        media_list = media_list[offset:offset + per_page]
    else:
        # Single table query
        table = 'anime' if media_type == 'anime' else ('movies' if media_type == 'movies' else 'best_series')
        
        # Build base query with DISTINCT to prevent duplicates
        query = f"SELECT DISTINCT * FROM {table} WHERE 1=1"
        
        # Add search filter
        if search_query:
            query += f" AND LOWER(title) LIKE LOWER('%{search_query}%')"
            
        # Add genre filter
        if genre_filter != 'all':
            # Handle comma-separated genres by checking if the genre is in the genre list
            query += f" AND (',' || genre || ',' LIKE '%,{genre_filter},%' OR genre = '{genre_filter}')"
            
        print(f"Executing query: {query}")
        c.execute(query)
        total_results = len(c.fetchall())
        
        # Add pagination
        per_page = 8
        total_pages = (total_results + per_page - 1) // per_page
        offset = (page - 1) * per_page
        query += f" ORDER BY rating DESC LIMIT {per_page} OFFSET {offset}"
        
        # Execute query
        c.execute(query)
        media_list = c.fetchall()
        
        # Get genres
        c.execute(f"SELECT DISTINCT genre FROM {table}")
        genres = [row[0] for row in c.fetchall()]
    
    # Calculate pagination
    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if page < total_pages else None
    
    conn.close()
    
    return {
        'media_list': media_list,
        'current_page': page,
        'total_pages': total_pages,
        'genres': genres,
        'prev_page': prev_page,
        'next_page': next_page,
        'search_query': search_query,
        'genre_filter': genre_filter
    }

@app.route('/')
def index():
    media_type = request.args.get('type', 'anime')
    page = int(request.args.get('page', 1))
    search_query = request.args.get('search', '')
    genre_filter = request.args.get('genre', 'all')
    
    media_data = get_media_list(media_type, page, search_query, genre_filter)
    
    return render_template('index.html', 
                         media_type=media_type,
                         media_list=media_data['media_list'],
                         current_page=media_data['current_page'],
                         total_pages=media_data['total_pages'],
                         genres=media_data['genres'],
                         prev_page=media_data['prev_page'],
                         next_page=media_data['next_page'],
                         search_query=media_data['search_query'],
                         genre_filter=media_data['genre_filter'])

@app.route('/filter')
def filter_media():
    try:
        media_type = request.args.get('type', 'all')
        page = request.args.get('page', 1, type=int)
        search_query = request.args.get('search', '')
        genre_filter = request.args.get('genre', 'all')
        
        print(f"Filtering media - Type: {media_type}, Page: {page}, Search: '{search_query}', Genre: {genre_filter}")
        
        # Get all media types if 'all' is selected
        if media_type == 'all':
            tables = ['anime', 'movies', 'best_series']
        else:
            tables = [media_type]
        
        all_media = []
        all_genres = set()
        
        # Process each table
        for table in tables:
            query = f"SELECT * FROM {table} WHERE 1=1"
            
            # Add search filter
            if search_query:
                query += f" AND LOWER(title) LIKE LOWER('%{search_query}%')"
                
            # Add genre filter (case-insensitive and handles spaces/punctuation)
            if genre_filter != 'all':
                # Clean up the genre filter
                genre_filter = genre_filter.lower().strip()
                # Handle case where genre is None or empty
                # Normalize the genre filter and handle different formats
                normalized_filter = genre_filter.lower().strip()
                
                # Build the query to handle various formats
                query += f"""
                AND (
                    -- Exact match (case insensitive)
                    LOWER(TRIM(genre)) = LOWER('{normalized_filter}') 
                    
                    -- Genre at start of string
                    OR LOWER(TRIM(genre)) LIKE LOWER('{normalized_filter},%')
                    
                    -- Genre in middle of string (surrounded by commas)
                    OR LOWER(TRIM(genre)) LIKE LOWER('%, {normalized_filter},%')
                    OR LOWER(TRIM(genre)) LIKE LOWER('%,{normalized_filter},%')
                    
                    -- Genre at end of string
                    OR LOWER(TRIM(genre)) LIKE LOWER('%, {normalized_filter}')
                    OR LOWER(TRIM(genre)) LIKE LOWER('%,{normalized_filter}')
                    
                    -- Handle genres with spaces
                    OR LOWER(TRIM(genre)) LIKE LOWER('% {normalized_filter} %')
                    OR LOWER(TRIM(genre)) LIKE LOWER('{normalized_filter} %')
                    OR LOWER(TRIM(genre)) LIKE LOWER('% {normalized_filter}%')
                )
                """
            
            # Execute query
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            items = cursor.fetchall()
            conn.close()
            
            # Convert to list of dicts for JSON
            result = [dict(item) for item in items]
            
            # If no results and a genre filter is active
            if not result and genre_filter != 'all':
                return jsonify({
                    'status': 'not_found',
                    'message': f'No items found for genre: {genre_filter}'
                })
                
            # Add type to each result
            for row in result:
                row['type'] = table  # Add type information
                all_media.append(row)
            
            # Get unique genres
            conn = get_db_connection()
            c = conn.cursor()
            c.execute(f"SELECT DISTINCT genre FROM {table}")
            for row in c.fetchall():
                if row['genre']:
                    genres = [g.strip() for g in row['genre'].split(',')]
                    all_genres.update(genres)
            
            conn.close()
        
        # Sort by rating (highest first)
        all_media.sort(key=lambda x: float(x.get('rating', 0)), reverse=True)
        
        # Pagination
        per_page = 8
        total_results = len(all_media)
        total_pages = max(1, (total_results + per_page - 1) // per_page)
        
        # Ensure page is within valid range
        page = max(1, min(page, total_pages))
        
        # Calculate start and end indices for pagination
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_media = all_media[start_idx:end_idx]
        offset = (page - 1) * per_page
        paginated_media = all_media[offset:offset + per_page]
        
        # Calculate pagination
        prev_page = page - 1 if page > 1 else None
        next_page = page + 1 if page < total_pages else None
        
        return jsonify({
            'status': 'success',
            'media': paginated_media,
            'total_pages': total_pages,
            'current_page': page,
            'total_results': total_results,
            'genres': sorted(list(all_genres)),
            'media_type': media_type,
            'genre_filter': genre_filter,
            'has_prev': page > 1,
            'has_next': page < total_pages,
            'prev_page': page - 1 if page > 1 else None,
            'next_page': page + 1 if page < total_pages else None,
            'search_query': search_query
        })
        
    except Exception as e:
        print(f"Error in filter_media: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

def init_db():
    try:
        # Check if database exists
        if os.path.exists('../db/anime.db'):
            print("Database already exists. Skipping initialization.")
            return
            
        conn = sqlite3.connect('../db/anime.db')
        with open('../db/data.sql', 'r') as f:
            conn.executescript(f.read())
        conn.close()
        print("Database initialized successfully!")
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")
        raise

if __name__ == '__main__':
    try:
        # Initialize database only if it doesn't exist
        if not os.path.exists('../db/anime.db'):
            init_db()
            print("Database initialized successfully!")
        app.run(debug=True)
    except Exception as e:
        print(f"Error: {e}")
