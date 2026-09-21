#!/usr/bin/env bash
# Run from any directory: bash /path/to/wireless_network/setup-ns3.sh
set -euo pipefail

if (( EUID == 0 )); then
    echo 'Run this script as your regular Ubuntu user, without sudo.' >&2
    echo 'It requests sudo only when Ubuntu packages need installing.' >&2
    exit 1
fi

if [[ ! -r /etc/os-release ]]; then
    echo 'This setup script requires Ubuntu.' >&2
    exit 1
fi
source /etc/os-release
if [[ ${ID:-} != ubuntu ]]; then
    echo 'This setup script supports Ubuntu; see the ns-3 guide for other systems.' >&2
    exit 1
fi

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
ns3_version=3.47
ns3_dir=${NS3_DIR:-"$HOME/ns-$ns3_version"}
jobs=${NS3_JOBS:-4}
if [[ $ns3_dir != /* || ! $jobs =~ ^[1-9][0-9]*$ ]]; then
    echo 'NS3_DIR must be an absolute path; NS3_JOBS must be a positive integer.' >&2
    exit 1
fi

# Reject an unrelated directory before making any changes.
if [[ -e $ns3_dir ]]; then
    if [[ ! -f $ns3_dir/VERSION || ! -f $ns3_dir/ns3 ]] ||
       [[ $(tr -d '[:space:]' < "$ns3_dir/VERSION") != "$ns3_version" ]]; then
        echo "Refusing to overwrite an existing directory that is not ns-$ns3_version: $ns3_dir" >&2
        exit 1
    fi
fi

packages=()
while IFS= read -r package || [[ -n $package ]]; do
    [[ -z $package || $package == \#* ]] && continue
    packages+=("$package")
done < "$script_dir/requirements-ubuntu.txt"

missing=()
for package in "${packages[@]}"; do
    if [[ $(dpkg-query -W -f='${Status}' "$package" 2>/dev/null || true) != 'install ok installed' ]]; then
        missing+=("$package")
    fi
done
if (( ${#missing[@]} )); then
    sudo apt-get update
    # Offline PCAP inspection does not require privileged live-capture access.
    sudo env DEBIAN_FRONTEND=noninteractive apt-get install -y "${missing[@]}"
fi

download_dir=
cleanup() {
    if [[ -n $download_dir && -d $download_dir ]]; then
        rm -rf -- "$download_dir"
    fi
}
trap cleanup EXIT

if [[ ! -e $ns3_dir ]]; then
    mkdir -p -- "$(dirname -- "$ns3_dir")"
    download_dir=$(mktemp -d "$(dirname -- "$ns3_dir")/.ns3-download.XXXXXX")
    curl --fail --location --retry 3 --connect-timeout 30 \
        "https://www.nsnam.org/release/ns-$ns3_version.tar.bz2" \
        --output "$download_dir/ns3.tar.bz2"
    tar -xjf "$download_dir/ns3.tar.bz2" -C "$download_dir"
    [[ $(tr -d '[:space:]' < "$download_dir/ns-$ns3_version/VERSION") == "$ns3_version" ]]
    # -T prevents accidentally nesting the source tree inside an existing folder.
    mv -T -- "$download_dir/ns-$ns3_version" "$ns3_dir"
fi

cd -- "$ns3_dir"
echo "Building ns-3 $ns3_version in $ns3_dir using $jobs jobs."
./ns3 configure --enable-examples --disable-tests \
    --enable-modules=core,network,internet,point-to-point,applications,wifi,mobility,flow-monitor
./ns3 build -j "$jobs" 2>&1 | tee installation-build.log
./ns3 run first 2>&1 | tee installation-first.log

printf '\nSetup complete: %s\n' "$ns3_dir"
printf 'Verified the unmodified first tutorial; these are not experiment results.\n'
printf 'For project work, put sources in scratch/ and run ./ns3 from this root.\n'
printf 'Wireshark and tshark are installed for PCAP inspection.\n'
