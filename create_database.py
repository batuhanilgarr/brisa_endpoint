#!/usr/bin/env python3
"""
CSV to SQLite Database Converter
Converts large CSV file to SQLite for efficient querying
"""

import sqlite3
import csv
import os
from pathlib import Path

CSV_FILE = "UBY.TyreListFriendlyPath.csv"
DB_FILE = "tyre_paths.db"

def create_database():
    """Create SQLite database from CSV file"""
    
    # Remove existing database
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"Removed existing {DB_FILE}")
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tyre_paths (
            id INTEGER PRIMARY KEY,
            tyre_category_link TEXT,
            tyre_group TEXT,
            tyre_group_type TEXT,
            tyre_listing_type TEXT,
            tyre_brand TEXT,
            tyre_model TEXT,
            tyre_year TEXT,
            tyre_version TEXT,
            tyre_season TEXT,
            tyre_usage TEXT,
            tyre_service TEXT,
            tyre_position TEXT,
            seo_title TEXT,
            seo_description TEXT,
            seo_keyword TEXT,
            seo_abstract TEXT,
            created_date TEXT,
            is_active TEXT,
            tyre_section_width TEXT,
            tyre_aspect_ratio TEXT,
            tyre_jant_cap TEXT,
            is_seo TEXT
        )
    ''')
    
    # Create indexes for fast searching
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_category_link ON tyre_paths(tyre_category_link)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_seo_title ON tyre_paths(seo_title)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_group_type ON tyre_paths(tyre_group_type)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_listing_type ON tyre_paths(tyre_listing_type)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_brand ON tyre_paths(tyre_brand)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_model ON tyre_paths(tyre_model)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_year ON tyre_paths(tyre_year)')
    
    print("Reading CSV file...")
    
    with open(CSV_FILE, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip header
        
        print(f"Header: {header}")
        
        batch_size = 10000
        batch = []
        total = 0
        
        for row in reader:
            if len(row) >= 23:
                batch.append((
                    row[0],   # ID
                    row[1],   # TyreCategoryLink
                    row[2],   # TyreGroup
                    row[3],   # TyreGroupType
                    row[4],   # TyreListingType
                    row[5],   # TyreBrand
                    row[6],   # TyreModel
                    row[7],   # TyreYear
                    row[8],   # TyreVersion
                    row[9],   # TyreSeason
                    row[10],  # TyreUsage
                    row[11],  # TyreService
                    row[12],  # TyrePosition
                    row[13],  # SeoTitle
                    row[14],  # SeoDescription
                    row[15],  # SeoKeyword
                    row[16],  # SeoAbstract
                    row[17],  # CreatedDate
                    row[18],  # IsActive
                    row[19] if len(row) > 19 else '',  # TyreSectionWidth
                    row[20] if len(row) > 20 else '',  # TyreAspectRatio
                    row[21] if len(row) > 21 else '',  # TyreJantCapı
                    row[22] if len(row) > 22 else ''   # IsSeo
                ))
                
                if len(batch) >= batch_size:
                    cursor.executemany('''
                        INSERT INTO tyre_paths VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', batch)
                    conn.commit()
                    total += len(batch)
                    print(f"Inserted {total:,} records...")
                    batch = []
        
        # Insert remaining
        if batch:
            cursor.executemany('''
                INSERT INTO tyre_paths VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', batch)
            conn.commit()
            total += len(batch)
    
    print(f"\n✅ Total records inserted: {total:,}")
    
    # Get database size
    conn.close()
    db_size = os.path.getsize(DB_FILE) / (1024 * 1024)
    print(f"📁 Database size: {db_size:.2f} MB")
    
    return total

if __name__ == "__main__":
    create_database()
