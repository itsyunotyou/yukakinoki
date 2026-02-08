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
PROJECTS_RANGE = 'Projects!A2:H'
INFO_RANGE = 'Info!A2:B'

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
            'type': row[1] if len(row) > 1 else 'image',
            'file_path': row[2] if len(row) > 2 else '',
            'thumbnail': row[3] if len(row) > 3 else '',
            'description': row[4] if len(row) > 4 else '',
            'category': row[5] if len(row) > 5 else 'gallery',
            'order': int(row[6]) if len(row) > 6 and row[6].isdigit() else 999,
            'visible': row[7].lower() == 'yes' if len(row) > 7 else True
        }
        
        if project['visible']:
            projects.append(project)
    
    projects.sort(key=lambda x: x['order'])
    return projects

def parse_info(rows):
    """Parse info page content"""
    info = {}
    for row in rows:
        if len(row) >= 2:
            key = row[0].lower().replace(' ', '_')
            value = row[1]
            info[key] = value
    return info

def generate_project_html(project):
    """Generate HTML for a single project"""
    if project['type'] == 'video':
        thumbnail = project['thumbnail'] if project['thumbnail'] else project['file_path'].replace('.mp4', '.png')
        return f'''        <a href="{project['file_path']}" class="project-item video">
            <img src="{thumbnail}" alt="{project['description']}">
            <div class="video-overlay">
                <p>Your browser does not support the video tag.</p>
            </div>
        </a>'''
    else:
        return f'''        <div class="project-item image">
            <img src="{project['file_path']}" alt="{project['description']}">
        </div>'''

def generate_nav():
    """Generate navigation HTML"""
    return '''    <header>
        <nav>
            <a href="/" class="logo">yukakinoki</a>
            <button class="menu-toggle">expand_more</button>
            <ul>
                <li><a href="info.html">INFO</a></li>
                <li><a href="index.html">GALLERY</a></li>
                <li><a href="archive.html">ARCHIVE</a></li>
            </ul>
        </nav>
    </header>'''

def generate_footer():
    """Generate footer HTML"""
    return f'''    <footer>
        <p>Copyright © {datetime.now().year}, yukakinoki.com</p>
    </footer>'''

def generate_gallery_page(projects):
    """Generate the gallery/index page"""
    gallery_projects = [p for p in projects if p['category'] == 'gallery']
    
    project_html = '\n'.join([generate_project_html(p) for p in gallery_projects])
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>yukakinoki</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
{generate_nav()}
    <main class="gallery">
{project_html}
    </main>
{generate_footer()}
</body>
</html>'''
    
    return html

def generate_archive_page(projects):
    """Generate the archive page"""
    archive_projects = [p for p in projects if p['category'] == 'archive']
    
    if archive_projects:
        project_html = '\n'.join([generate_project_html(p) for p in archive_projects])
    else:
        project_html = ''
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Archive - yukakinoki</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
{generate_nav()}
    <main class="archive">
{project_html}
    </main>
{generate_footer()}
</body>
</html>'''
    
    return html

def generate_info_page(info_data):
    """Generate the info page"""
    # Default values
    bio_en = info_data.get('bio_english', '''Yu Kakinoki is a billingual interdisciplinary designer, currently based in Tokyo. Have developed a distinct eye for aesthetics by growing up in California, Japan, Hong Kong, and London. The goal is to push the boundaries of storytelling through spatial design - whether it be a tangible room, a digital space, or both. This website was built through GitHub Pages with self-learnt HTML, CSS, JavaScript, and Bootstrap. My dissertation title was 'To what extent is the aura relevant to a work of art in the age of biocybernetic simulation?'
''')
    
    bio_jp = info_data.get('bio_japanese', '''柿木優は、現在東京を拠点に活動している学際的なバイリンガルデザイナーです。 カリフォルニア、香港、ロンドンと日本で生まれ育ち、独特なセンスを構築しました。ストーリーテリングの未来をデジタル、そして現実的な空間デザインを交えて追求しています。 事実上何でも独学で学べる世界に住んで幸せです！ このサイトは、HTML、CSS、JavaScript、および Bootstrapを自己学習し、GitHubページを通して構築しました。''')
    
    contact_email = info_data.get('contact_email', 'yukakinoki@gmail.com')
    contact_text = info_data.get('contact_text', 'contact')
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>yukakinoki</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
{generate_nav()}
    <main class="info">
        <section class="bio">
            <p>{bio_en}</p>
            <p>{bio_jp}</p>
        </section>
        <section class="contact">
            <a href="mailto:{contact_email}">{contact_text}</a>
        </section>
    </main>
{generate_footer()}
</body>
</html>'''
    
    return html

def main():
    """Main build process"""
    print("🚀 Starting build process...")
    
    # Fetch data from Google Sheets
    print("📊 Fetching data from Google Sheets...")
    try:
        # Fetch projects
        project_rows = fetch_sheet_data(SHEET_ID, PROJECTS_RANGE, API_KEY)
        projects = parse_projects(project_rows)
        print(f"✅ Found {len(projects)} projects")
        
        # Fetch info page content
        try:
            info_rows = fetch_sheet_data(SHEET_ID, INFO_RANGE, API_KEY)
            info_data = parse_info(info_rows)
            print(f"✅ Found info page content")
        except:
            print("⚠️  Info sheet not found, using defaults")
            info_data = {}
            
    except Exception as e:
        print(f"❌ Error fetching sheet data: {e}")
        return
    
    # Generate pages
    print("📝 Generating HTML pages...")
    
    # Gallery page
    gallery_html = generate_gallery_page(projects)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(gallery_html)
    print("✅ Generated index.html")
    
    # Archive page
    archive_html = generate_archive_page(projects)
    with open('archive.html', 'w', encoding='utf-8') as f:
        f.write(archive_html)
    print("✅ Generated archive.html")
    
    # Info page
    info_html = generate_info_page(info_data)
    with open('info.html', 'w', encoding='utf-8') as f:
        f.write(info_html)
    print("✅ Generated info.html")
    
    print("🎉 Build complete!")

if __name__ == '__main__':
    main()
