# Experiment records

Add one row per run to [experiments.csv](experiments.csv). It starts with column
headers only; there are no measured results yet. Use a unique run ID such as
`q2-distance-01` and use that ID in related table, figure, and note filenames.

For each run, record:

- Question and run ID.
- Commit containing the source used (`git rev-parse HEAD`); document any uncommitted
  source changes explicitly, or commit the source before running.
- ns-3 version and exact command, including any random seed/run settings used.
- AP/STA positions or link parameters, traffic settings, aggregation, and RTS settings.
- Configured duration and actual interval used to calculate the measurement.
- Metric, value, and units; identify whether throughput is per-station or total.
- Local capture filename and the observations supporting the report answer.

Use separate Markdown notes or CSV tables for multiple measurements from one run;
link their paths in the `notes` field. Quote CSV fields containing commas. Leave
unavailable values blank and explain why in the notes; do not use zero for missing data.

Keep packet captures and full logs locally, since they are ignored. Include the
small tables and figures needed to review conclusions in this repository. If a
teammate needs a capture, agree on a shared storage location and record where to
find it without including credentials.

## Run note template

Copy this into a new file such as `results/q2-distance-01.md`:

```markdown
# Run ID

- Question:
- Date / author:
- Source commit:
- ns-3 version:
- Exact command:
- Source changes or configuration:
- Topology / node positions:
- Traffic and PHY settings:
- Aggregation / RTS settings:
- Random seed / run settings:
- Configured duration:
- Measurement interval:
- Local capture / log filenames:

## Measurements

Include units, calculation method, and per-station or total labels.

## Observations

Explain what the output or capture shows and which report answer it supports.

## Reproduction notes / limitations

Record anything another teammate needs to repeat or interpret the run.
```
