# Wireless Network Simulations

C++ experiments using **ns-3.47** to study UDP echo latency, TCP throughput over
802.11n, wireless transmission range, and beacon timing. Wireshark and tshark
provide packet-level inspection of generated PCAPs.

## Contents

| File | Purpose |
| --- | --- |
| `udp-echo.cc` | Two-node wired UDP echo simulation with PCAP tracing |
| `wifi-throughput.cc` | WiFi TCP simulation with configurable distance, data rate, and duration |
| [experiments.csv](experiments.csv) | 78 measured records with settings and source provenance |
| [setup-ns3.sh](setup-ns3.sh) | Ubuntu dependency installation and ns-3.47 build |
| [requirements-ubuntu.txt](requirements-ubuntu.txt) | Ubuntu packages used by setup |

## Setup

Use Ubuntu, either natively or through WSL2, with a regular user account that has
sudo access. Ubuntu/WSL must already be installed. You need internet access and
several GB of free space. The setup has been checked on Ubuntu 26.04.

If Git is missing, run `sudo apt-get update` followed by `sudo apt-get install git`.
Then, in an Ubuntu terminal:

```bash
git clone https://github.com/yuexin-z11/wireless_network.git
cd wireless_network
bash setup-ns3.sh
```

Setup installs Wireshark, tshark, and build dependencies, downloads ns-3.47 to
`~/ns-3.47`, builds the required modules, and runs the unmodified `first` tutorial
as an environment check. The requirements file is for Ubuntu packages, not pip.
Run setup as your regular user, not root; it requests sudo for packages only.

An existing extracted ns-3.47 tree is reused without replacing its source or
scratch files. A downloaded archive alone is not detected. For a different path
or reduced memory use:

```bash
NS3_DIR="$HOME/ns-3.47" NS3_JOBS=2 bash setup-ns3.sh
```

Substitute your chosen absolute path in subsequent commands. A different version
at the destination is rejected. Do not build the same installation concurrently.
Setup performs a tutorial smoke check, not the full ns-3 test suite.

## Run simulations

From the repository directory, copy the sources into ns-3:

```bash
cp -i udp-echo.cc wifi-throughput.cc ~/ns-3.47/scratch/
cd ~/ns-3.47
./ns3 build udp-echo wifi-throughput -j 4
```

Preserve newer scratch files if prompted to overwrite. Run every `./ns3` command
from the ns-3 root, never from `scratch/` and never with sudo.

### Wired UDP echo

```bash
./ns3 run udp-echo
```

The client and server use a 1 Mbps link with a 10 ms one-way channel delay,
1024-byte UDP payloads, port 6610, and addresses 192.168.1.1 and 192.168.1.2.
The client starts at 2 seconds, sends every 2 seconds, and stops at 10 seconds.
Captures are written as `udp-echo-0-0.pcap` and `udp-echo-1-0.pcap` in the ns-3 root.
Use request and reply timestamps from the client capture when calculating RTT:

```bash
tshark -r udp-echo-0-0.pcap -Y 'udp.port == 6610'
```

### WiFi TCP baseline

```bash
./ns3 run 'wifi-throughput --phyRate=HtMcs4 --simulationTime=3 --distance=10'
```

The AP is at the origin and the STA at `(distance, 0, 0)` meters. Traffic starts
at 1 second; `simulationTime=3` gives a stop time of 4 seconds. Record the final
`Average throughput:` line; earlier lines describe separate 100 ms intervals.

To repeat the distance experiment, vary `--distance` in 5 m steps and stop at the
first zero final throughput. Other options include `--dataRate`, `--payloadSize`,
`--tcpVariant`, and `--pcap`. Aggregation and RTS settings remain source variables.

### Beacon captures

```bash
./ns3 run 'wifi-throughput --phyRate=HtMcs4 --simulationTime=3 --distance=5 --pcap=1'
tshark -r wifi-ap-0-0.pcap \
  -Y 'wlan.fc.type_subtype == 0x08 && frame.time_epoch < 1' \
  -T fields -e frame.time_epoch -e wlan.fixed.beacon
```

The AP and STA captures use the `wifi-ap` and `wifi-sta` prefixes. Open them with
Wireshark's File → Open, or use tshark without a graphical desktop. No live-capture
permissions are required. ns-3 epoch timestamps represent simulation time, so the
filter above selects beacons before simulation time 1 second.

## Recorded results

All WiFi runs used ns-3.47, HtMcs4, 5 GHz, a 20 MHz channel, 800 ns guard interval,
TCP NewReno, a 100 Mbps offered rate, large A-MPDU enabled, and RTS/CTS disabled.
The default random seed/run was 1/1. Full values and commands are in `experiments.csv`.

| Measurement | Result |
| --- | --- |
| Final received throughput at 10 m | 31.9758 Mbit/s |
| Distance sweep | 76 runs, 5–380 m in 5 m steps |
| Last tested positive throughput | 0.274773 Mbit/s at 375 m |
| First zero-throughput distance | 380 m |
| Beacon interval at 5 m | 100 TU = 102.4 ms |

The beacon field was checked against ten beacons in the first second: timestamps
ran from 0.005860 to 0.927460 seconds, with all nine gaps equal to 0.1024 seconds.
The offered rate exceeds received throughput because the PHY rate, protocol
overhead, channel access, acknowledgments, and TCP behavior limit useful delivery.
The range is specific to this model, seed, and short measurement window, not a
universal WiFi range. Wired measurements are not included in this result table.

Measurements were collected before the source files and capture prefixes were
renamed. CSV commands use the current executable names; source commits and hashes
refer to the code used for the original runs. Packet captures and logs remain on
the measurement machine and are not bundled; rerun commands to generate your own.

## Contributing

Git pull updates this repository, not the separate ns-3 scratch copies. Copy edited
sources back from scratch before committing. Work on a task branch, push that
branch, and open a PR into `main`. For protected branches, satisfy the required
reviews and checks before merging; do not bypass protection or force-push.

With a clean working tree, start with `git switch main`, `git pull --ff-only`, and
`git switch -c feature/your-change`. After committing, push your branch manually.
Resolve conflicts on that branch, then merge the PR and update local `main`.

## Troubleshooting

- **Root error:** Use your regular Ubuntu user, without sudo for ns-3.
- **Compiler killed:** Close memory-heavy applications and rerun setup with `NS3_JOBS=2`.
- **Download/package failure:** Resolve the reported network or apt error, then rerun setup.
- **Wireshark window unavailable:** Use an Ubuntu desktop/WSLg session or tshark.

## Attribution

The simulations adapt ns-3 examples and supplied WiFi code; source copyright and
license notices are retained. AI assistance supported setup, code comments, the
distance option, simulation execution, packet analysis, and documentation. Numerical
results were recorded from actual simulation output and captures.
