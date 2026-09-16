# ECE 6610: Wireless Networks — Programming Assignment 1

Experiments with point-to-point networking, TCP over WiFi, hidden terminals,
MPDU aggregation, and RTS/CTS using **ns-3.47** and **Wireshark**.

**Due:** September 23, 2026, 11:59 PM ET  
**Names:** Pending — add all group members before submission.

**Group name:** Pending — agree on a name with the group.

## Start here

1. Clone the repository using the [Git and pull request guide](CONTRIBUTING.md).
2. Install ns-3.47 and Wireshark using the one-command Ubuntu setup below.
3. Claim a task in the [team tracker](docs/TEAM.md) and create a task branch.
4. Save experiment settings and measurements in [results](results/README.md).
5. Write answers in the [report source](report/PA1.md), record [AI usage](report/AI_USAGE.md),
   and open a PR for a teammate to review.

The repository currently contains the provided WiFi starter and collaboration
templates. The Q1 and Q3 implementations, measurements, and final PDF are pending.

## Repository contents

| File | Purpose | Status |
| --- | --- | --- |
| `wifi6610-v2.cc` | Updated WiFi starter code for Q2 and Q3 (`HtMcs4`) | Included |
| [requirements-ubuntu.txt](requirements-ubuntu.txt) | Ubuntu packages for the assignment environment | Ready |
| [scripts/setup-ns3.sh](scripts/setup-ns3.sh) | One-command ns-3.47 and Wireshark setup | Ready |
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
- [ ] Q2: Use `wifi6610-v2.cc` with `phyRate=HtMcs4` and `simulationTime=3` (stop at 4 seconds); measure throughput and sweep distance in 5-meter steps.
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

## One-command Ubuntu setup

### 1. Prepare Ubuntu and get the repository

Use an Ubuntu terminal, including Ubuntu on WSL2 if working on Windows. Run these
commands inside Ubuntu, not PowerShell. You need a regular Linux account with
sudo access, an internet connection, and several GB of free disk space. The setup
has been checked on Ubuntu 26.04. A graphical desktop or WSLg is needed to open
Wireshark windows; terminal capture analysis works without a GUI.

Check your current account:

```bash
whoami
```

If this prints `root`, switch to your regular Ubuntu account before continuing.
Do not run the setup script or `./ns3` with `sudo`.

Make sure you can access the group's repository while signed in to Georgia Tech
GitHub. If Git is not installed, install it first:

```bash
sudo apt-get update
sudo apt-get install -y git
```

For a new checkout:

```bash
cd ~
git clone https://github.gatech.edu/yzhang3841/wireless_network_pas.git
cd wireless_network_pas
```

If you already cloned the repository, open that folder instead. Until the setup
changes are merged into `main`, they are on branch `docs/git-guide`; after the
author pushes them, a fresh clone can access them with `git switch docs/git-guide`.
See [CONTRIBUTING.md](CONTRIBUTING.md) for authentication and branch instructions.

### 2. Install the requirements and build ns-3

From the repository directory, run:

```bash
bash scripts/setup-ns3.sh
```

The script installs the packages in [requirements-ubuntu.txt](requirements-ubuntu.txt),
downloads the official **ns-3.47** release to `~/ns-3.47`, builds the assignment's
wired and WiFi modules and their dependencies, and runs the unmodified `first`
tutorial to verify the installation. It asks for your sudo password only if system
packages need installing. Internet access and several minutes for the initial
build are required. This requirements file is for Ubuntu packages, not `pip`.
The procedure follows the [official installation guide](https://www.nsnam.org/docs/release/3.47/installation/singlehtml/index.html).

An existing ns-3.47 installation is reused without replacing its sources or
`scratch/` files; its build configuration is updated for this assignment. A different
installation at the destination is rejected. Build and tutorial output are saved
as `installation-build.log` and `installation-first.log` inside the ns-3 directory.
Tests are disabled; the tutorial run is a smoke check, not the full ns-3 test suite.
Do not run multiple setup/build processes against the same installation at once.

For a different location or a smaller build parallelism, use:

```bash
NS3_DIR="$HOME/ns-3.47" NS3_JOBS=2 bash scripts/setup-ns3.sh
```

If you use a custom `NS3_DIR`, substitute that path for `~/ns-3.47` in the remaining
instructions. For WSL, keeping the installation under your Linux home directory
also keeps generated build files separate from the Git checkout.

### 3. Verify the environment

Run from the ns-3 root:

```bash
cd ~/ns-3.47
cat VERSION
./ns3 run first
tshark --version
```

`VERSION` should show `3.47`. The unmodified tutorial should print a client send,
server receive/reply, and client receive. Its default addresses, port, and timing
are tutorial settings, not the required Q1 configuration or Q1 results.

The setup does not create `q1.cc` or `q3.cc` or generate assignment measurements.
Wireshark's graphical interface needs a desktop or WSLg; `tshark` can inspect saved
PCAPs in a terminal. No live network capture permissions are needed for ns-3 PCAPs.

### 4. Prepare assignment work after setup

Work through Q1, then Q2, then Q3. Place working C++ source files under
`~/ns-3.47/scratch/`, but run every `./ns3` command from `~/ns-3.47`, never from
`scratch/`. Before creating a file, inspect `scratch/` and preserve existing work.

- **Q1:** Copy `examples/tutorial/first.cc` to `scratch/q1.cc`, configure it using
  the assignment, then build with `./ns3 build q1` and run with `./ns3 run q1`.
- **Q2:** Copy the repository's `wifi6610-v2.cc` to `scratch/wifi6610.cc`.
  Use `./ns3 run 'wifi6610 --phyRate=HtMcs4 --simulationTime=3'` for the required
  runtime. Add `--pcap=1` inside the quotes when captures are needed.
- **Q3:** Create `scratch/q3.cc` from the WiFi starter and implement the two-STA
  configuration. Build with `./ns3 build q3`, then run with 10 seconds of activity.

The copy step renames the Q2 working file so its ns-3 target is `wifi6610`.
Keep `wifi6610-v2.cc` unchanged as the reference. There is no required `q2.cc`
deliverable. Save measurements in `results/` and copy the finished `q1.cc` and
`q3.cc` back to the Git repository before committing them.

For generated captures, use Wireshark's **File → Open** to select the `.pcap`
file in the ns-3 directory. For a terminal-only Q1 inspection, after generating
the capture, run:

```bash
cd ~/ns-3.47
tshark -r q1-0-0.pcap -Y 'udp.port == 6610'
```

### Setup troubleshooting

- **Missing script:** Check that you are in the repository directory and have the
  branch containing the setup files.
- **Root-user error:** Use your regular Ubuntu account; the script requests sudo
  only for package installation.
- **Download or apt error:** Check internet access and the actual error, resolve
  it, then rerun the same setup command.
- **Compiler killed or insufficient memory:** Close other memory-heavy programs
  and rerun with `NS3_JOBS=2 bash scripts/setup-ns3.sh` from the repository.
- **Destination already contains a different installation:** Choose another
  absolute `NS3_DIR`; do not delete an existing project to make room.
- **Wireshark cannot open a window:** Use an Ubuntu desktop/WSLg session or use
  `tshark` to inspect the saved captures.

## Working locally

**New to Git or pull requests?** Read the [group Git guide](CONTRIBUTING.md)
for setup, the branch-and-PR workflow, merging, conflict resolution, and common fixes.

Keep the ns-3 installation separate from this repository when practical. Edit and
run assignment simulations in its `scratch/` directory as required by the handout,
then copy the final source files back here before committing. Keep the provided
`wifi6610-v2.cc` as a reference.

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
