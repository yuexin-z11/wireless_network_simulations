# Wireless Network Simulations

Reproducible C++ experiments with **ns-3.47** and Wireshark: wired UDP echo,
802.11n TCP throughput, and the effect of distance on wireless delivery.
Two-station hidden-terminal and RTS/CTS experiments are planned.

## Results and status

- **WiFi baseline:** 31.9758 Mbit/s received throughput at 10 m, with 100 Mbps
  application offered load, HtMcs4, and 3 seconds of activity.
- **Distance sweep:** 76 runs from 5 to 380 m in 5 m steps. The last positive
  throughput was 0.274773 Mbit/s at 375 m; the first zero was at 380 m.
- **Beacon interval:** 102.4 ms, confirmed from the first second of a 5 m PCAP.
- **Remaining:** first-STA-frame analysis, verification of the updated wired capture,
  and the two-station aggregation/RTS experiments.

These results describe the recorded simulator settings and seed, not a universal
WiFi range. See [the report](REPORT.md) and [raw measurement records](experiments.csv).

## Files

| File | Purpose |
| --- | --- |
| `q1.cc` | Two-node wired UDP echo simulation with PCAP tracing |
| `wifi6610.cc` | Single-STA WiFi TCP simulation with a configurable distance |
| `q3.cc` | Starter for two-STA experiments; currently still one STA |
| [REPORT.md](REPORT.md) | Experiment explanations, full distance table, and AI disclosure |
| [experiments.csv](experiments.csv) | 78 experiment records with commands, settings, and source provenance |
| [setup-ns3.sh](setup-ns3.sh) | Ubuntu setup and tutorial verification |
| [requirements-ubuntu.txt](requirements-ubuntu.txt) | Ubuntu package dependencies |

The simulations originated in ECE 6610 coursework. Original source filenames and
report question numbers are retained for traceability. Source copyright notices
are preserved.

## Set up Ubuntu

Ubuntu must already be installed, directly or through WSL2 on Windows. Use an
Ubuntu terminal and a regular Linux user with sudo access, not root. You need
internet access and several GB of free space. The setup was verified on Ubuntu
26.04. If Git is missing, install it with `sudo apt-get install git` after
`sudo apt-get update`, then clone the repository:

```bash
git clone https://github.com/yuexin-z11/wireless_network.git
cd wireless_network
bash setup-ns3.sh
```

For an existing checkout, open its directory and run `bash setup-ns3.sh`.
The script installs the listed Ubuntu packages, including Wireshark and tshark,
then downloads, builds, and checks ns-3.47 in `~/ns-3.47`. Do not use `pip` for
this requirements file. The script requests sudo only for installing packages.
The build takes several minutes and ends by running the unmodified `first`
tutorial; that output verifies the environment rather than measuring these experiments.

An existing extracted ns-3.47 installation is reused, preserving source and
`scratch/` files while updating its build configuration. A downloaded archive
alone is not detected. For another installation path or fewer build jobs:

```bash
NS3_DIR="$HOME/ns-3.47" NS3_JOBS=2 bash setup-ns3.sh
```

Use an absolute `NS3_DIR` and substitute it in the commands below if different.
A different version at the destination is rejected. Do not run simultaneous builds
against one installation. Build logs are saved inside the ns-3 directory.
The setup runs a tutorial check, not the full ns-3 test suite.

## Copy and run the working files

From the Git repository directory:

```bash
cp -i q1.cc wifi6610.cc q3.cc ~/ns-3.47/scratch/
cd ~/ns-3.47
cat VERSION
./ns3 build q1 wifi6610 q3 -j 4
./ns3 run q1
```

If prompted to overwrite, preserve any newer work in `scratch/`. Always run
`./ns3` from the ns-3 root, never from `scratch/`, and never with sudo.
Git pull only updates the repository; it does not sync `scratch/` automatically.

Q1 currently writes captures into `scratch/`. Open `scratch/q1-0-0.pcap` in
Wireshark for the client's timestamps, or inspect it from the ns-3 root:

```bash
tshark -r scratch/q1-0-0.pcap -Y 'udp.port == 6610'
```

Wireshark needs an Ubuntu desktop or WSLg for its window. Use File → Open for
saved captures; live capture permissions are unnecessary. Terminal-only users
can use tshark.

For the WiFi baseline, run from the ns-3 root:

```bash
./ns3 run 'wifi6610 --phyRate=HtMcs4 --simulationTime=3 --distance=10'
```

This gives 3 seconds of activity, stopping at 4 seconds. Change `--distance` to
repeat the experiment at another distance. To reproduce the sweep, use 5, 10, 15,
... meters and record the final `Average throughput:` value, stopping at the first
zero. Add `--pcap=1` to enable WiFi captures. The intermediate output covers 100 ms
intervals, not the final average.

`q3.cc` must first be adapted for two transmitting STAs before running the planned
10-second hidden-terminal experiments. It is currently only a one-STA starter.

## Record and share work

Record each run in `experiments.csv`: source commit, exact command, ns-3 version,
topology, traffic/PHY settings, aggregation/RTS settings, seed if relevant,
measurement interval, value, units, and local PCAP reference. Distinguish aggregate
and per-station throughput. Leave missing values blank; do not invent results.
Write analysis and AI disclosure in `REPORT.md`.

After editing files in `scratch/`, copy the changed sources back to this repository
before committing. From the repository, copy back the changed sources:

```bash
cp -i ~/ns-3.47/scratch/q1.cc ~/ns-3.47/scratch/q3.cc .
```

Copy back `wifi6610.cc` too if you changed it. Check `git status` and `git diff`,
then stage only your intended files and commit. Use a task branch and open a PR
for teammate review. The user runs the final push command; Codex does not push.
The original supplied `wifi6610-v2.cc` remains available in Git history.

## Branches and merging

A branch keeps your task separate from `main`. A pull request (PR) asks the group
to review and merge that branch. When `main` is protected, changes must follow
the required PR approvals and checks. Do not bypass branch protection.

1. **Start a task.** With a clean working tree (`git status`), update `main` and
   create a branch. Replace `yourname/q1` with your name and task:

   ```bash
   git switch main
   git pull --ff-only origin main
   git switch -c yourname/q1
   ```

   If you already have uncommitted work, preserve it on a task branch before
   switching to `main`; do not discard it to follow these steps.

2. **Save and share.** Review your edits, stage only the intended files, and commit.
   This example assumes you changed `q1.cc`; substitute your actual files:

   ```bash
   git diff
   git add q1.cc
   git diff --cached
   git commit -m "Update Q1 simulation"
   git push -u origin yourname/q1
   ```

   Run the push yourself. Codex prepares local changes and leaves pushing to you.
   A push uploads your branch; it does not merge it into `main`.

3. **Open a PR on GitHub.** Choose `main` as the base and your task branch as the
   compare branch. Describe the changes and checks, then request a teammate's
   review. Address comments and satisfy the required approvals and checks shown
   on the PR. Push follow-up commits to the same branch to update the PR.

4. **Resolve conflicts if needed.** With your task branch checked out and local
   edits committed, run `git fetch origin`, then `git merge origin/main`. Edit
   conflicting files to keep the intended combined result and remove conflict
   markers. Stage the resolved files, run `git commit`, check the code, and push
   your branch again. Do not force-push or bypass branch protection.

5. **Merge and update.** Once GitHub allows merging, use the PR's merge button
   with a merge method permitted by the repository. Then update your local copy:

   ```bash
   git switch main
   git pull --ff-only origin main
   ```

   Create a fresh task branch for the next change. Updating the repository does
   not update the separate ns-3 `scratch/` copies.

## Troubleshooting

- **Root error:** Switch to your regular Ubuntu account; do not use sudo for ns-3.
- **Missing setup script:** Run from the repository directory with the latest files.
- **Download/package error:** Resolve the reported network or apt error and rerun setup.
- **Compiler killed:** Free memory and retry with `NS3_JOBS=2 bash setup-ns3.sh`.
- **Wrong existing version:** Select a different `NS3_DIR` without deleting your work.
- **No Wireshark window:** Use a graphical Ubuntu/WSLg session or tshark.

## Outputs

Keep generated PCAPs, logs, build files, and archives local; `.gitignore` excludes
them. Commit reproducible commands, source changes, and measured tables. Raw log
paths in `experiments.csv` refer to the machine that ran the experiments; rerun the
recorded commands to produce local logs on another machine. The report includes
unfinished sections so planned work remains distinguishable from measured results.
