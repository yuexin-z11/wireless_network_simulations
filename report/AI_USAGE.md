# AI usage summary

Maintain this log throughout the project and append the completed summary to the
final report. Keep the three headings below. Replace drafting notes with an
accurate account of the group's actual usage and verification.

## Prompts used

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

## Ideas the AI provided correctly with minimal guidance

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
