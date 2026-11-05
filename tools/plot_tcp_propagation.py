"""Generate a standalone SVG plot of the recorded TCP propagation sweep."""

import csv
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "tcp-propagation.csv"
FIGURE = ROOT / "figures" / "tcp-propagation.svg"

with DATA.open(newline="") as file:
    rows = list(csv.DictReader(file))

sweep = sorted(
    ((int(row["one_way_delay_ms"]), float(row["sink_throughput_mbps"]))
     for row in rows if row["link_rate_mbps"] == "100")
)
baseline = [(int(row["one_way_delay_ms"]), float(row["sink_throughput_mbps"]))
            for row in rows if row["link_rate_mbps"] == "10"]
assert [delay for delay, _ in sweep] == [1, 5, 10, 15, 20, 25, 30]
assert len(baseline) == 1 and baseline[0][0] == 30

left, right, top, bottom = 100, 900, 112, 444


def x_position(delay):
    return left + delay / 30 * (right - left)


def y_position(throughput):
    return bottom - throughput / 55 * (bottom - top)


def label(value, x, y, size=16, anchor="middle", fill="#253344"):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" '
            f'fill="{fill}">{escape(str(value))}</text>')


parts = [
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 980 570" '
    'role="img" aria-labelledby="plot-title plot-description">',
    '<title id="plot-title">TCP throughput versus wired propagation delay</title>',
    '<desc id="plot-description">Seven measurements at a 100 Mbps wired link; '
    'throughput falls from 49.511 Mbps at 1 ms to 16.5488 Mbps at 30 ms. '
    'A 10 Mbps baseline at 30 ms reaches 9.26536 Mbps.</desc>',
    '<rect width="980" height="570" fill="white"/>',
    '<g font-family="Arial, Helvetica, sans-serif">',
    label("TCP throughput versus wired propagation delay", 490, 47, 24),
    label("100 Mbps wired link, with a 10 Mbps baseline", 490, 74, 15, fill="#526071"),
]

for throughput in range(0, 51, 10):
    y = y_position(throughput)
    parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{right}" y2="{y:.1f}" '
                 'stroke="#d9e1e8"/>')
    parts.append(label(throughput, left - 16, f"{y + 6:.1f}", anchor="end"))

for delay in (1, 5, 10, 15, 20, 25, 30):
    x = x_position(delay)
    parts.append(f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{bottom}" '
                 'stroke="#edf1f5"/>')
    parts.append(label(delay, f"{x:.1f}", bottom + 28))

parts.append(f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" '
             'stroke="#253344" stroke-width="2"/>')
parts.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" '
             'stroke="#253344" stroke-width="2"/>')
points = " ".join(f"{x_position(delay):.1f},{y_position(value):.1f}"
                  for delay, value in sweep)
parts.append(f'<polyline points="{points}" fill="none" stroke="#1768a8" '
             'stroke-width="4" stroke-linejoin="round"/>')
for delay, value in sweep:
    parts.append(f'<circle cx="{x_position(delay):.1f}" cy="{y_position(value):.1f}" '
                 'r="6" fill="#1768a8"/>')
delay, value = baseline[0]
parts.append(f'<circle cx="{x_position(delay):.1f}" cy="{y_position(value):.1f}" '
             'r="7" fill="#d97732"/>')
parts.extend([
    '<line x1="610" y1="126" x2="645" y2="126" stroke="#1768a8" stroke-width="4"/>',
    label("100 Mbps", 655, 132, 15, anchor="start"),
    '<circle cx="628" cy="154" r="7" fill="#d97732"/>',
    label("10 Mbps baseline", 655, 160, 15, anchor="start"),
    label("Wired one-way propagation delay (ms)", 500, 509, 18),
    '<text x="31" y="278" transform="rotate(-90 31 278)" text-anchor="middle" '
    'font-size="18" fill="#253344">Sink average throughput (Mbps)</text>',
    label("Propagation-only RTT = 2 × one-way delay", 500, 543, 14, fill="#526071"),
    '</g></svg>',
])

FIGURE.write_text("\n".join(parts) + "\n")
print(FIGURE)
