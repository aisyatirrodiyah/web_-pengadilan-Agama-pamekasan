import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

# Base URL
BASE_URL = "https://pa-pamekasan.go.id"

# Target URLs based on categories
URLS = {
    "Pimpinan": "https://pa-pamekasan.go.id/halaman/content/pimpinan",
    "Hakim": "https://pa-pamekasan.go.id/halaman/content/hakim",
    "Kepaniteraan": "https://pa-pamekasan.go.id/halaman/content/kepaniteraan",
    "Kesekretariatan": "https://pa-pamekasan.go.id/halaman/content/kesekretariatan",
    "PPNPN": "https://pa-pamekasan.go.id/pages/ppnpn"
}

# Image Directory
IMG_DIR = os.path.join("assets", "img")

def sanitize_filename(name):
    """Sanitize name to be used as a filename."""
    return re.sub(r'[^\w\s-]', '', name).strip().replace(' ', '_').lower()

def setup():
    """Create necessary directories."""
    if not os.path.exists(IMG_DIR):
        os.makedirs(IMG_DIR)
        print(f"Created directory: {IMG_DIR}")

def download_image(url, name):
    """Download image and return the local path."""
    try:
        # Handle cases where URL might have spaces
        url = url.replace(' ', '%20')
        response = requests.get(url, stream=True, timeout=15)
        if response.status_code == 200:
            # Try to get extension from URL or content type
            ext = "jpg"
            if '.' in url:
                potential_ext = url.split('.')[-1].split('?')[0].lower()
                if potential_ext in ['jpg', 'jpeg', 'png', 'webp', 'gif']:
                    ext = potential_ext
            
            filename = f"{sanitize_filename(name)}.{ext}"
            filepath = os.path.join(IMG_DIR, filename)
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return filepath.replace('\\', '/') # Use forward slashes for web
    except Exception as e:
        print(f"   [!] Error downloading image for {name}: {e}")
    return None

def scrape_category(category, url):
    """Scrape staff data from a specific category URL."""
    print(f"[*] Scraping {category} from: {url}")
    staff_data = []
    try:
        # Use a user-agent to avoid being blocked
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = 'utf-8' # Ensure UTF-8
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Staff are usually inside table cells
        cells = soup.find_all('td')
        
        for cell in cells:
            img_tag = cell.find('img')
            strong_tags = cell.find_all('strong')
            
            if img_tag and strong_tags:
                name = strong_tags[0].get_text(strip=True)
                
                # Extract NIP from cell text
                cell_text = cell.get_text(" ", strip=True)
                nip_match = re.search(r'NIP[\.\s:]*([\d\.]+)', cell_text)
                nip = nip_match.group(1).strip() if nip_match else ""
                
                # Position is usually the second strong tag, or just use the category
                position = category
                if len(strong_tags) > 1:
                    potential_pos = strong_tags[1].get_text(strip=True)
                    # If potential_pos contains NIP, it's not the position, try next
                    if nip and nip in potential_pos:
                        if len(strong_tags) > 2:
                            position = strong_tags[2].get_text(strip=True)
                    else:
                        position = potential_pos
                
                # Filter out generic entries
                if len(name) < 3 or name.lower() in ['pimpinan', 'hakim', 'kepaniteraan', 'kesekretariatan']:
                    continue
                
                img_src = img_tag.get('src')
                if img_src:
                    full_img_url = urljoin(BASE_URL, img_src)
                    
                    print(f"   [+] Found: {name} | NIP: {nip} | Pos: {position}")
                    
                    # Download image
                    local_path = download_image(full_img_url, name)
                    
                    staff_data.append({
                        "name": name,
                        "nip": nip,
                        "position": position,
                        "category": category,
                        "original_img_url": full_img_url,
                        "local_img_path": local_path
                    })
                    
    except Exception as e:
        print(f"   [!] Error scraping {category}: {e}")
        
    return staff_data

def main():
    setup()
    all_staff = []
    
    for category, url in URLS.items():
        category_data = scrape_category(category, url)
        all_staff.extend(category_data)
        print(f"   [v] Found {len(category_data)} staff in {category}\n")
    
    # Save to JSON
    output_file = "staff_data.json"
    with open(output_file, "w", encoding='utf-8') as f:
        json.dump(all_staff, f, indent=4, ensure_ascii=False)
        
    print(f"--- SUCCESS ---")
    print(f"Total staff scraped: {len(all_staff)}")
    print(f"Data saved to: {output_file}")
    print(f"Images saved to: {IMG_DIR}")

if __name__ == "__main__":
    main()
