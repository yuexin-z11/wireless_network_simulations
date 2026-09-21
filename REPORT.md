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

Pending.

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

- Asked Codex to organize the repository as a general network simulation project
  and prepare it for the personal GitHub repository, retaining experiment provenance
  and AI disclosure.

- Asked Codex to complete Q2-2 by running the distance sweep in 5 m increments
  and recording the actual results and transmission-range estimate.

- Asked Codex to run Q2-1 and record the actual final throughput and explanation.

- Asked Codex to simplify the repository, consolidate the report and AI notes,
  and remove redundant templates and duplicate files.

Known prompts from the repository documentation work:

- "add a instruction page for the people dont know how to do prs or new to git since this will be a group project. they need to know how to merge and resolve problems"
- "do i push now?"
- "now i did that but prepare the rest of the readme file and everything for me to push"
- Asked Codex to inspect the PA1 starter and local ns-3 environment, then install ns-3.47 on Ubuntu.
- "can you add what commants to run to a requirement file so that everything can be installed for others running one command to get the environment set up?"
- Asked Codex to expand the README with environment prerequisites, installation,
  verification, and assignment file setup instructions, then prepare a local Git
  commit while leaving the push command for the user.

Pending: Add earlier planning/setup prompts and later code, analysis, or report
prompts used by any group member. Include the tool/model if required by the handout.

- Asked Codex to create separate Q1, Q2, and Q3 working files and prepare them for
  GitHub, leaving the actual push to the user. Files were copied from the tutorial
  and supplied WiFi starter, with comments identifying unfinished assignment work.

## Ideas the AI provided correctly with minimal guidance

- Added a distance command-line option without changing the 10 m default, compiled
  the source, and ran 76 distance cases. Confirmed the 10 m result matched Q2-1
  and recorded the first zero at 380 m with the last positive result at 375 m.

- Ran the supplied WiFi simulation with HtMcs4 and three seconds of activity;
  recorded the final throughput directly from the saved output and kept the
  protocol-overhead explanation separate from measured results.

- Created separate `q1.cc`, `wifi6610.cc`, and `q3.cc` starter copies. All three
  compiled under ns-3.47, and the repository and scratch copies matched. This
  was a build check only; assignment configurations and measurements are pending.

- Created an Ubuntu package list and setup script for ns-3.47, Wireshark, and
  tshark. On Ubuntu 26.04, the configured ns-3 modules and examples compiled,
  the unmodified `first` tutorial completed a UDP echo exchange, and rerunning
  the setup script against the installation succeeded. These checks verify the
  environment only; the tutorial output is not PA1 measurement data.

Pending: Review the generated Git guide, repository documentation, and templates
and record what the group verified to be correct. Add later verified contributions
and explain how they were checked.

## Ideas the AI provided that were incorrect or misleading

The earlier README incorrectly said to set Q2's `simulationTime` to 4 seconds.
Using the supplied assignment instructions, this was corrected to 3 seconds of
activity, with the simulation stopping at 4 seconds.

Pending: Record errors, misleading suggestions, and corrections found during
review or experiments. If none are found after review, state that explicitly.
