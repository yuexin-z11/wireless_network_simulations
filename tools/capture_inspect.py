#!/usr/bin/env python3
"""Summarize Wi-Fi beacons or IP-to-Ethernet source mappings in a PCAP capture."""

import argparse
from collections import Counter, defaultdict
import ipaddress
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def capture_rows(capture: Path, display_filter: str, fields: tuple[str, ...]):
    """Yield TShark field rows without retaining the entire capture in memory."""
    command = [
        "tshark", "-r", str(capture), "-Y", display_filter,
        "-T", "fields", "-E", "separator=\t", "-E", "occurrence=a",
        "-E", "aggregator=,",
    ]
    for field in fields:
        command.extend(("-e", field))

    with tempfile.TemporaryFile(mode="w+t") as errors:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=errors, text=True)
        assert process.stdout is not None
        for line in process.stdout:
            values = line.rstrip("\r\n").split("\t")
            yield dict(zip(fields, values + [""] * (len(fields) - len(values))))
        if process.wait() != 0:
            errors.seek(0)
            raise RuntimeError(errors.read().strip() or "TShark could not read the capture")


def decode_ssid(value: str) -> str:
    if not value:
        return ""
    try:
        return bytes.fromhex(value).decode("utf-8", errors="replace")
    except ValueError:
        return value


def max_legacy_rate(value: str):
    """Rate octets use 500 kb/s units; bit 7 marks a basic rate."""
    if not value:
        return None
    try:
        return max((int(octet, 16) & 0x7f) / 2 for octet in value.split(","))
    except ValueError:
        return None


def as_number(value: str):
    if not value:
        return None
    number = float(value)
    return int(number) if number.is_integer() else number


def beacon_summary(capture: Path, ssid_filter: str | None):
    fields = (
        "frame.number", "wlan.ssid", "wlan.ta", "wlan.ht.info.primarychannel",
        "wlan.ds.current_channel", "wlan_radio.channel", "wlan_radio.frequency",
        "wlan.fixed.beacon", "wlan_radio.phy", "wlan_radio.data_rate",
        "wlan.supported_rates", "wlan.extended_supported_rates",
    )
    networks = {}
    for row in capture_rows(capture, "wlan.fc.type == 0 && wlan.fc.subtype == 8", fields):
        ssid = decode_ssid(row["wlan.ssid"])
        if ssid_filter is not None and ssid != ssid_filter:
            continue
        transmitter = row["wlan.ta"] or None
        key = (ssid, transmitter)
        if key not in networks:
            interval = as_number(row["wlan.fixed.beacon"])
            networks[key] = {
                "ssid": ssid,
                "transmitter_mac": transmitter,
                "beacon_count": 0,
                "first_frame": int(row["frame.number"]),
                "primary_channel": as_number(
                    row["wlan.ht.info.primarychannel"]
                    or row["wlan.ds.current_channel"]
                    or row["wlan_radio.channel"]
                ),
                "frequency_mhz": as_number(row["wlan_radio.frequency"]),
                "beacon_interval_tu": interval,
                "beacon_interval_ms": round(interval * 1.024, 4) if interval is not None else None,
                "sample_phy_code": as_number(row["wlan_radio.phy"]),
                "sample_data_rate_mbps": as_number(row["wlan_radio.data_rate"]),
                "max_supported_rate_mbps": max_legacy_rate(row["wlan.supported_rates"]),
                "max_extended_supported_rate_mbps": max_legacy_rate(
                    row["wlan.extended_supported_rates"]
                ),
            }
        networks[key]["beacon_count"] += 1
    return {"capture": str(capture), "mode": "beacons", "networks": list(networks.values())}


def ip_destination_summary(capture: Path, destination: str):
    fields = ("ip.src", "eth.src")
    ethernet_sources = Counter()
    ip_sources = defaultdict(Counter)
    packet_count = 0
    for row in capture_rows(capture, f"ip.dst == {destination}", fields):
        ip_source = row["ip.src"] or None
        mac_source = row["eth.src"] or None
        packet_count += 1
        ethernet_sources[mac_source] += 1
        ip_sources[ip_source][mac_source] += 1

    return {
        "capture": str(capture),
        "mode": "ip-dest",
        "destination_ip": destination,
        "packet_count": packet_count,
        "ethernet_sources": [
            {"mac": mac, "packets": count}
            for mac, count in sorted(ethernet_sources.items(), key=lambda item: str(item[0]))
        ],
        "ip_sources": [
            {
                "ip": ip,
                "ethernet_sources": [
                    {"mac": mac, "packets": count}
                    for mac, count in sorted(macs.items(), key=lambda item: str(item[0]))
                ],
            }
            for ip, macs in sorted(ip_sources.items(), key=lambda item: str(item[0]))
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="mode", required=True)
    beacons = subcommands.add_parser("beacons", help="summarize 802.11 Beacon frames")
    beacons.add_argument("capture", type=Path)
    beacons.add_argument("--ssid", help="include only this decoded SSID")
    ip_dest = subcommands.add_parser("ip-dest", help="compare IP and Ethernet sources")
    ip_dest.add_argument("capture", type=Path)
    ip_dest.add_argument("destination", help="IPv4 destination address")
    args = parser.parse_args()

    if not args.capture.is_file():
        parser.error(f"capture file does not exist: {args.capture}")
    if shutil.which("tshark") is None:
        parser.error("tshark is required and was not found on PATH")

    try:
        if args.mode == "beacons":
            result = beacon_summary(args.capture, args.ssid)
        else:
            destination = str(ipaddress.IPv4Address(args.destination))
            result = ip_destination_summary(args.capture, destination)
    except (RuntimeError, ValueError) as exc:
        parser.error(str(exc))

    json.dump(result, sys.stdout, indent=2)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
