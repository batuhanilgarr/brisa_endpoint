#!/usr/bin/env python3
"""
Flask API Server for Tyre Path Search
Provides fast search capability for 2+ million records
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

DB_FILE = "tyre_paths.db"

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/search', methods=['GET'])
def search():
    """
    Search tyre paths
    Query params:
    - q: search query (searches in category_link and seo_title)
    - group_type: filter by TyreGroupType (Consumer, Commercial, LightCommercial)
    - listing_type: filter by TyreListingType
    - brand: filter by TyreBrand ID
    - model: filter by TyreModel ID
    - year: filter by TyreYear
    - limit: max results (default 50)
    - offset: pagination offset (default 0)
    """
    q = request.args.get('q', '').strip()
    group_type = request.args.get('group_type', '')
    listing_type = request.args.get('listing_type', '')
    brand = request.args.get('brand', '')
    model = request.args.get('model', '')
    year = request.args.get('year', '')
    limit = min(int(request.args.get('limit', 50)), 200)
    offset = int(request.args.get('offset', 0))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Build query
    conditions = []
    params = []
    
    if q:
        conditions.append("(tyre_category_link LIKE ? OR seo_title LIKE ? OR seo_keyword LIKE ?)")
        params.extend([f'%{q}%', f'%{q}%', f'%{q}%'])
    
    if group_type:
        conditions.append("tyre_group_type = ?")
        params.append(group_type)
    
    if listing_type:
        conditions.append("tyre_listing_type = ?")
        params.append(listing_type)
    
    if brand and brand != '0':
        conditions.append("tyre_brand = ?")
        params.append(brand)
    
    if model and model != '0':
        conditions.append("tyre_model = ?")
        params.append(model)
    
    if year and year != '0':
        conditions.append("tyre_year = ?")
        params.append(year)
    
    where_clause = " AND ".join(conditions) if conditions else "1=1"
    
    # Get total count
    count_query = f"SELECT COUNT(*) FROM tyre_paths WHERE {where_clause}"
    cursor.execute(count_query, params)
    total = cursor.fetchone()[0]
    
    # Get results
    query = f"""
        SELECT id, tyre_category_link, tyre_group, tyre_group_type, tyre_listing_type,
               tyre_brand, tyre_model, tyre_year, tyre_version, tyre_season,
               tyre_usage, tyre_service, tyre_position, seo_title, seo_description
        FROM tyre_paths 
        WHERE {where_clause}
        ORDER BY id
        LIMIT ? OFFSET ?
    """
    params.extend([limit, offset])
    cursor.execute(query, params)
    
    results = []
    for row in cursor.fetchall():
        results.append({
            'id': row['id'],
            'path': row['tyre_category_link'],
            'url': f"https://www.bridgestone.com.tr/{row['tyre_category_link']}",
            'group': row['tyre_group'],
            'groupType': row['tyre_group_type'],
            'listingType': row['tyre_listing_type'],
            'brand': row['tyre_brand'],
            'model': row['tyre_model'],
            'year': row['tyre_year'],
            'version': row['tyre_version'],
            'season': row['tyre_season'],
            'usage': row['tyre_usage'],
            'service': row['tyre_service'],
            'position': row['tyre_position'],
            'title': row['seo_title'],
            'description': row['seo_description']
        })
    
    conn.close()
    
    return jsonify({
        'total': total,
        'limit': limit,
        'offset': offset,
        'results': results
    })

@app.route('/api/stats', methods=['GET'])
def stats():
    """Get database statistics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Total count
    cursor.execute("SELECT COUNT(*) FROM tyre_paths")
    total = cursor.fetchone()[0]
    
    # Group types
    cursor.execute("SELECT tyre_group_type, COUNT(*) as count FROM tyre_paths GROUP BY tyre_group_type")
    group_types = {row['tyre_group_type'] or 'Undefined': row['count'] for row in cursor.fetchall()}
    
    # Listing types
    cursor.execute("SELECT tyre_listing_type, COUNT(*) as count FROM tyre_paths WHERE tyre_listing_type != '' GROUP BY tyre_listing_type")
    listing_types = {row['tyre_listing_type']: row['count'] for row in cursor.fetchall()}
    
    conn.close()
    
    return jsonify({
        'total': total,
        'groupTypes': group_types,
        'listingTypes': listing_types
    })

@app.route('/api/brands', methods=['GET'])
def get_brands():
    """Get unique brand IDs with counts"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT DISTINCT tyre_brand, COUNT(*) as count 
        FROM tyre_paths 
        WHERE tyre_brand != '0' AND tyre_brand != ''
        GROUP BY tyre_brand
        ORDER BY count DESC
        LIMIT 100
    """)
    
    brands = [{'id': row['tyre_brand'], 'count': row['count']} for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(brands)

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    if os.path.exists(DB_FILE):
        return jsonify({'status': 'ok', 'database': 'connected'})
    return jsonify({'status': 'error', 'database': 'not found'}), 500

if __name__ == '__main__':
    import os
    # Production'da debug kapalı
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print("🚀 Starting Tyre Path API Server...")
    print("📍 API available at http://localhost:5001")
    print("\nEndpoints:")
    print("  GET /api/search?q=<query>&limit=50&offset=0")
    print("  GET /api/stats")
    print("  GET /api/brands")
    print("  GET /api/health")
    app.run(host='0.0.0.0', port=5001, debug=debug_mode)
