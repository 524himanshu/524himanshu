import os
import json
import re
import requests
from bs4 import BeautifulSoup

def fetch_github_contributions(username="524himanshu"):
    url = f"https://github.com/users/{username}/contributions"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }

    print(f"Fetching contribution data for @{username}...")
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print(f"Failed to fetch contributions: HTTP {res.status_code}")
        return None

    soup = BeautifulSoup(res.text, "html.parser")
    
    # Map tooltips by `for` attribute ID
    tooltip_map = {}
    for tt in soup.find_all("tool-tip"):
        for_id = tt.get("for")
        if for_id:
            tooltip_map[for_id] = tt.text.strip()

    # Parse contribution cells
    day_cells = soup.find_all(["rect", "td"], class_=re.compile(r"ContributionCalendar-day"))
    
    days_data = []
    total_contributions = 0

    for cell in day_cells:
        date = cell.get("data-date")
        if not date:
            continue
            
        level = cell.get("data-level", "0")
        try:
            level = int(level)
        except ValueError:
            level = 0

        cell_id = cell.get("id")
        tt_text = tooltip_map.get(cell_id, "")
        
        count = 0
        if tt_text:
            match = re.search(r"(\d+)\s+contribution", tt_text)
            if match:
                count = int(match.group(1))

        days_data.append({
            "date": date,
            "level": level,
            "count": count
        })
        total_contributions += count

    # Sort days by date
    days_data.sort(key=lambda x: x["date"])

    # Calculate streaks
    longest_streak = 0
    temp_streak = 0
    for d in days_data:
        if d["count"] > 0 or d["level"] > 0:
            temp_streak += 1
            if temp_streak > longest_streak:
                longest_streak = temp_streak
        else:
            temp_streak = 0

    current_streak = 0
    for d in reversed(days_data):
        if d["count"] > 0 or d["level"] > 0:
            current_streak += 1
        else:
            break

    result = {
        "username": username,
        "total": total_contributions,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "total_days": len(days_data),
        "days": days_data
    }

    # Save to data/contributions.json
    data_dir = os.path.join(r"C:\Users\asus\Desktop\hm\524himanshu", "data")
    os.makedirs(data_dir, exist_ok=True)
    json_path = os.path.join(data_dir, "contributions.json")
    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(f"Successfully saved {len(days_data)} days to {json_path}")
    print(f"Total Contributions: {total_contributions} | Current Streak: {current_streak} days | Longest Streak: {longest_streak} days")
    return result

if __name__ == "__main__":
    fetch_github_contributions("524himanshu")
