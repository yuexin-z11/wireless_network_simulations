# ECE 6610: Wireless Networks — Programming Assignment 1

Experiments with point-to-point networking, TCP over WiFi, hidden terminals,
MPDU aggregation, and RTS/CTS using **ns-3.47** and **Wireshark**.

**Due:** September 23, 2026, 11:59 PM ET  
**Names:** TODO  
**Group name:** TODO

## Repository contents

| File | Purpose | Status |
| --- | --- | --- |
| `wifi6610.cc` | Provided WiFi starter code for Q2 and Q3 | Included |
| `q1.cc` | Two-node PPP/UDP echo simulation | To create |
| `q3.cc` | Two-STA WiFi simulation with hidden terminals | To create |
| `PA1.pdf` | Numbered answers, measurements, and AI usage summary | To create |

## Assignment checklist

- [ ] Set up ns-3.47 and Wireshark.
- [ ] Q1: Copy `examples/tutorial/first.cc` to ns-3's `scratch/q1.cc`, configure the assigned link and applications, and capture both nodes.
- [ ] Q1: Answer Q1-1 through Q1-4 using simulation output and packet captures.
- [ ] Q2: Use `wifi6610.cc` with `simulationTime` set to 4 seconds; measure throughput and sweep distance in 5-meter steps.
- [ ] Q2: Capture a run with STA and AP within 5 meters and answer Q2-1 through Q2-4.
- [ ] Q3: Add a second transmitting STA and compare aggregation settings at positions -10 and +10 meters from the AP.
- [ ] Q3: Choose hidden-terminal positions using the Q2 range measurement, keeping both STAs within AP range.
- [ ] Q3: Compare all four aggregation/RTS combinations with 10 seconds of network activity and answer Q3-1 through Q3-5.
- [ ] Save the hidden-terminal simulation as `q3.cc`.
- [ ] Complete `PA1.pdf` with names, group name, and all numbered answers.
- [ ] Package `PA1.pdf`, `q1.cc`, and `q3.cc` into one ZIP for Canvas.

The assignment handout is the source of truth for detailed settings and questions.

## Working locally

Keep the ns-3 installation separate from this repository when practical. Edit and
run assignment simulations in its `scratch/` directory as required by the handout,
then copy the final source files back here before committing. Keep the provided
`wifi6610.cc` as a reference.

Record run settings and measured throughput as you work. Small result tables,
report sources, and figures may be committed alongside the final PDF. Generated
packet captures, build products, and submission ZIPs are ignored by default;
keep captures locally for Wireshark analysis.

## AI usage summary

Append a separate summary to `PA1.pdf` using these exact headings:

- Prompts used
- Ideas the AI provided correctly with minimal guidance
- Ideas the AI provided that were incorrect or misleading

Include the assignment-planning and repository-setup interactions if used, and
update the summary as work continues.

## Submission

Submit one ZIP containing:

```text
PA1.pdf
q1.cc
q3.cc
```

One group member submits through Canvas. GitHub is for version control; pushing
to GitHub does not submit the assignment.

## First commit and push

After reviewing the repository, run these commands yourself:

```bash
git add README.md .gitignore wifi6610.cc
git commit -m "Set up PA1 repository"
git branch -M main
git push -u origin main
```

The `origin` remote is configured as
`https://github.gatech.edu/yzhang3841/wireless_network_pas.git`.
If the remote already has commits, reconcile its history before pushing.
