import requests
import concurrent.futures
from typing import List, Dict, Any

# The official external WhatsMyName OSINT database (100% Free & Open Source)
WMN_API_URL = "https://raw.githubusercontent.com/WebBreacher/WhatsMyName/main/wmn-data.json"

CHECK_ENDPOINTS = {
    "github": "https://github.com/{username}",
    "reddit": "https://www.reddit.com/user/{username}/about.json",
    "medium": "https://medium.com/@{username}",
    "substack": "https://{username}.substack.com",
    "pinterest": "https://www.pinterest.com/{username}/",
    "soundcloud": "https://soundcloud.com/{username}",
    "steam": "https://steamcommunity.com/id/{username}",
    "behance": "https://www.behance.net/{username}",
    "dribbble": "https://dribbble.com/{username}"
}

def sweep_external_endpoints(username: str) -> List[Dict[str, Any]]:
    discovered = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }

    def check_target(platform: str, url_template: str):
        target_url = url_template.format(username=username)
        display_url = target_url.replace("/about.json", "") if platform == "reddit" else target_url
        
        try:
            # Use GET with stream=True to avoid downloading full page bodies
            res = requests.get(target_url, headers=headers, timeout=5, allow_redirects=True, stream=True)
            
            if platform == "reddit":
                if res.status_code == 200:
                    return {"platform": platform, "username": username, "profile_url": display_url}
            else:
                # 200 means active; 403 often means the page exists behind a bot shield
                if res.status_code in [200, 403]:
                    return {"platform": platform, "username": username, "profile_url": display_url}
        except Exception as e:
            print(f"[OSINT DEBUG] {platform} check failed: {e}")
        return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(check_target, platform, template) 
            for platform, template in CHECK_ENDPOINTS.items()
        ]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                discovered.append(result)
                
    return discovered