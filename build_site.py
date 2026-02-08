#!/usr/bin/env python3
"""
Build script for <span style="text-transform: lowercase;">yukakinoki.com</span> - INTERACTIVE VERSION
Fetches data from Google Sheets and images from Google Drive folders
Generates interactive archive with clickable table rows
"""

import os
import json
import requests
from datetime import datetime

# Google configuration
SHEET_ID = os.environ.get('GOOGLE_SHEET_ID', '')
API_KEY = os.environ.get('GOOGLE_API_KEY', '')

# Sheet ranges
PROJECTS_RANGE = 'Projects!A2:K100'
INFO_RANGE = 'Info!A2:B'

def fetch_sheet_data(sheet_id, range_name, api_key):
    """Fetch data from Google Sheets"""
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{range_name}?key={api_key}'
    response = requests.get(url)
    response.raise_for_status()
    return response.json().get('values', [])

def fetch_drive_folder_files(folder_id, api_key):
    """Fetch all files from a Google Drive folder"""
    url = f'https://www.googleapis.com/drive/v3/files'
    params = {
        'q': f"'{folder_id}' in parents and mimeType contains 'image/'",
        'key': api_key,
        'fields': 'files(id, name, mimeType, webContentLink, thumbnailLink)',
        'orderBy': 'name'
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json().get('files', [])

def get_drive_image_url(file_id):
    """Convert Drive file ID to direct viewable URL"""
    return f'https://drive.google.com/uc?export=view&id={file_id}'

def parse_projects(rows):
    """Parse all projects from single sheet"""
    projects = []
    print(f"   DEBUG: Received {len(rows)} rows from Google Sheets")
    for i, row in enumerate(rows):
        print(f"   DEBUG: Row {i}: length={len(row)}, data={row[:3] if len(row) >= 3 else row}")
        if len(row) < 4:
            print(f"   DEBUG: Skipping row {i} - too short")
            continue
        
        project = {
            'date': row[0] if len(row) > 0 else '',
            'role': row[1] if len(row) > 1 else '',
            'project_name': row[2] if len(row) > 2 else '',
            'task': row[3] if len(row) > 3 else '',
            'type': row[4] if len(row) > 4 else 'none',
            'media_source': row[5] if len(row) > 5 else '',
            'gallery_thumbnail': row[6] if len(row) > 6 else '',
            'description': row[7] if len(row) > 7 else '',
            'category': row[8] if len(row) > 8 else 'archive',
            'order': int(row[9]) if len(row) > 9 and row[9] and str(row[9]).isdigit() else 999,
            'visible': row[10].lower() == 'yes' if len(row) > 10 else True,
            'images': [],
            'thumbnail_image': None
        }
        
        print(f"   DEBUG: Project '{project['project_name']}' visible={project['visible']}")
        
        if project['visible']:
            projects.append(project)
    
    # Auto-sort by date (most recent first)
    projects.sort(key=lambda x: x['date'], reverse=True)
    return projects

def fetch_project_images(projects, api_key):
    """Fetch images from Google Drive for projects with drive_folder type"""
    for project in projects:
        if project['type'] == 'drive_folder' and project['media_source']:
            try:
                print(f"   📁 Fetching images for '{project['project_name']}'...")
                files = fetch_drive_folder_files(project['media_source'], api_key)
                
                thumbnail_found = False
                
                for file in files:
                    img_data = {
                        'id': file['id'],
                        'name': file['name'],
                        'url': get_drive_image_url(file['id']),
                        'thumbnail': file.get('thumbnailLink', '')
                    }
                    project['images'].append(img_data)
                    
                    # Check if this is the specified gallery thumbnail
                    if project['gallery_thumbnail'] and file['name'] == project['gallery_thumbnail']:
                        project['thumbnail_image'] = img_data
                        thumbnail_found = True
                
                # If no thumbnail specified or not found, use first image
                if not thumbnail_found and len(project['images']) > 0:
                    project['thumbnail_image'] = project['images'][0]
                
                print(f"      ✅ Found {len(project['images'])} images")
                if project.get('thumbnail_image'):
                    print(f"      🖼️  Gallery thumbnail: {project['thumbnail_image']['name']}")
            except Exception as e:
                print(f"      ⚠️  Error fetching Drive folder: {e}")
        
        elif project['type'] in ['image', 'video']:
            img_data = {
                'url': project['media_source'],
                'thumbnail': project.get('gallery_thumbnail', ''),
                'name': project['project_name']
            }
            project['images'].append(img_data)
            project['thumbnail_image'] = img_data
    
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

def get_css_links():
    """Generate CSS links - uses your existing styles.css"""
    return '<link rel="stylesheet" href="css/styles.css">'


def generate_gallery_project_html(project):
    """Generate HTML for a gallery project - shows only the chosen thumbnail"""
    # Use the specified thumbnail image
    if not project.get('thumbnail_image'):
        return ''
    
    img = project['thumbnail_image']
    
    if project['type'] == 'video':
        thumbnail = img.get('thumbnail', img['url'].replace('.mp4', '.png'))
        return f'                <a href="{img["url"]}"><img src="{thumbnail}" alt="{project["description"]}"></a>'
    else:
        return f'                <img src="{img["url"]}" alt="{project["description"]}">'

def generate_gallery_page(projects):
    """Generate the gallery/index page"""
    gallery_projects = [p for p in projects if p['category'].lower() in ['gallery', 'both'] and len(p['images']) > 0]
    
    project_html = '\n'.join([generate_gallery_project_html(p) for p in gallery_projects])
    css_links = get_css_links()
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>yukakinoki</title>
    {css_links}
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
</head>
<body>
    <nav>
        <ul>
            <li class="aboutbutton"><a href="info.html">INFO</a></li>
            <li class="gallerybutton active"><a href="index.html">GALLERY</a></li>
            <li class="listbutton"><a href="archive.html">ARCHIVE</a></li>
        </ul>
    </nav>
    
    <div class="gallery-section">
        <div class="sample">
            <div class="scroll-container">
{project_html}
            </div>
        </div>
    </div>
    
    <footer>
        <p>Copyright © {datetime.now().year}, <span style="text-transform: lowercase;">yukakinoki.com</span></p>
    </footer>
</body>
</html>'''
    
    return html


def generate_archive_page(projects):
    """Generate INTERACTIVE archive page with clickable table rows"""
    
    # Sort by date (most recent first)
    sorted_projects = sorted(projects, key=lambda x: x['date'], reverse=True)
    
    # Generate table rows with data-tab attributes
    table_rows = []
    content_sections = []
    
    for i, project in enumerate(sorted_projects):
        task = project['task']
        if 'https://' in task or 'http://' in task:
            import re
            task = re.sub(r'(https?://[^\s]+)', r'<a href="\1" target="_blank">\1</a>', task)
        
        # Create unique ID for each project
        project_id = f"project-{i}"
        
        # Add table row with data-tab
        table_rows.append(f'''            <tr data-tab="{project_id}">
                <td>{project['date']}</td>
                <td>{project['role']}</td>
                <td>{project['project_name']}</td>
                <td>{task}</td>
            </tr>''')
        
        # Generate content section for this project
        if len(project['images']) > 0:
            images_html = []
            for img in project['images']:
                if project['type'] == 'video':
                    thumbnail = img.get('thumbnail', img['url'].replace('.mp4', '.png'))
                    images_html.append(f'                    <a href="{img["url"]}"><img src="{thumbnail}" alt="{project["description"]}"></a>')
                else:
                    images_html.append(f'                    <img src="{img["url"]}" alt="{project["description"]}">')
            
            content_sections.append(f'''        <div id="{project_id}" class="project-content">
            <div class="scroll-container">
{chr(10).join(images_html)}
            </div>
        </div>''')
        else:
            # No images - empty content section
            content_sections.append(f'''        <div id="{project_id}" class="project-content"></div>''')
    
    table_html = '\n'.join(table_rows)
    content_html = '\n'.join(content_sections)
    css_links = get_css_links()
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Archive - yukakinoki</title>
    {css_links}
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
</head>
<body>
    <nav>
        <ul>
            <li class="aboutbutton"><a href="info.html">INFO</a></li>
            <li class="gallerybutton"><a href="index.html">GALLERY</a></li>
            <li class="listbutton active"><a href="archive.html">ARCHIVE</a></li>
        </ul>
    </nav>
    
    <div class="archive-container">
        <div class="table-container">
            <div class="table-header">
                <button id="toggleTable" class="collapse-button">-</button>
            </div>
            <table class="table table-hover">
                <thead>
                    <tr>
                        <th>DATE</th>
                        <th>ROLE</th>
                        <th>PROJECT</th>
                        <th>TASK</th>
                    </tr>
                </thead>
                <tbody>
{table_html}
                </tbody>
            </table>
        </div>
        
        <div class="sample">
{content_html}
        </div>
    </div>
    
    <footer>
        <p>Copyright © {datetime.now().year}, <span style="text-transform: lowercase;">yukakinoki.com</span></p>
    </footer>
    
    <script src="js/scripts.js"></script>
</body>
</html>'''
    
    return html


def generate_info_page(info_data):
    """Generate the info page"""
    bio_en = info_data.get('bio_english', '''Yu Kakinoki is a billingual interdisciplinary designer, currently based in Tokyo. Have developed a distinct eye for aesthetics by growing up in California, Japan, Hong Kong, and London. The goal is to push the boundaries of storytelling through spatial design - whether it be a tangible room, a digital space, or both. This website was built through GitHub Pages with self-learnt HTML, CSS, JavaScript, and Bootstrap. My dissertation title was 'To what extent is the aura relevant to a work of art in the age of biocybernetic simulation?'
''')
    
    bio_jp = info_data.get('bio_japanese', '''柿木優は、現在東京を拠点に活動している学際的なバイリンガルデザイナーです。 カリフォルニア、香港、ロンドンと日本で生まれ育ち、独特なセンスを構築しました。ストーリーテリングの未来をデジタル、そして現実的な空間デザインを交えて追求しています。 事実上何でも独学で学べる世界に住んで幸せです！ このサイトは、HTML、CSS、JavaScript、および Bootstrapを自己学習し、GitHubページを通して構築しました。''')
    
    contact_email = info_data.get('contact_email', 'yukakinoki@gmail.com')
    contact_text = info_data.get('contact_text', 'contact')
    css_links = get_css_links()
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>yukakinoki</title>
    {css_links}
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
</head>
<body>
    <nav>
        <ul>
            <li class="aboutbutton active"><a href="info.html">INFO</a></li>
            <li class="gallerybutton"><a href="index.html">GALLERY</a></li>
            <li class="listbutton"><a href="archive.html">ARCHIVE</a></li>
        </ul>
    </nav>
    
    <main class="info">
        <section class="bio">
            <p>{bio_en}</p>
            <p>{bio_jp}</p>
        </section>
        <section class="contact">
            <a href="mailto:{contact_email}">{contact_text}</a>
        </section>
    </main>
    
    <footer>
        <p>Copyright © {datetime.now().year}, <span style="text-transform: lowercase;">yukakinoki.com</span></p>
    </footer>
</body>
</html>'''
    
    return html

def main():
    """Main build process"""
    print("🚀 Starting build process...")
    
    print("📊 Fetching data from Google Sheets...")
    
    try:
        project_rows = fetch_sheet_data(SHEET_ID, PROJECTS_RANGE, API_KEY)
        all_projects = parse_projects(project_rows)
        print(f"✅ Found {len(all_projects)} total projects")
        
        print("📸 Fetching images from Google Drive...")
        all_projects = fetch_project_images(all_projects, API_KEY)
        
        gallery_count = len([p for p in all_projects if p['category'].lower() in ['gallery', 'both'] and len(p['images']) > 0])
        total_images = sum(len(p['images']) for p in all_projects)
        print(f"✅ Total images loaded: {total_images}")
        print(f"   └─ {gallery_count} projects will appear in gallery")
        
        try:
            info_rows = fetch_sheet_data(SHEET_ID, INFO_RANGE, API_KEY)
            info_data = parse_info(info_rows)
            print(f"✅ Found info page content")
        except:
            print("⚠️  Info sheet not found, using defaults")
            info_data = {}
            
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("📝 Generating HTML pages...")
    
    gallery_html = generate_gallery_page(all_projects)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(gallery_html)
    print("✅ Generated index.html")
    
    archive_html = generate_archive_page(all_projects)
    with open('archive.html', 'w', encoding='utf-8') as f:
        f.write(archive_html)
    print("✅ Generated archive.html (interactive)")
    
    info_html = generate_info_page(info_data)
    with open('info.html', 'w', encoding='utf-8') as f:
        f.write(info_html)
    print("✅ Generated info.html")
    
    print("🎉 Build complete!")

if __name__ == '__main__':
    main()
