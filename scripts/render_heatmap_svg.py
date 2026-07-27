<<<<<<< HEAD
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
=======
#!/usr/bin/env python3
"""
Render data/contributions.json (produced by fetch_contributions.py) as a proper
GitHub-style contribution heatmap SVG: a grid of rounded, colored BOXES in the
classic 53-week x 7-day calendar, revealed once with a diagonal line-after-line
slide-down (CSS keyframes, plays on load then freezes -- no looping "glow"), a
Less->More legend, and a real stats footer.

Run by .github/workflows/update-profile-art.yml after fetch_contributions.py.
"""
import datetime
import json
import os

HERE = os.path.dirname(__file__)
IN_PATH = os.path.join(HERE, "..", "data", "contributions.json")
OUT_PATH = os.path.join(HERE, "..", "contrib-heatmap.svg")

# GitHub-ish green ramp: empty -> brightest. Level 5 is a brighter neon top end.
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

CELL = 12
GAP = 3
STEP = CELL + GAP
PAD = 22
LEFT_LABEL_W = 30
TOP_LABEL_H = 20
TITLEBAR_H = 30

BG = "#0a0e14"
BG2 = "#0d1420"
FRAME = "#1f6feb"
MUTED = "#7d8590"
TEXT = "#e6edf3"
ACCENT = "#22d3ee"
GREEN = "#39d353"
GOLD = "#f2cc60"

# reveal timing (one-shot)
COL_T = 0.018   # per-column delay contribution (left -> right sweep)
ROW_T = 0.045   # per-row delay contribution (top -> bottom cascade)
CELL_DUR = 0.42


def level_for(count):
    if count == 0:
        return 0
    if count <= 5:
        return 1
    if count <= 15:
        return 2
    if count <= 30:
        return 3
    if count <= 50:
        return 4
    return 5


def build_grid(days):
    first = datetime.date.fromisoformat(days[0]["date"])
    lead_pad = (first.weekday() + 1) % 7  # sunday=0
    grid = []
    col = [None] * lead_pad
    for d in days:
        date = datetime.date.fromisoformat(d["date"])
        weekday = (date.weekday() + 1) % 7
        while len(col) < weekday:
            col.append(None)
        col.append((d["date"], d["count"], level_for(d["count"])))
        if len(col) == 7:
            grid.append(col)
            col = []
    if col:
        while len(col) < 7:
            col.append(None)
        grid.append(col)
    return grid


def render(data):
    days = data["days"]
    grid = build_grid(days)
    n_cols = len(grid)
    art_w = n_cols * STEP
    art_h = 7 * STEP

    month_labels = []
    seen_months = set()
    for ci, column in enumerate(grid):
        for cell in column:
            if cell is None:
                continue
            date = datetime.date.fromisoformat(cell[0])
            key = (date.year, date.month)
            if key not in seen_months and date.day <= 7:
                seen_months.add(key)
                month_labels.append((ci, date.strftime("%b")))
            break

    canvas_w = PAD + LEFT_LABEL_W + art_w + PAD
    stats_h = 88
    canvas_h = TITLEBAR_H + TOP_LABEL_H + art_h + stats_h + PAD

    css = f"""
@keyframes cell {{
  0%   {{ opacity: 0; transform: translateY(-6px); }}
  100% {{ opacity: 1; transform: translateY(0); }}
}}
.c {{ opacity: 0; animation: cell {CELL_DUR:.2f}s cubic-bezier(.2,.8,.2,1) both; }}
""".strip()

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_w}" height="{canvas_h}" '
        f'viewBox="0 0 {canvas_w} {canvas_h}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
        f'<style>{css}</style>',
        '<defs>'
        f'<linearGradient id="hbg" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient>'
        '</defs>',
        f'<rect width="{canvas_w}" height="{canvas_h}" rx="12" fill="url(#hbg)"/>',
        f'<rect x="0.5" y="0.5" width="{canvas_w-1}" height="{canvas_h-1}" rx="12" '
        f'fill="none" stroke="{FRAME}" stroke-width="1" stroke-opacity="0.55"/>',
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{canvas_w}" y2="{TITLEBAR_H}" stroke="{FRAME}" stroke-opacity="0.35"/>',
    ]
    for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
    parts.append(f'<text x="{canvas_w/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" '
                 f'text-anchor="middle">avi@github: ~/contributions --graph</text>')

    grid_top = TITLEBAR_H + TOP_LABEL_H
    grid_left = PAD + LEFT_LABEL_W

    for ci, label in month_labels:
        x = grid_left + ci * STEP
        parts.append(f'<text x="{x}" y="{TITLEBAR_H + 14}" fill="{MUTED}" font-size="10">{label}</text>')

    for wi, wname in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
        y = grid_top + wi * STEP + CELL * 0.78
        parts.append(f'<text x="{PAD}" y="{y:.1f}" fill="{MUTED}" font-size="9">{wname}</text>')

    # the boxes -- each a rounded rect, diagonal slide-down reveal (once, freeze)
    for ci, column in enumerate(grid):
        gx = grid_left + ci * STEP
        for ri, cell in enumerate(column):
            if cell is None:
                continue
            date_s, count, lvl = cell
            gy = grid_top + ri * STEP
            delay = ci * COL_T + ri * ROW_T
            plural = "s" if count != 1 else ""
            parts.append(
                f'<rect class="c" x="{gx}" y="{gy}" width="{CELL}" height="{CELL}" rx="2.5" '
                f'fill="{PALETTE[lvl]}" style="animation-delay:{delay:.3f}s">'
                f'<title>{date_s}: {count} contribution{plural}</title></rect>'
            )

    # legend: Less [][][][][] More (bottom-right of the grid)
    leg_y = grid_top + art_h + 6
    leg_x = canvas_w - PAD - (len(PALETTE) * (CELL - 1) + 70)
    parts.append(f'<text x="{leg_x}" y="{leg_y + CELL*0.8:.1f}" fill="{MUTED}" font-size="10" text-anchor="end">Less</text>')
    lx = leg_x + 8
    for lvl, color in enumerate(PALETTE):
        parts.append(f'<rect x="{lx}" y="{leg_y}" width="{CELL-1}" height="{CELL-1}" rx="2.2" fill="{color}"/>')
        lx += CELL
    parts.append(f'<text x="{lx + 4}" y="{leg_y + CELL*0.8:.1f}" fill="{MUTED}" font-size="10">More</text>')

    sep_y = leg_y + CELL + 14
    parts.append(f'<line x1="0" y1="{sep_y}" x2="{canvas_w}" y2="{sep_y}" stroke="{FRAME}" stroke-opacity="0.25"/>')

    cs = data["current_streak"]["length"]
    ls = data["longest_streak"]["length"]
    total = data["total_contributions"]
    best = data["best_day"]
    rng = data["range"]

    ly = sep_y + 24
    # left column: big highlighted numbers; right column: context in muted
    parts.append(f'<text x="{PAD}" y="{ly}" font-size="13" fill="{GREEN}">'
                 f'<tspan font-weight="700">{total:,}</tspan>'
                 f'<tspan fill="{MUTED}"> contributions in the last year</tspan></text>')
    parts.append(f'<text x="{canvas_w - PAD}" y="{ly}" font-size="12" fill="{MUTED}" text-anchor="end">'
                 f'{rng["start"]} &#8594; {rng["end"]}</text>')
    ly += 24
    parts.append(f'<text x="{PAD}" y="{ly}" font-size="13" fill="{MUTED}">current streak '
                 f'<tspan fill="{ACCENT}" font-weight="700">{cs} days</tspan>'
                 f'<tspan fill="{MUTED}">   &#183;   longest </tspan>'
                 f'<tspan fill="{ACCENT}" font-weight="700">{ls} days</tspan></text>')
    parts.append(f'<text x="{canvas_w - PAD}" y="{ly}" font-size="12" fill="{MUTED}" text-anchor="end">'
                 f'best day <tspan fill="{GOLD}" font-weight="700">{best["count"]}</tspan> on {best["date"]}</text>')

    parts.append("</svg>")
    return "".join(parts)


if __name__ == "__main__":
    data = json.load(open(IN_PATH))
    svg = render(data)
    with open(OUT_PATH, "w") as f:
        f.write(svg)
    print(f"wrote {OUT_PATH} ({len(svg)} bytes)")
>>>>>>> 9991a2c (Refactor code structure for improved readability and maintainability)
