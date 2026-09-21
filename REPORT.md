# Network Simulation Report

Group name: Group 3

Members: [everyone's name].

This report records wired and wireless ns-3 experiments. It originated in ECE 6610
coursework; numbered questions are retained for traceability. Sections marked
Pending have not been completed. Measurements are in [experiments.csv](experiments.csv),
and AI usage is disclosed separately at the end.

## Q1

### Q1-1

Pending.

### Q1-2

Pending.

### Q1-3

Pending.

### Q1-4

Pending.

## Q2

### Q2-1

**Configuration:** The client application offers **100 Mbps** (`dataRate="100Mbps"`).
The AP is at (0, 0, 0) m and the STA at (10, 0, 0) m. The run uses ns-3.47,
802.11n at 5 GHz, HtMcs4, a 20 MHz channel, and the default 800 ns guard interval.
Large A-MPDU is enabled and RTS/CTS is disabled; TCP is NewReno.

**Measured result:** The simulation printed **Average throughput: 31.9758 Mbit/s**.
This is the final application-layer receive throughput, calculated by the starter
as `sink->GetTotalRx() * 8 / (1e6 * simulationTime)`, with `simulationTime=3`.
Traffic starts at 1 s and simulation stops at 4 s. The intermediate printed
values cover 100 ms intervals and are not the final average.

Command (run from the ns-3 root):

```bash
./ns3 run "wifi6610 --phyRate=HtMcs4 --simulationTime=3"
```

**Explanation (reasoning):** The configured application rate is the offered load,
not a guarantee of delivered throughput. HtMcs4 limits the physical transmission
rate; WiFi preambles, MAC/IP/TCP headers, contention/backoff, interframe spacing,
and acknowledgments consume airtime. TCP flow/congestion control and connection
startup also affect delivery during this short run. Thus the useful payload rate
at the AP is below the offered 100 Mbps even with aggregation. This run measures
the total received throughput, not the individual contribution of each overhead.

Run details are in `experiments.csv` under `q2-1-baseline`; raw output is saved
locally at `/home/yuexin/ns-3.47/q2-1-baseline.log`.

### Q2-2

**Measured distance sweep:** Using ns-3.47, HtMcs4, and 3 seconds of activity,
we moved the STA from 5 m to 380 m in 5 m increments with the AP at the origin.
All other settings matched Q2-1. A `--distance` option was added to the working
source; its default remains 10 m. The 10 m run reproduced Q2-1's 31.9758 Mbit/s.

Example command from the ns-3 root (replace 5 with each tested distance):

```bash
./ns3 run "wifi6610 --phyRate=HtMcs4 --simulationTime=3 --distance=5"
```

The **first zero-throughput distance was 380 m**. Following the assignment's
first-zero convention, use **Rtx ≈ 380 m**. The last tested positive throughput
was **0.274773 Mbit/s at 375 m**, so the observed transition lies between 375 m
and 380 m at this 5 m resolution. Do not treat the zero-throughput 380 m point
as a verified working AP link when choosing Q3 positions.

These are single-run results with default seed/run 1/1 and a 3-second measurement
window, not a universal radio range. Throughput varies slightly before dropping
sharply near the cutoff. Increased path loss and resulting delivery failures
provide a model-based explanation; this sweep measures throughput, not individual
PHY losses or retry counts.

| Distance (m) | Final throughput (Mbit/s) |
| --- | --- |
| 5 | 31.9797 |
| 10 | 31.9758 |
| 15 | 31.9758 |
| 20 | 31.9915 |
| 25 | 31.9797 |
| 30 | 31.9797 |
| 35 | 31.9758 |
| 40 | 30.28 |
| 45 | 30.2761 |
| 50 | 30.2761 |
| 55 | 30.2761 |
| 60 | 30.2761 |
| 65 | 30.2761 |
| 70 | 30.2761 |
| 75 | 30.2761 |
| 80 | 30.2761 |
| 85 | 30.28 |
| 90 | 30.3428 |
| 95 | 30.3428 |
| 100 | 30.3428 |
| 105 | 30.3428 |
| 110 | 30.3428 |
| 115 | 30.3428 |
| 120 | 30.3428 |
| 125 | 30.4998 |
| 130 | 30.4959 |
| 135 | 30.3428 |
| 140 | 30.3428 |
| 145 | 30.3428 |
| 150 | 30.4998 |
| 155 | 30.4998 |
| 160 | 30.4959 |
| 165 | 30.4959 |
| 170 | 30.4959 |
| 175 | 30.2722 |
| 180 | 30.2722 |
| 185 | 30.2722 |
| 190 | 30.2722 |
| 195 | 30.2722 |
| 200 | 30.2722 |
| 205 | 30.2682 |
| 210 | 30.2682 |
| 215 | 30.2094 |
| 220 | 30.2094 |
| 225 | 30.2682 |
| 230 | 30.2682 |
| 235 | 30.2682 |
| 240 | 30.2722 |
| 245 | 30.2682 |
| 250 | 30.2682 |
| 255 | 30.2643 |
| 260 | 30.4959 |
| 265 | 30.3428 |
| 270 | 30.3821 |
| 275 | 30.6726 |
| 280 | 31.3477 |
| 285 | 31.23 |
| 290 | 30.0877 |
| 295 | 30.3428 |
| 300 | 30.4606 |
| 305 | 29.5421 |
| 310 | 28.2938 |
| 315 | 27.3792 |
| 320 | 25.6324 |
| 325 | 24.0152 |
| 330 | 21.6325 |
| 335 | 19.3166 |
| 340 | 15.6974 |
| 345 | 12.6788 |
| 350 | 9.71913 |
| 355 | 6.35904 |
| 360 | 4.01954 |
| 365 | 2.0294 |
| 370 | 0.981333 |
| 375 | 0.274773 |
| 380 | 0 |

All 76 runs are recorded in `experiments.csv`. Raw outputs remain locally in
`/home/yuexin/ns-3.47/q2-distance-logs/`.

### Q2-3

**Measured beacon interval: 102.4 ms (0.1024 s).** With the AP at (0,0,0) m and
STA at (5,0,0) m, PCAP tracing was enabled using the existing `--pcap=1` option:

```bash
./ns3 run "wifi6610 --phyRate=HtMcs4 --simulationTime=3 --distance=5 --pcap=1"
```

In the AP capture, only beacons in the first simulation second were inspected.
Their fixed-parameter Beacon Interval field was **100 TU**, which Wireshark
explicitly decoded as **0.102400 seconds** (1 TU = 1024 microseconds). All nine
consecutive timestamp differences were also exactly **0.102400 s**.

| Frame | Simulation timestamp (s) |
| --- | --- |
| 1 | 0.005860000 |
| 2 | 0.108260000 |
| 9 | 0.210660000 |
| 10 | 0.313060000 |
| 11 | 0.415460000 |
| 12 | 0.517860000 |
| 13 | 0.620260000 |
| 14 | 0.722660000 |
| 15 | 0.825060000 |
| 16 | 0.927460000 |

Wireshark/tshark display filter:

```text
wlan.fc.type_subtype == 0x08 && frame.time_epoch < 1
```

These ns-3 captures use simulation time as their epoch timestamps, so this filter
selects the first second rather than one second after the first captured frame.
The source address of all ten beacons was the AP, `00:00:00:00:00:01`.
Evidence is saved locally in `/home/yuexin/ns-3.47/q2-3-captures/`, including the
AP and STA captures, run log, and first-second beacon table. The beacon interval
is read from the capture, not assumed from a simulator default.

### Q2-4

Pending.

## Q3

### Q3-1

Pending.

### Q3-2

Pending.

### Q3-3

Pending.

### Q3-4

Pending.

### Q3-5

Pending.

---

# AI usage summary

## Prompts used

Selected prompts (summarized):

- “Help me install ns-3.47 and Wireshark on Ubuntu.”
- “Review my Q1 code against the assignment requirements.”
- “Explain why application data rate and measured throughput differ.”
- “Add comments explaining the code changes.”
- “Help organize the repository and draft explanations of the results.”

## Ideas the AI provided correctly with minimal guidance

I also used Codex to add explanatory comments to the code, identifying the
modified sections and explaining their purpose.

The AI helped prepare the setup script and working source copies, reviewed Q1
settings, and added the Q2 distance option and explanatory comments. It ran the
Q2 baseline and 5 m distance sweep, recorded actual simulation output, and used
PCAP fields and timestamps to determine the beacon interval. It also helped
explain offered data rate versus measured throughput and organize the report.
The recorded numerical results came from simulation runs and packet captures.

## Ideas the AI provided that were incorrect or misleading

An earlier AI-generated README incorrectly specified `simulationTime=4` for Q2.
This was corrected to `simulationTime=3`: traffic starts at 1 second and the
simulation stops at 4 seconds.
