import os
import json
from datetime import datetime

def render_heatmap_svg(json_path=r"C:\Users\asus\Desktop\hm\524himanshu\data\contributions.json", output_svg=r"C:\Users\asus\Desktop\hm\524himanshu\contrib-heatmap.svg"):
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found. Run fetch_contributions.py first.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    days = data.get("days", [])
    total = data.get("total", 0)
    streak = data.get("current_streak", 0)
    longest = data.get("longest_streak", 0)
    username = data.get("username", "524himanshu")

    # GitHub Green Palette Ramp
    PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

    # Calculate grid layout
    box_size = 11
    box_gap = 3
    start_x = 45
    start_y = 65

    weeks = []
    current_week = []
    
    for idx, d in enumerate(days):
        current_week.append(d)
        if len(current_week) == 7 or idx == len(days) - 1:
            weeks.append(current_week)
            current_week = []

    # Months labels extraction
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month_labels = []
    prev_month = -1

    for w_idx, week in enumerate(weeks):
        if week:
            dt = datetime.strptime(week[0]["date"], "%Y-%m-%d")
            if dt.month != prev_month:
                month_labels.append((w_idx, months[dt.month - 1]))
                prev_month = dt.month

    # Generate SVG Content
    svg = []
    svg.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 220" width="860" height="220">')
    svg.append('  <defs>')
    svg.append('    <linearGradient id="bg-grad-heat" x1="0%" y1="0%" x2="100%" y2="100%">')
    svg.append('      <stop offset="0%" stop-color="#0D1117" />')
    svg.append('      <stop offset="100%" stop-color="#161B22" />')
    svg.append('    </linearGradient>')
    svg.append('    <filter id="shadow-heat" x="-5%" y="-5%" width="110%" height="110%">')
    svg.append('      <feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#000000" flood-opacity="0.5" />')
    svg.append('    </filter>')
    svg.append('  </defs>')

    svg.append('  <style>')
    svg.append('    .font-mono { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }')
    svg.append('    .font-sans { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }')
    svg.append('  </style>')

    # Background Card
    svg.append('  <rect width="860" height="220" rx="16" fill="url(#bg-grad-heat)" stroke="rgba(255,255,255,0.1)" stroke-width="1.5" filter="url(#shadow-heat)" />')

    # Header Bar (Top)
    svg.append('  <g transform="translate(24, 28)" class="font-sans">')
    svg.append(f'    <text font-size="14" font-weight="700" fill="#F8FAFC">📊 GitHub Contribution Activity <tspan fill="#39D353">(@{username})</tspan></text>')
    svg.append('  </g>')

    # Month Labels Row (Spaced cleanly below header)
    svg.append('  <g transform="translate(0, 0)" class="font-mono" font-size="10" fill="#8B949E">')
    for w_idx, label in month_labels:
        x_pos = start_x + (w_idx * (box_size + box_gap))
        svg.append(f'    <text x="{x_pos}" y="{start_y - 10}">{label}</text>')
    svg.append('  </g>')

    # Day Labels Column
    day_names = ["Mon", "Wed", "Fri"]
    day_indices = [1, 3, 5]
    svg.append('  <g class="font-mono" font-size="9" fill="#8B949E">')
    for d_idx, d_name in zip(day_indices, day_names):
        y_pos = start_y + (d_idx * (box_size + box_gap)) + 9
        svg.append(f'    <text x="16" y="{y_pos}">{d_name}</text>')
    svg.append('  </g>')

    # Grid Rectangles
    svg.append('  <g>')
    for w_idx, week in enumerate(weeks):
        for d_idx, day_data in enumerate(week):
            x = start_x + (w_idx * (box_size + box_gap))
            y = start_y + (d_idx * (box_size + box_gap))
            lvl = min(4, max(0, day_data["level"]))
            color = PALETTE[lvl]
            date_str = day_data["date"]
            cnt = day_data["count"]

            delay = (w_idx * 0.02) + (d_idx * 0.008)
            svg.append(f'    <rect x="{x}" y="{y}" width="{box_size}" height="{box_size}" rx="2" fill="{color}">')
            svg.append(f'      <title>{cnt} contributions on {date_str}</title>')
            svg.append(f'      <animate attributeName="opacity" from="0" to="1" dur="0.3s" begin="{delay:.2f}s" fill="freeze" />')
            svg.append('    </rect>')
    svg.append('  </g>')

    # Footer & Legend
    svg.append('  <g transform="translate(24, 198)" class="font-mono" font-size="11">')
    svg.append(f'    <text fill="#8B949E"><tspan fill="#39D353" font-weight="700">{total:,}</tspan> contributions in the last year • <tspan fill="#58A6FF">Streak: {streak}d</tspan> • <tspan fill="#D2A8FF">Longest: {longest}d</tspan></text>')

    # Legend
    svg.append('    <g transform="translate(680, -10)" font-size="10" fill="#8B949E">')
    svg.append('      <text x="-30" y="9">Less</text>')
    for i, c in enumerate(PALETTE):
        lx = i * 13
        svg.append(f'      <rect x="{lx}" y="0" width="10" height="10" rx="2" fill="{c}" />')
    svg.append('      <text x="68" y="9">More</text>')
    svg.append('    </g>')
    svg.append('  </g>')

    svg.append('</svg>')

    with open(output_svg, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))

    print(f"Successfully re-rendered heatmap SVG at {output_svg}")

if __name__ == "__main__":
    render_heatmap_svg()
