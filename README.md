# ECE 6610: Wireless Networks — Programming Assignment 1

Experiments with point-to-point networking, TCP over WiFi, hidden terminals,
MPDU aggregation, and RTS/CTS using **ns-3.47** and **Wireshark**.

**Due:** September 23, 2026, 11:59 PM ET  
**Names:** Pending — add all group members before submission.

**Group name:** Pending — agree on a name with the group.

## Start here

1. Clone the repository using the [Git and pull request guide](CONTRIBUTING.md).
2. Install the assignment's ns-3.47 and Wireshark tools using the course setup instructions.
3. Claim a task in the [team tracker](docs/TEAM.md) and create a task branch.
4. Save experiment settings and measurements in [results](results/README.md).
5. Write answers in the [report source](report/PA1.md), record [AI usage](report/AI_USAGE.md),
   and open a PR for a teammate to review.

The repository currently contains the provided WiFi starter and collaboration
templates. The Q1 and Q3 implementations, measurements, and final PDF are pending.

## Repository contents

| File | Purpose | Status |
| --- | --- | --- |
| `wifi6610.cc` | Provided WiFi starter code for Q2 and Q3 | Included |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Beginner Git, PR, merge, and conflict instructions | Ready |
| [docs/TEAM.md](docs/TEAM.md) | Task ownership and group coordination | Template |
| [results/README.md](results/README.md) | Experiment recording instructions | Ready |
| [results/experiments.csv](results/experiments.csv) | Shared experiment index | Empty template |
| [report/PA1.md](report/PA1.md) | Editable source for numbered answers | Outline |
| [report/AI_USAGE.md](report/AI_USAGE.md) | AI usage notes to append to the report | Template |
| [.github/pull_request_template.md](.github/pull_request_template.md) | Checklist for new PRs | Ready |
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
It is not included in this checkout; verify this checklist and the due date against
the course handout before starting.

## Working locally

**New to Git or pull requests?** Read the [group Git guide](CONTRIBUTING.md)
for setup, the branch-and-PR workflow, merging, conflict resolution, and common fixes.

Keep the ns-3 installation separate from this repository when practical. Edit and
run assignment simulations in its `scratch/` directory as required by the handout,
then copy the final source files back here before committing. Keep the provided
`wifi6610.cc` as a reference.

Record run settings and measured throughput as you work. Small result tables,
report sources, and figures may be committed alongside the final PDF. Generated
packet captures, build products, and submission ZIPs are ignored by default;
keep captures locally for Wireshark analysis.

### Reproducible experiments

Record the source commit, exact run command, tool version, topology, relevant
settings, and measurement interval for each experiment. Use one row per run in
[the experiment index](results/experiments.csv), with detailed notes or tables
beside it. Keep units explicit and distinguish per-station from total throughput.

The starter exposes `payloadSize`, `dataRate`, `tcpVariant`, `phyRate`,
`simulationTime`, and `pcap` as command-line options. Its aggregation, RTS, and
frequency settings are currently source variables, not command-line options.
Record any source edits used for a run so another teammate can reproduce it.

### Team workflow

Use one branch and PR per task. Update [task ownership](docs/TEAM.md) when taking
work, and request a teammate's review before merging. Coordinate edits to shared
report sections. Edit the Markdown sources first and have one person export the
final PDF after the answers are merged; see the [report instructions](report/PA1.md).

## AI usage summary

Append a separate summary to `PA1.pdf` using these exact headings:

- Prompts used
- Ideas the AI provided correctly with minimal guidance
- Ideas the AI provided that were incorrect or misleading

Include the assignment-planning and repository-setup interactions if used, and
update the summary as work continues.
Use [report/AI_USAGE.md](report/AI_USAGE.md) to collect these notes during the project.

## Submission

Submit one ZIP containing:

```text
PA1.pdf
q1.cc
q3.cc
```

One group member submits through Canvas. GitHub is for version control; pushing
to GitHub does not submit the assignment.

Before creating the ZIP:

- Finish every numbered answer and replace all pending fields in the report.
- Add the group name, every member's name, and the separate AI usage summary.
- Export the report to `PA1.pdf` at the repository root and inspect every page.
- Verify the final `q1.cc` and `q3.cc` run in the required ns-3 environment.
- Check that the ZIP contains the three required files and opens correctly.
- Have the designated submitter upload it and confirm the Canvas submission receipt.

## Joining the repository

Clone the existing repository and create a branch for your work using the
[group Git guide](CONTRIBUTING.md). The repository URL is
`https://github.gatech.edu/yzhang3841/wireless_network_pas.git`.
