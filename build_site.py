#!/usr/bin/env python3
"""
Build script for yukakinoki.com
Fetches data from Google Sheets and generates HTML pages
"""

import os
import json
import requests
from datetime import datetime

# Google Sheets configuration
SHEET_ID = os.environ.get('GOOGLE_SHEET_ID', '')
API_KEY = os.environ.get('GOOGLE_API_KEY', '')

# Sheet ranges
PROJECTS_RANGE = 'Projects!A2:H'  # Assuming headers in row 1
CONFIG_RANGE = 'Config!A2:B'

def fetch_sheet_data(sheet_id, range_name, api_key):
    """Fetch data from Google Sheets"""
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{range_name}?key={api_key}'
    response = requests.get(url)
    response.raise_for_status()
    return response.json().get('values', [])

def parse_projects(rows):
    """Parse project rows into structured data"""
    projects = []
    for row in rows:
        if len(row) < 3:  # Skip incomplete rows
            continue
        
        project = {
            'name': row[0] if len(row) > 0 else '',
            'type': row[1] if len(row) > 1 else 'image',  # image or video
            'file_path': row[2] if len(row) > 2 else '',
            'thumbnail': row[3] if len(row) > 3 else '',  # Optional thumbnail for videos
            'description': row[4] if len(row) > 4 else '',
            'category': row[5] if len(row) > 5 else 'gallery',  # gallery or archive
            'order': int(row[6]) if len(row) > 6 and row[6].isdigit() else 999,
            'visible': row[7].lower() == 'yes' if len(row) > 7 else True
        }
        
        if project['visible']:
            projects.append(project)
    
    # Sort by order
    projects.sort(key=lambda x: x['order'])
    return projects

def generate_project_html(project):
    """Generate HTML for a single project"""
    if project['type'] == 'video':
        thumbnail = project['thumbnail'] if project['thumbnail'] else project['file_path'].replace('.mp4', '.png')
        return f'''[![

Your browser does not support the video tag.
]({thumbnail})]({project['file_path']})'''
    else:
        return f"![{project['description']}]({project['file_path']})"

def generate_gallery_page(projects, template_path='templates/gallery_template.html'):
    """Generate the gallery/index page"""
    gallery_projects = [p for p in projects if p['category'] == 'gallery']
    
    project_html = '\n'.join([generate_project_html(p) for p in gallery_projects])
    
    # Read template
    if os.path.exists(template_path):
        with open(template_path, 'r') as f:
            template = f.read()
        html = template.replace('{{PROJECTS}}', project_html)
    else:
        # Fallback: generate basic HTML
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>yukakinoki</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <nav>
            <a href="/" class="logo">yukakinoki</a>
            <button class="menu-toggle">expand_more</button>
            <ul>
                <li><a href="info.html">INFO</a></li>
                <li><a href="index.html">GALLERY</a></li>
                <li><a href="archive.html">ARCHIVE</a></li>
            </ul>
        </nav>
    </header>
    <main class="gallery">
{project_html}
    </main>
    <footer>
        <p>Copyright © {datetime.now().year}, yukakinoki.com</p>
    </footer>
</body>
</html>'''
    
    return html

def generate_archive_page(projects, template_path='templates/archive_template.html'):
    """Generate the archive page"""
    archive_projects = [p for p in projects if p['category'] == 'archive']
    
    project_html = '\n'.join([generate_project_html(p) for p in archive_projects])
    
    # Similar to gallery but for archive
    if os.path.exists(template_path):
        with open(template_path, 'r') as f:
            template = f.read()
        html = template.replace('{{PROJECTS}}', project_html)
    else:
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Archive - yukakinoki</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <nav>
            <a href="/" class="logo">yukakinoki</a>
            <button class="menu-toggle">expand_more</button>
            <ul>
                <li><a href="info.html">INFO</a></li>
                <li><a href="index.html">GALLERY</a></li>
                <li><a href="archive.html">ARCHIVE</a></li>
            </ul>
        </nav>
    </header>
    <main class="archive">
{project_html}
    </main>
    <footer>
        <p>Copyright © {datetime.now().year}, yukakinoki.com</p>
    </footer>
</body>
</html>'''
    
    return html

def main():
    """Main build process"""
    print("🚀 Starting build process...")
    
    # Fetch data from Google Sheets
    print("📊 Fetching data from Google Sheets...")
    try:
        project_rows = fetch_sheet_data(SHEET_ID, PROJECTS_RANGE, API_KEY)
        projects = parse_projects(project_rows)
        print(f"✅ Found {len(projects)} projects")
    except Exception as e:
        print(f"❌ Error fetching sheet data: {e}")
        return
    
    # Generate pages
    print("📝 Generating HTML pages...")
    
    # Gallery page
    gallery_html = generate_gallery_page(projects)
    with open('index.html', 'w') as f:
        f.write(gallery_html)
    print("✅ Generated index.html")
    
    # Archive page
    archive_html = generate_archive_page(projects)
    with open('archive.html', 'w') as f:
        f.write(archive_html)
    print("✅ Generated archive.html")
    
    print("🎉 Build complete!")

if __name__ == '__main__':
    main()
