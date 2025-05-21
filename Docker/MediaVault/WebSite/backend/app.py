from flask import Flask, render_template, request, jsonify
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend/templates')

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
                LOWER(TRIM(genre)) LIKE LOWER(CONCAT(%%s, ',%%%%')) OR
                LOWER(TRIM(genre)) LIKE LOWER(CONCAT('%%%%, ', %%s, ',%%%%')) OR
                LOWER(TRIM(genre)) LIKE LOWER(CONCAT('%%%%,', %%s, ',%%%%')) OR
                LOWER(TRIM(genre)) LIKE LOWER(CONCAT('%%%%, ', %%s)) OR
                LOWER(TRIM(genre)) LIKE LOWER(CONCAT('%%%%,', %%s)) OR
                LOWER(TRIM(genre)) LIKE LOWER(CONCAT('%%%% ', %%s, ' %%%%')) OR
                LOWER(TRIM(genre)) LIKE LOWER(CONCAT(%%s, ' %%%%')) OR
                LOWER(TRIM(genre)) LIKE LOWER(CONCAT('%%%% ', %%s))
            )"""
            params.extend([genre_filter] * 9)
        
        # Add ordering
        query += " ORDER BY rating DESC"
        
        # Get total count for pagination
        count_query = f"SELECT COUNT(*) as total FROM ({query}) as subquery"
        cursor.execute(count_query, params)
        total_results = cursor.fetchone()['total']
        
        # Execute the query without pagination to get all results
        cursor.execute(query, params)
        all_results = cursor.fetchall()
        
        # Apply pagination in Python to get the current page results
        per_page = 8
        total_results = len(all_results)
        offset = (page - 1) * per_page
        paginated_results = all_results[offset:offset + per_page] if total_results > 0 else []
        
        # Initialize genres list
        genres = []
        
        # Only fetch genres if we have results
        if total_results > 0:
            cursor.execute(f"""
                SELECT DISTINCT TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(genre, ',', n.n), ',', -1)) as genre
                FROM {table} t
                CROSS JOIN (
                    SELECT 1 as n UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL
                    SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6
                ) n
                WHERE n.n <= 1 + (LENGTH(genre) - LENGTH(REPLACE(genre, ',', '')))
                AND TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(genre, ',', n.n), ',', -1)) != ''
                ORDER BY genre
            """)
            genres = [row['genre'] for row in cursor.fetchall()]
        
        # Calculate pagination info
        total_pages = (total_results + per_page - 1) // per_page if per_page > 0 else 1
        current_page = min(page, total_pages) if total_pages > 0 else 1
        
        return {
            'media_list': paginated_results,
            'all_media': all_results,  # Include all results for total count
            'current_page': current_page,
            'total_pages': total_pages,
            'genres': genres,
            'prev_page': current_page - 1 if current_page > 1 else None,
            'next_page': current_page + 1 if current_page < total_pages else None,
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
    try:
        media_type = request.args.get('type', 'anime')
        page = int(request.args.get('page', 1))
        search_query = request.args.get('search', '')
        genre_filter = request.args.get('genre', 'all')
        
        media_data = get_media_list(media_type, page, search_query, genre_filter)
        
        # Ensure all required keys exist in media_data
        media_list = media_data.get('media_list', [])
        current_page = media_data.get('current_page', 1)
        total_pages = media_data.get('total_pages', 1)
        genres = media_data.get('genres', [])
        prev_page = media_data.get('prev_page')
        next_page = media_data.get('next_page')
        search_query = media_data.get('search_query', search_query)
        genre_filter = media_data.get('genre_filter', genre_filter)
        
        # Debug output
        print(f"Media data: {media_data}")
        print(f"Media type: {media_type}")
        print(f"Media list length: {len(media_list) if media_list else 0}")
        
        return render_template('index.html', 
                            media_type=media_type,
                            media_list=media_list,
                            current_page=current_page,
                            total_pages=total_pages,
                            genres=genres,
                            prev_page=prev_page,
                            next_page=next_page,
                            search_query=search_query,
                            genre_filter=genre_filter)
    except Exception as e:
        print(f"Error in index route: {str(e)}")
        # Return a minimal response with default values
        return render_template('index.html',
                            media_type='anime',
                            media_list=[],
                            current_page=1,
                            total_pages=1,
                            genres=[],
                            prev_page=None,
                            next_page=None,
                            search_query='',
                            genre_filter='all')

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
            tables = [
                {'name': 'anime', 'count_col': 'episodes'},
                {'name': 'movies', 'count_col': 'runtime'},
                {'name': 'best_series', 'count_col': 'episodes'}
            ]
        else:
            tables = [{
                'name': media_type,
                'count_col': 'episodes' if media_type in ['anime', 'series'] else 'runtime'
            }]
        
        all_media = []
        all_genres = set()
        
        # Process each table
        for table in tables:
            # Define the base query with proper parameterization
            query = f"""
                SELECT 
                    id, 
                    title, 
                    genre, 
                    rating, 
                    {table['count_col']} as count,
                    release_year as year,
                    image,
                    {'' if table['name'] == 'best_series' else 'NULL as'} description
                FROM {table['name']} 
                WHERE 1=1
            """
            
            params = []
            
            # Add search filter with parameterization
            if search_query:
                query += " AND LOWER(title) LIKE LOWER(%s)"
                params.append(f"%{search_query}%")
                
            # Add genre filter with parameterization
            if genre_filter != 'all':
                query += """ AND (
                    LOWER(TRIM(genre)) = LOWER(%s) OR
                    LOWER(TRIM(genre)) LIKE LOWER(CONCAT(%s, ',%')) OR
                    LOWER(TRIM(genre)) LIKE LOWER(CONCAT('%, ', %s, ',%')) OR
                    LOWER(TRIM(genre)) LIKE LOWER(CONCAT('%,', %s, ',%')) OR
                    LOWER(TRIM(genre)) LIKE LOWER(CONCAT('%, ', %s)) OR
                    LOWER(TRIM(genre)) LIKE LOWER(CONCAT('%,', %s)) OR
                    LOWER(TRIM(genre)) LIKE LOWER(CONCAT('% ', %s, ' %')) OR
                    LOWER(TRIM(genre)) LIKE LOWER(CONCAT(%s, ' %')) OR
                    LOWER(TRIM(genre)) LIKE LOWER(CONCAT('% ', %s))
                )"""
                # Add the genre parameter multiple times for each LIKE condition
                params.extend([genre_filter] * 9)
            
            # Execute query with parameters
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            print(f"Executing query for {table['name']}:", query)
            print("With params:", params)
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            conn.close()
            
            print(f"Found {len(results)} results for {table['name']}")
            
            # If no results and a genre filter is active
            if not results and genre_filter != 'all':
                return jsonify({
                    'status': 'not_found',
                    'message': f'No items found for genre: {genre_filter}'
                })
            
            # Add media type to each result
            for item in results:
                item['media_type'] = table['name']
                if table['name'] == 'best_series':
                    item['media_type'] = 'series'  # Map to 'series' for frontend
                all_media.append(item)
                
                # Extract and add unique genres
                if item.get('genre'):
                    genres = [g.strip() for g in item['genre'].split(',') if g.strip()]
                    all_genres.update(genres)
            
            conn.close()
        
        # Sort by rating (highest first)
        all_media.sort(key=lambda x: float(x.get('rating', 0)), reverse=True)
        
        # Apply pagination
        per_page = 8
        total_items = len(all_media)
        total_pages = (total_items + per_page - 1) // per_page if per_page > 0 else 1
        
        # Ensure page is within valid range
        current_page = max(1, min(page, total_pages)) if total_pages > 0 else 1
        
        # Calculate start and end indices for pagination
        start_idx = (current_page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_media = all_media[start_idx:end_idx]
        
        # Sort genres alphabetically
        sorted_genres = sorted(all_genres)
        
        response = {
            'media_list': paginated_media,
            'current_page': current_page,
            'total_pages': total_pages,
            'genres': sorted_genres,
            'prev_page': current_page - 1 if current_page > 1 else None,
            'next_page': current_page + 1 if current_page < total_pages else None,
            'search_query': search_query,
            'genre_filter': genre_filter
        }
        
        return jsonify({
            'status': 'success',
            'media': response['media_list'],
            'total_pages': response['total_pages'],
            'current_page': response['current_page'],
            'total_results': len(all_media),
            'genres': response['genres'],
            'media_type': media_type,
            'genre_filter': response['genre_filter'],
            'has_prev': response['prev_page'] is not None,
            'has_next': response['next_page'] is not None,
            'prev_page': response['prev_page'],
            'next_page': response['next_page'],
            'search_query': response['search_query']
        })
        
    except Exception as e:
        print(f"Error in filter_media: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/media', methods=['GET'])
def get_media():
    """API endpoint to get media items with optional filtering."""
    try:
        media_type = request.args.get('type', 'all')
        page = int(request.args.get('page', 1))
        search = request.args.get('search', '')
        genre = request.args.get('genre', 'all')
        
        # Get media data
        media_data = get_media_list(media_type, page, search, genre)
        
        # Get total results count
        total_results = len(media_data.get('all_media', []))
        
        # Prepare pagination info
        pagination = {
            'current_page': media_data['current_page'],
            'total_pages': media_data['total_pages'],
            'total_results': total_results,
            'per_page': 8,
            'has_prev': media_data['prev_page'] is not None,
            'has_next': media_data['next_page'] is not None,
            'prev_page': media_data['prev_page'],
            'next_page': media_data['next_page']
        }
        
        # If no results, return empty response
        if total_results == 0:
            return jsonify({
                'status': 'success',
                'data': {
                    'media': [],
                    'pagination': pagination,
                    'filters': {
                        'search': search,
                        'genre': genre,
                        'type': media_type
                    },
                    'genres': media_data.get('genres', [])
                }
            }), 200
        
        # Prepare filters
        filters = {
            'search': search,
            'genre': genre,
            'type': media_type
        }
        
        return jsonify({
            'status': 'success',
            'data': {
                'media': media_data['media_list'],
                'pagination': pagination,
                'filters': filters,
                'genres': media_data.get('genres', [])
            }
        }), 200
        
    except Exception as e:
        print(f"Error in get_media: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/media/<media_type>/<int:media_id>', methods=['GET'])
def get_media_item(media_type, media_id):
    """API endpoint to get a specific media item by ID and type."""
    try:
        # Validate media type
        if media_type not in ['anime', 'movies', 'series']:
            return jsonify({
                'status': 'error',
                'message': 'Invalid media type. Must be one of: anime, movies, series'
            }), 400
            
        # Map media type to table name and select fields
        table_map = {
            'anime': {
                'table': 'anime',
                'select': 'id, title, genre, rating, episodes as count, release_year as year, image, NULL as description'
            },
            'movies': {
                'table': 'movies',
                'select': 'id, title, genre, rating, runtime as count, release_year as year, image, NULL as description'
            },
            'series': {
                'table': 'best_series',
                'select': 'id, title, genre, rating, episodes as count, release_year as year, image, description'
            }
        }
        
        table_info = table_map[media_type]
        
        # Get database connection
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Query the database with proper field mapping
        query = f"SELECT {table_info['select']} FROM {table_info['table']} WHERE id = %s"
        cursor.execute(query, (media_id,))
        item = cursor.fetchone()
        
        # Close connection
        cursor.close()
        conn.close()
        
        if not item:
            return jsonify({
                'status': 'error',
                'message': f'{media_type.capitalize()} not found with ID {media_id}'
            }), 404
            
        # Add media type to the response
        item['media_type'] = media_type
        
        return jsonify({
            'status': 'success',
            'data': item
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/genres', methods=['GET'])
def get_all_genres():
    """API endpoint to get all unique genres across all media types."""
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
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'data': genres
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"Error: {e}")
