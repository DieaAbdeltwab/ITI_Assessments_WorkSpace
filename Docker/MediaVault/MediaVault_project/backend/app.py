from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from flask_cors import CORS

# Load environment variables
load_dotenv()

# Create Flask app without frontend folders
app = Flask(__name__)

# Enable CORS for all routes with specific configurations
cors = CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

# Database connection function
def get_db_connection():
    """Get a connection to the MariaDB database."""
    try:
        conn = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', 'db'),
            user=os.getenv('MYSQL_USER', 'user'),
            password=os.getenv('MYSQL_PASSWORD', 'password'),
            database=os.getenv('MYSQL_DATABASE', 'anime_db'),
            port=3306,
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci'
        )
        return conn
    except Error as e:
        print(f"Error connecting to MariaDB: {e}")
        raise

def get_media_list(media_type='anime', page=1, search_query='', genre_filter='all'):
    """
    Retrieve a list of media items from the database.
    
    Args:
        media_type (str): Type of media ('anime', 'movies', 'series', or 'all')
        page (int): Page number for pagination
        search_query (str): Search term to filter by title
        genre_filter (str): Genre to filter by
        
    Returns:
        dict: Dictionary containing media list and pagination info
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # If 'all' is selected, combine results from all tables
        if media_type == 'all':
            # Get results from all tables with proper parameterization
            queries = []
            params = []
            
            # Base queries for each table with proper field mapping
            queries.append("""
                SELECT 'anime' as media_type, id, title, genre, rating, 
                       episodes as count, release_year as year, image, NULL as description 
                FROM anime WHERE 1=1
            """)
            
            queries.append("""
                SELECT 'movies' as media_type, id, title, genre, rating, 
                       runtime as count, release_year as year, image, NULL as description 
                FROM movies WHERE 1=1
            """)
            
            queries.append("""
                SELECT 'series' as media_type, id, title, genre, rating, 
                       episodes as count, release_year as year, image, description 
                FROM best_series WHERE 1=1
            """)
            
            # Add search filter if provided
            if search_query:
                search_param = f"%{search_query}%"
                for i in range(len(queries)):
                    queries[i] += " AND title LIKE %s"
                    params.append(search_param)
            
            # Add genre filter if provided
            if genre_filter != 'all':
                genre_condition = """ AND (
                    LOWER(TRIM(genre)) = LOWER(%s) OR
                    LOWER(TRIM(genre)) LIKE LOWER(CONCAT(%%s, ',%%%%')) OR
                    LOWER(TRIM(genre)) LIKE LOWER(CONCAT('%%%%, ', %%s, ',%%%%')) OR
                    LOWER(TRIM(genre)) LIKE LOWER(CONCAT('%%%%,', %%s, ',%%%%')) OR
                    LOWER(TRIM(genre)) LIKE LOWER(CONCAT('%%%%, ', %%s)) OR
                    LOWER(TRIM(genre)) LIKE LOWER(CONCAT('%%%%,', %%s)) OR
                    LOWER(TRIM(genre)) LIKE LOWER(CONCAT('%%%% ', %%s, ' %%%%')) OR
                    LOWER(TRIM(genre)) LIKE LOWER(CONCAT(%%s, ' %%%%')) OR
                    LOWER(TRIM(genre)) LIKE LOWER(CONCAT('%%%% ', %%s))
                )"""
                for i in range(len(queries)):
                    queries[i] += genre_condition
                    params.extend([genre_filter] * 9)
            
            # Combine all queries with UNION ALL
            combined_query = " UNION ALL ".join(queries) + " ORDER BY rating DESC"
            
            # Execute the combined query
            cursor.execute(combined_query, params)
            all_results = cursor.fetchall()
            
            # Get unique genres from all tables
            cursor.execute("""
                SELECT DISTINCT TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(t.genre, ',', n.n), ',', -1)) as genre
                FROM (
                    SELECT genre FROM anime
                    UNION SELECT genre FROM movies
                    UNION SELECT genre FROM best_series
                ) t
                CROSS JOIN (
                    SELECT 1 as n UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL
                    SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6
                ) n
                WHERE n.n <= 1 + (LENGTH(t.genre) - LENGTH(REPLACE(t.genre, ',', '')))
                AND TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(t.genre, ',', n.n), ',', -1)) != ''
                ORDER BY genre
            """)
            genres = [row['genre'] for row in cursor.fetchall()]
            
            # Apply pagination
            per_page = 8
            total_results = len(all_results)
            total_pages = (total_results + per_page - 1) // per_page if per_page > 0 else 1
            page = max(1, min(page, total_pages))  # Ensure page is within valid range
            offset = (page - 1) * per_page
            paginated_results = all_results[offset:offset + per_page]
            
            return {
                'media_list': paginated_results,
                'current_page': page,
                'total_pages': total_pages,
                'genres': genres,
                'prev_page': page - 1 if page > 1 else None,
                'next_page': page + 1 if page < total_pages else None,
                'search_query': search_query,
                'genre_filter': genre_filter
            }
    except Error as e:
        print(f"Database error: {e}")
        return {
            'media_list': [],
            'current_page': 1,
            'total_pages': 1,
            'genres': [],
            'error': str(e)
        }
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

    # If we get here, we're querying a single table
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Determine the table and count column based on media_type
        if media_type == 'anime':
            table = 'anime'
            count_col = 'episodes'
            select_fields = "id, title, genre, rating, episodes as count, release_year as year, image, NULL as description"
        elif media_type == 'movies':
            table = 'movies'
            count_col = 'runtime'
            select_fields = "id, title, genre, rating, runtime as count, release_year as year, image, NULL as description"
        else:  # series
            table = 'best_series'
            count_col = 'episodes'
            select_fields = "id, title, genre, rating, episodes as count, release_year as year, image, description"
        
        # Build the base query
        query = f"""
            SELECT 
                '{media_type}' as media_type, 
                {select_fields}
            FROM {table} 
            WHERE 1=1
        """
        
        params = []
        
        # Add search filter if provided
        if search_query:
            query += " AND LOWER(title) LIKE LOWER(%s)"
            params.append(f"%{search_query}%")
        
        # Add genre filter if provided
        if genre_filter != 'all':
            query += """ AND (
                LOWER(TRIM(genre)) = LOWER(%s) OR
                LOWER(TRIM(genre)) LIKE LOWER(CONCAT(%s, ',%%')) OR
                LOWER(TRIM(genre)) LIKE LOWER(CONCAT('%%, ', %s, ',%%')) OR
                LOWER(TRIM(genre)) LIKE LOWER(CONCAT('%%,', %s, ',%%')) OR
                LOWER(TRIM(genre)) LIKE LOWER(CONCAT('%%, ', %s)) OR
                LOWER(TRIM(genre)) LIKE LOWER(CONCAT('%%,', %s)) OR
                LOWER(TRIM(genre)) LIKE LOWER(CONCAT('%% ', %s, ' %%')) OR
                LOWER(TRIM(genre)) LIKE LOWER(CONCAT(%s, ' %%')) OR
                LOWER(TRIM(genre)) LIKE LOWER(CONCAT('%% ', %s))
            )"""
            params.extend([genre_filter] * 9)
        
        # Add sorting
        query += " ORDER BY rating DESC"
        
        # Execute the query
        cursor.execute(query, params)
        all_results = cursor.fetchall()
        
        # Get unique genres for the selected media type
        genre_query = f"""
            SELECT DISTINCT TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(genre, ',', n.n), ',', -1)) as genre
            FROM {table}
            CROSS JOIN (
                SELECT 1 as n UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL
                SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6
            ) n
            WHERE n.n <= 1 + (LENGTH(genre) - LENGTH(REPLACE(genre, ',', '')))
            AND TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(genre, ',', n.n), ',', -1)) != ''
            ORDER BY genre
        """
        cursor.execute(genre_query)
        genres = [row['genre'] for row in cursor.fetchall()]
        
        # Apply pagination
        per_page = 8
        total_results = len(all_results)
        total_pages = (total_results + per_page - 1) // per_page if per_page > 0 else 1
        page = max(1, min(page, total_pages))  # Ensure page is within valid range
        offset = (page - 1) * per_page
        paginated_results = all_results[offset:offset + per_page]
        
        return {
            'media_list': paginated_results,
            'current_page': page,
            'total_pages': total_pages,
            'genres': genres,
            'prev_page': page - 1 if page > 1 else None,
            'next_page': page + 1 if page < total_pages else None,
            'search_query': search_query,
            'genre_filter': genre_filter
        }
    except Error as e:
        print(f"Database error: {e}")
        return {
            'media_list': [],
            'current_page': 1,
            'total_pages': 1,
            'genres': [],
            'error': str(e)
        }
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

@app.route('/')
def index():
    """
    API root endpoint that returns basic API information
    """
    return jsonify({
        "status": "success",
        "message": "MediaVault API is running",
        "api_endpoints": {
            "/api/media": "Get media items with optional filtering",
            "/api/media/<media_type>/<media_id>": "Get details for a specific media item",
            "/api/genres": "Get all available genres"
        }
    })

@app.route('/api/media')
def get_media():
    """
    API endpoint to get media items with optional filtering.
    
    Query parameters:
    - type: Media type ('anime', 'movies', 'series', or 'all')
    - page: Page number for pagination
    - search: Search term to filter by title
    - genre: Genre to filter by
    
    Returns:
    - JSON response with media items and pagination info
    """
    try:
        media_type = request.args.get('type', 'anime')
        page = int(request.args.get('page', 1))
        search_query = request.args.get('search', '')
        genre_filter = request.args.get('genre', 'all')
        
        # Get media list with filters
        media_data = get_media_list(media_type, page, search_query, genre_filter)
        
        # Convert media_list to media for API consistency
        if 'media_list' in media_data:
            media_data['media'] = media_data.pop('media_list')
        
        # Return JSON response
        return jsonify(media_data)
    except Exception as e:
        print(f"Error in get_media: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'media': [],
            'current_page': 1,
            'total_pages': 1,
            'genres': []
        })

@app.route('/api/media/<media_type>/<int:media_id>')
def get_media_item(media_type, media_id):
    """
    API endpoint to get a specific media item by ID and type.
    
    Path parameters:
    - media_type: Type of media ('anime', 'movies', 'series')
    - media_id: ID of the media item
    
    Returns:
    - JSON response with media item details
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Determine the table and fields based on media_type
        if media_type == 'anime':
            table = 'anime'
            count_col = 'episodes'
            select_fields = "id, title, genre, rating, episodes as count, release_year as year, image, NULL as description"
        elif media_type == 'movies':
            table = 'movies'
            count_col = 'runtime'
            select_fields = "id, title, genre, rating, runtime as count, release_year as year, image, NULL as description"
        elif media_type == 'series':
            table = 'best_series'
            count_col = 'episodes'
            select_fields = "id, title, genre, rating, episodes as count, release_year as year, image, description"
        else:
            return jsonify({
                'status': 'error',
                'message': f"Invalid media type: {media_type}"
            }), 400
        
        # Build and execute the query
        query = f"""
            SELECT 
                '{media_type}' as media_type, 
                {select_fields}
            FROM {table} 
            WHERE id = %s
        """
        
        cursor.execute(query, (media_id,))
        result = cursor.fetchone()
        
        if result:
            return jsonify(result)
        else:
            return jsonify({
                'status': 'error',
                'message': f"Media item not found: {media_type}/{media_id}"
            }), 404
    except Exception as e:
        print(f"Error in get_media_item: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

@app.route('/api/genres')
def get_all_genres():
    """
    API endpoint to get all unique genres across all media types.
    
    Returns:
    - JSON response with list of genres
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get unique genres from all tables
        cursor.execute("""
            SELECT DISTINCT TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(t.genre, ',', n.n), ',', -1)) as genre
            FROM (
                SELECT genre FROM anime
                UNION SELECT genre FROM movies
                UNION SELECT genre FROM best_series
            ) t
            CROSS JOIN (
                SELECT 1 as n UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL
                SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6
            ) n
            WHERE n.n <= 1 + (LENGTH(t.genre) - LENGTH(REPLACE(t.genre, ',', '')))
            AND TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(t.genre, ',', n.n), ',', -1)) != ''
            ORDER BY genre
        """)
        
        genres = [row['genre'] for row in cursor.fetchall()]
        
        return jsonify({
            'status': 'success',
            'genres': genres
        })
    except Exception as e:
        print(f"Error in get_all_genres: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'genres': []
        }), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"Error starting Flask app: {e}")
