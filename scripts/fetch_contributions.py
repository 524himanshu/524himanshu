<<<<<<< HEAD
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
=======
#!/usr/bin/env python3
"""
Scrape real daily contribution counts from GitHub's public, unauthenticated
contributions endpoint (the same fragment the profile page itself uses) and
write data/contributions.json with the raw days plus derived stats
(current streak, longest streak, best day, monthly totals).

No token, no auth, no GraphQL -- just the public HTML GitHub already serves.
Run daily by .github/workflows/update-profile-art.yml.
"""
import datetime
import json
import os
import re
import sys

import requests
from bs4 import BeautifulSoup

USERNAME = os.environ.get("GH_PROFILE_USER", "AVIVASHISHTA29")
URL = f"https://github.com/users/{USERNAME}/contributions"
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "contributions.json")


def fetch_days():
    resp = requests.get(URL, headers={"User-Agent": "profile-readme-bot/1.0"}, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    cells = soup.select("td.ContributionCalendar-day")
    if not cells:
        print("no calendar cells found -- github markup may have changed", file=sys.stderr)
        sys.exit(1)

    days = []
    for td in cells:
        date = td.get("data-date")
        if not date:
            continue
        td_id = td.get("id")
        tooltip_el = soup.find("tool-tip", attrs={"for": td_id}) if td_id else None
        text = tooltip_el.get_text(strip=True) if tooltip_el else ""
        if re.search(r"no contributions", text, re.I):
            count = 0
        else:
            m = re.match(r"(\d+)", text)
            count = int(m.group(1)) if m else 0
        days.append({"date": date, "count": count})

    days.sort(key=lambda d: d["date"])
    return days


def compute_current_streak(days):
    idx = len(days) - 1
    if days[idx]["count"] == 0:
        idx -= 1  # today isn't over yet -- don't break the streak on it
    streak = 0
    end_idx = idx
    while idx >= 0 and days[idx]["count"] > 0:
        streak += 1
        idx -= 1
    start_idx = idx + 1
    if streak == 0:
        return 0, None, None
    return streak, days[start_idx]["date"], days[end_idx]["date"]


def compute_longest_streak(days):
    longest = run = 0
    longest_start = longest_end = None
    run_start_idx = None
    for i, d in enumerate(days):
        if d["count"] > 0:
            if run == 0:
                run_start_idx = i
            run += 1
            if run > longest:
                longest = run
                longest_start = days[run_start_idx]["date"]
                longest_end = days[i]["date"]
        else:
            run = 0
    return longest, longest_start, longest_end


def build_data(days):
    total = sum(d["count"] for d in days)
    active_days = sum(1 for d in days if d["count"] > 0)
    best = max(days, key=lambda d: d["count"])
    cur_len, cur_start, cur_end = compute_current_streak(days)
    long_len, long_start, long_end = compute_longest_streak(days)

    monthly = {}
    for d in days:
        key = d["date"][:7]
        monthly[key] = monthly.get(key, 0) + d["count"]
    monthly_list = [{"month": k, "total": v} for k, v in sorted(monthly.items())]

    return {
        "username": USERNAME,
        "generated_at": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "range": {"start": days[0]["date"], "end": days[-1]["date"]},
        "total_contributions": total,
        "active_days": active_days,
        "avg_per_active_day": round(total / active_days, 1) if active_days else 0,
        "current_streak": {"length": cur_len, "start": cur_start, "end": cur_end},
        "longest_streak": {"length": long_len, "start": long_start, "end": long_end},
        "best_day": {"date": best["date"], "count": best["count"]},
        "monthly": monthly_list,
        "days": days,
    }


if __name__ == "__main__":
    days = fetch_days()
    data = build_data(days)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w") as f:
        json.dump(data, f, indent=2)
    print(f"wrote {OUT_PATH}: {data['total_contributions']} contributions, "
          f"current streak {data['current_streak']['length']}, "
          f"longest streak {data['longest_streak']['length']}")
>>>>>>> 9991a2c (Refactor code structure for improved readability and maintainability)
