# Group Git guide

Use this workflow for code, measurements, and report changes:

**Update `main` → create a branch → edit → commit → push → open a PR → review → merge.**

Coordinate who is working on each question or file before starting. Keep each PR
focused on one task, and ask a teammate to review it before merging into `main`.
Make changes on your own branch rather than pushing directly to `main`.

## 1. What the words mean

| Term | Meaning |
| --- | --- |
| Repository (repo) | The project files and their saved history. |
| Clone | Download the repository and its history to your computer. |
| Branch | A separate line of work. `main` holds the group's merged work. |
| Stage | Select the changes to include in the next commit with `git add`. |
| Commit | Save a snapshot locally with a message explaining the change. |
| Remote / `origin` | The shared GitHub repository / its usual local nickname. |
| Fetch | Download remote history without changing your working files. |
| Pull | Fetch and integrate remote changes into your current branch. |
| Push | Upload your local commits to GitHub. This does not merge them into `main`. |
| Pull request (PR) | A request on GitHub to review and merge one branch into another. |
| Merge conflict | Changes Git cannot combine automatically; a person must decide the result. |

## 2. First-time setup

Install Git if needed. Open a terminal (Git Bash on Windows works) and check:

```bash
git --version
```

Set the name and email attached to your commits, replacing these examples:

```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@gatech.edu"
```

These global settings apply to all your repositories. Omit `--global` and run
inside this repository if you want settings for this project only.

Sign in to Georgia Tech GitHub and make sure you can access the repository.
Ask the repository owner for access if you cannot view it or push a branch.
Then, from the folder where you want to keep the project:

```bash
git clone https://github.gatech.edu/yzhang3841/wireless_network_pas.git
cd wireless_network_pas
git status
```

If you already have a clone, open a terminal in that folder instead. Run all
remaining Git commands there. Follow your Git credential manager or the site's
authentication instructions if prompted; never put passwords or tokens in files.

## 3. Start a task

First check that `git status` reports a clean working tree. If there are unsaved
Git changes, commit them on their task branch or use the stash instructions below
before switching branches.

```bash
git switch main
git pull --ff-only origin main
git switch -c alex/q1-udp-echo
```

Use your own branch name, such as `sam/q2-distance-results` or
`lee/report-q3`. In the examples below, replace `alex/q1-udp-echo` with your branch.
`--ff-only` stops if updating would require merging divergent history; see the
troubleshooting section if that happens.

## 4. Edit, check, and save your work

Edit files and run the relevant simulation or check the report changes. If you
work in ns-3's separate `scratch/` directory, copy your updated assignment files
back into this repository before committing.

Review what changed, then stage only the intended files. This example assumes
you created or edited `q1.cc`; use the actual file names for your task.

```bash
git status
git diff
git add q1.cc
git diff --cached
git commit -m "Add Q1 UDP echo simulation"
git push -u origin alex/q1-udp-echo
```

`git diff` shows unstaged edits to tracked files; open new files to review their
contents too. `git diff --cached` shows what will go into the commit. A commit
saves locally; a push shares it. After the first push, use `git push` on this branch.

Keep generated captures, build files, and submission ZIPs out of commits. They
are ignored by default. Prefer editable report sources and small result tables;
coordinate edits to the final PDF because Git cannot combine PDF contents.

## 5. Open a pull request

1. Push your task branch, then open the repository on Georgia Tech GitHub.
2. Use **Compare & pull request**, or open **Pull requests → New pull request**.
3. Set the **base** to `main` and the **compare** branch to your task branch.
4. Give the PR a clear title and describe the changes, checks, and remaining issues.
5. Review the changed files for accidental files or unrelated edits.
6. Create the PR and request a teammate's review, or share its link with the group.

Example description:

```text
Changes: Add the Q1 two-node simulation and capture configuration.
Checked: Ran with ns-3.47 and verified UDP echo request/reply output.
Remaining: Packet measurements still need to be added to the report.
```

Use a draft PR if work is incomplete. To respond to review, edit files on the same
branch, commit, and push again. The existing PR updates automatically.

## 6. Review and merge a PR

As a reviewer, read the description and changed files. Check that the settings
match the assignment, results are explained, and relevant checks were run. Leave
comments for needed changes; approve when the work is ready.

Before merging:

- Get a teammate's approval and address review comments.
- Make sure any configured automated checks pass. If there are none, record your
  manual checks in the PR description.
- Resolve any merge conflicts using the next section.
- Confirm the PR targets `main` and contains only the intended changes.

Use GitHub's merge control and confirm the merge. If the repository offers several
methods, **Squash and merge** puts the PR's work into one commit on `main`;
**Merge pull request** preserves its individual commits. Follow the group's agreed
method and the repository's available options. If merging is blocked by permissions
or repository rules, ask the owner or address the displayed requirement.

After GitHub confirms the merge, you can delete the remote task branch using the
PR's delete-branch control. Everyone should update their local `main` before
starting their next task, with a clean working tree:

```bash
git switch main
git pull --ff-only origin main
```

Create a fresh branch for the next task. Merging a PR does not update anyone's
local files automatically, and it does not submit the assignment to Canvas.

## 7. Update your branch and resolve conflicts

If another PR changed `main` while you were working, bring those changes into
your task branch. Start with a clean working tree: commit or stash your edits first.

```bash
git switch alex/q1-udp-echo
git fetch origin
git merge origin/main
```

This merges the latest shared `main` into **your task branch**. It does not change
the shared `main`. If Git opens an editor for a merge message, save and close it
to finish the merge. If there are no conflicts, check the result and `git push`.

If Git reports conflicts:

1. Run `git status` to find the unmerged files.
2. Open each conflicted text file. A conflict looks like this:

   ```text
   <<<<<<< HEAD
   Your task branch's version
   =======
   The version from origin/main
   >>>>>>> origin/main
   ```

3. Edit the block into the correct final content. Keep one version or combine
   both as appropriate, and remove all three marker lines. During this merge,
   an editor's "current" usually means your task branch and "incoming" means
   `origin/main`. Read the actual changes before accepting either side.
4. Ask the author of the other change if the intended behavior is unclear.
   Resolving a conflict should preserve the group's intended work.
5. Stage each resolved file, using its actual name, then check and finish:

   ```bash
   git add q1.cc
   git diff --cached
   git status
   git commit -m "Merge main and resolve Q1 conflicts"
   ```

6. Run the affected simulation or review the resulting document, commit any
   follow-up fixes, and `git push`. The PR updates with your resolution.

For a binary conflict, such as `PA1.pdf`, there will be no text markers to edit.
Coordinate with the other author and regenerate a PDF containing both sets of
changes from the report sources, or agree which final file to use. Put the resolved
file in place, stage it, and complete the merge as above.

**To cancel an unfinished merge:**

```bash
git merge --abort
```

This returns to the pre-merge state when you started with a clean working tree.
Copy out any conflict-resolution edits you want to keep before aborting.

## 8. Common problems and recovery

### I need to switch branches but have unfinished edits

Save them temporarily, including new untracked files:

```bash
git stash push -u -m "Unfinished task work"
```

Switch branches or update as needed. Return to the branch where the work belongs,
then restore it:

```bash
git stash pop
git status
```

Stashing is local and does not back up work to GitHub. Ignored files are not
included. If restoring causes conflicts, resolve and stage the files as above,
then commit when ready. Git keeps the stash when `pop` conflicts; do not apply it
again blindly. `git stash list` shows saved stashes.

### I accidentally started editing or committing on local `main`

If you have **not pushed** those commits, create a task branch right where you are:

```bash
git switch -c alex/recover-work
```

Your edits and existing commits stay with you. Commit any remaining changes,
push this branch, and open a PR. If local `main` has accidental commits, ask a
teammate to help realign it after your work is safely on the remote task branch.
Do not force-push `main` to fix this. If you already pushed to shared `main`, tell
the group so you can agree on the correction.

### My push was rejected as non-fast-forward

Someone may have pushed to the same branch. With a clean working tree and your
task branch checked out, integrate their work:

```bash
git fetch origin
git merge origin/alex/q1-udp-echo
```

Resolve conflicts if needed, check the result, then `git push`. Replace the branch
name with yours. Do not force-push over a teammate's changes. Authentication or
permission errors instead require checking your account and repository access.

### `git pull --ff-only origin main` failed on local `main`

Local and remote history may have diverged. Stop and inspect:

```bash
git status
git log --oneline --graph --decorate -15
```

If you committed on local `main`, preserve the commits with a task branch using
the recovery steps above. Ask a teammate for help before resetting or rewriting
history; share the error and these command outputs without credentials.

### I staged the wrong file

```bash
git restore --staged q1.cc
```

Replace the file name as needed. This removes it from the next commit while
keeping your edits on disk.

### I need to undo a change already merged into `main`

Coordinate with the group, update `main`, create a new branch, and make a corrective
commit and PR. To reverse a whole ordinary commit, `git revert COMMIT_ID` creates
a new undo commit; replace `COMMIT_ID` with the actual hash from `git log`. Reverting
a merge commit needs extra care, so get help before doing that. Avoid `git reset
--hard` or force-pushing as beginner recovery steps: they can discard work.

## Quick checklist for every task

- [ ] Agree on the task and files with the group.
- [ ] Update `main` and create a task branch.
- [ ] Check the changes, commit intended files, and push.
- [ ] Open a PR to `main` and describe how you checked the work.
- [ ] Address review comments and resolve conflicts.
- [ ] Merge after review, then update local `main`.
