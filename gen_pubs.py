#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "pyyaml",
# ]
# ///
"""
Simple Publication Sync Script

Generates missing publication pages from my_pubs.yml
"""

import datetime
import yaml
from pathlib import Path
import re

def load_publications(yaml_file):
    """Load publications from YAML file"""
    with open(yaml_file, 'r') as f:
        return yaml.safe_load(f)

def get_existing_pub_dirs(pubs_dir="pubs"):
    """Get set of existing publication directory names"""
    pubs_path = Path(pubs_dir)
    if not pubs_path.exists():
        pubs_path.mkdir()
        return set()
    
    return {item.name for item in pubs_path.iterdir() if item.is_dir()}

def generate_slug(pub_key, pub_data):
    """Generate URL-friendly slug from publication data"""
    title = pub_data.get('title', pub_key)
    
    # Handle title that might be a dict with 'value' key
    if isinstance(title, dict):
        title = title.get('value', pub_key)
    
    # Remove special characters and convert to lowercase
    slug = re.sub(r'[^\w\s-]', '', title)
    slug = re.sub(r'[-\s]+', '-', slug)
    slug = slug.lower().strip('-')
    
    # Limit length and add year
    # Note that date is sometimes a plain number (e.g., 2023)
    date = pub_data.get('date', '')
    if isinstance(date, int):
        date = str(date)
    elif isinstance(date, datetime.date):
        date = date.isoformat()
    year = date[:4]
    if year:
        slug = f"{slug[:30]}-{year}".strip('-')
    else:
        slug = slug[:30].strip('-')
    
    return slug

def extract_student_authors(authors):
    """Extract student authors (marked with *) and clean author list"""
    if isinstance(authors, str):
        authors = [authors]
    
    student_authors = []
    clean_authors = []
    
    for author in authors:
        if '*' in author:
            clean_name = author.replace('*', '').strip()
            student_authors.append(clean_name)
            clean_authors.append(clean_name)
        else:
            clean_authors.append(author)
    
    return student_authors, clean_authors

def generate_quarto_content(pub_key, pub_data):
    """Generate complete Quarto file content"""
    authors = pub_data.get('author', [])
    student_authors, clean_authors = extract_student_authors(authors)
    
    # Handle title that might be a dict with 'value' key
    title = pub_data.get('title', '')
    if isinstance(title, dict):
        title = title.get('value', '')
    
    # Build frontmatter
    frontmatter = {
        'title': title,
        'authors': clean_authors,
        'date': pub_data.get('date', ''),
        'categories': ["HCI", "NLP"]  # Default, customize as needed
    }
    
    # Add optional fields

    # Handle 'parent' as a list or dict
    parent = pub_data.get('parent')
    if parent:
        if isinstance(parent, list):
            parent = parent[0] if parent else {}
        if isinstance(parent, dict) and 'title' in parent:
            frontmatter['publication'] = parent['title']
    
    if 'abstract' in pub_data:
        frontmatter['abstract'] = pub_data['abstract']
    
    if 'url' in pub_data:
        frontmatter['url_pdf'] = pub_data['url']
    
    # Generate YAML frontmatter using yaml library
    content = "---\n"
    content += yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True)
    content += "---\n\n"
    
    # Add student author callout
    if student_authors:
        content += "::: {.callout-important}\n"
        if len(student_authors) == 1:
            content += f"Note: {student_authors[0]} is an undergraduate student\n"
        else:
            content += f"Note: {', '.join(student_authors)} are undergraduate students\n"
        content += ":::\n\n"
    
    # Add featured image
    content += "![](featured.png)\n\n"
    
    # Add publication link
    if 'url' in pub_data:
        # Handle 'parent' as a list or dict
        parent = pub_data.get('parent')
        venue = 'Publication'  # Default value
        if parent:
            if isinstance(parent, list):
                parent = parent[0] if parent else {}
            if isinstance(parent, dict) and 'title' in parent:
                venue = parent['title']
        content += f"[PDF]({pub_data['url']}) {venue}\n\n"
    
    # Add abstract
    content += "## Abstract\n\n"
    if 'abstract' in pub_data:
        content += f"{pub_data['abstract']}\n"
    else:
        content += "*Abstract to be added*\n"
    
    return content

def create_publication_page(pub_key, pub_data, slug, pubs_dir="pubs"):
    """Create publication directory and files"""
    pub_dir = Path(pubs_dir) / slug
    pub_dir.mkdir(exist_ok=True)
    
    # Create index.qmd
    index_file = pub_dir / "index.qmd"
    content = generate_quarto_content(pub_key, pub_data)
    
    with open(index_file, 'w') as f:
        f.write(content)
        
    print(f"Created: {pub_dir}")
    return pub_dir

def sync_publications(yaml_file="my_pubs.yml"):
    """Main sync function"""
    print(f"Syncing publications from {yaml_file}...")

    pubs_data = load_publications(yaml_file)
    existing_dirs = get_existing_pub_dirs()
    
    print(f"Loaded {len(pubs_data)} publications")
    print(f"Found {len(existing_dirs)} existing directories")
    
    created_count = 0
    
    for pub_key, pub_data in pubs_data.items():
        slug = generate_slug(pub_key, pub_data)
        
        if slug not in existing_dirs:
            create_publication_page(pub_key, pub_data, slug)
            created_count += 1
    
    if created_count == 0:
        print("✅ All publications already have pages!")
    else:
        print(f"\n🎉 Created {created_count} new publication pages")
        print("\nNext steps:")
        print("1. Add featured.png images")
        print("2. Review and enhance generated content")
        print("3. Commit changes to git")

if __name__ == "__main__":
    sync_publications()