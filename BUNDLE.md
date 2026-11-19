# Bundle manifest (Rule-11 property 7)

The whole distribution this repo authors, at pinned versions: one row per craft in the tree — the
core craft (`dyad-operator`) plus every Tended craft. Checked both directions by
`dyad/guards/infra/bundle.py`: every row's version equal to that craft's live `VERSION`, every craft
in the tree has a row and every row names a craft in the tree. Built by `dyad bundle build [dir]`
(the one distribution code path, `dyad build` / `dyad craft export` per row — no second mechanism),
released as the unprefixed tag `vMAJOR.MINOR.PATCH` = `v` + the version below. A system that wants
only some components pins them individually by their own crafts' tags (`dyad-operator-vX.Y.Z`,
`<craft>-vX.Y.Z`) instead of this file.

## Release notes (1.6.0)

This repository starts fresh at 1.6.0 as the reference, a successor snapshot of `dyad-system`. Row numbers
(`#747`) below and in earlier notes refer to that system's ledger, where each change was decided.


- **Incidents upstream (#747).** When an incident's fix lies in a craft the system installed unmodified (its registry
  sha256 matches its tree), Rule-3 Incidents has the agent record it in `INCIDENTS.md` and draft an `issue` post on the
  channels repository (`crafts/channels/playbooks/channel-post.md`). Each post is asked as its own posting question
  and is never carried by a plan. A system with no channels membership hands the drafted post to the operator, who may
  have a member system they attend post it under that system's own question, and first boot's greeting says so.
  `channels` is now bundled with the core, so every install carries it.
- **Fixes from #747's install test.**
  - **A:** `land` works with no `origin` remote. It fast-forwards the local `main` and fetches and pushes nothing.
  - **B:** `dwork state -d` refuses an entry that opens with a date, which the verb writes itself.
  - **C:** first boot gives an unborn `main` an empty root commit, which the fence admits, and the home's launcher
    sets `DYAD_SESSION`.
  - **D:** the test clones copy objects, never hard-link them.
  - **E:** the bundled-craft test no longer rewrites a live guard while other tests run.
- **The home's nickname (#748).** `dmc:cos-nickname` recommends a nickname for the home and never sets one. The template
  gains `chief-of-staff-nickname`, `agent-signature` and `operator-signature`, each shipped `none`; the agent signs as
  itself, never as the operator.
- **Calendar access (#749).** `dmc:calendar-access-direction` says how much of each calendar a home may read; a
  client-confidential calendar is read as busy times only. Bindings are read from git config, which also keeps every
  calendar id. `dyad attention bindings` and `dyad attention overlaps --busy-file` read the bindings and the daily
  overlap, storing nothing. A new authority preference, `calendar-mandate` (template `off`), lets the home write events
  with no attendees on the one `write` binding, each reported with its undo.
- **The attention brief (#750).** `dyad attention brief` (read-only) prints the brief's mechanical half:
  - the waiting questions, by unit;
  - blocked and done-ready rows;
  - owned PRs whose head no longer merges;
  - unread inbox items;
  - the next attention window.
  Attention play-book A8 states the 15-minute cadence and the untracked `<git common dir>/dyad-brief.md`, and keeps
  work-calendar content in the session and that file.
- **channels 0.2.0 (#752), the craft's first release.**
  - A message may carry attachments: `attachments:` names each file by sha256 and size, and the files sit in `<id>/`
    beside the message, append-only like it.
  - A channel entry gains `visibility` and `attachment-limit`.
  - The guard checks every attachment and runs the fence on text. It admits binaries and personal data only on a
    private channel, and fails a `private` entry that the hosting calls public.
  - `post --attach` stages and checks before it writes.

## Release notes (1.5.0)

- **First boot (#728).** The core Release's `install.sh` hands the new system its seed prompt. The first session follows
  `dyad/playbooks/first-boot.md`, and `--attention-clone` names the operator's central repository at install.
- **The quoted answer (#737).** An answer may open with `>` lines quoting the question it answers. The quote binds the
  answer to that question and is not read as text or as a prompt. A quote that matches no outstanding question binds
  nothing, and the recording verbs warn. The new key `answer-quoting` (template `off`) controls whether the home
  invites the quoted form.
- **Repeated answers (#739).** `dyad dwork state --after-entry <n>` records an answer only once. On a re-run, an
  answer whose words already stand after entry `n` is reported as already landed.
- **The attention calendar (#740).** `dmc:attention-calendar` presents ready questions against the operator's attention
  windows, which are times only and kept in a private store. It adds two verbs, `dyad attention windows --set-file`
  and `dyad attention calendar`. An owed question is never held. A held question counts as `deferred` in Coming,
  together with the next window's start. Calendar ids are refused in provenance and on the board. It adds three new
  keys:
  - `work-owner` (template `none`) names whose calendar binding is read.
  - `calendar-question-minutes` and `calendar-window-min` are tunables.
- **Fixes (#738, #742, #744):**
  - The runner's evidence note names the failing tests.
  - Corroboration's scratch install unsets the hooks path that `install` sets, so its one commit passes.
  - The automaton tests no longer inherit the runner's `AUTOMATON_EVIDENCE_SANDBOX`.

## Release notes (1.4.0)

- **Attention ledger (#700, #703).** One store, per operator, of what waits on the operator across units and systems:
  `dyad attention sync` replays this system's board and rows into it as references, and the closing line counts its
  open set; the `paired` kind and its drift check read each system's `paired-units`.
- **Attention strategy and mandate (#705, #707).** The operator's goals and today's focus order what reaches the
  operator (`dmc:attention-strategy`); attention rows open under `attention-mandate`, their Dones asked at the weekly
  review.
- **Next-best disposition and the question page (#706, #709).** Which questions are presented, alone, batched or
  deferred, gated on their predecessors, in the operator's weighted order; under `question-page: on` the home
  publishes the outstanding questions as one private page.
- **Recommended for next (#695).** A third part of the closing line: what a trigger says is due and nobody has asked.
- **Hardening mandate (#692).** Under `hardening-mandate: on` a due backlog row of hardening work opens with no intent
  or plan question, its Done always asked.
- **Stale work retired (#697).** The grooming reads the oldest rows for staleness; stale open or planned work can be
  retired in the grooming's question (`dyad dwork retire`).
- **Decision records (#689, #690, #691, #694, #698).** When a row needs its own plan question, the judgement trace,
  the audit trigger, re-presenting a question, and take-over or wait.
- **A curl-retrievable installer (#721).** The core Release carries `install.sh`, stamped with its tag and this
  repository: it asks for the directory and whether to clone or reuse, checks the archive against its sha256, installs
  and launches `claude`. Its sha256 for `dyad-operator-v1.4.0` is
  `47f4a612b7acbbbd7f9ad63a7d0918b690abf4bea96a6adbb0e84c9ab826d64b`, also printed in the Release's notes.
- **Fixes (#652, #658, #704, #715).** A unit is rung only after its post lands; live tests are out of the code gate;
  `read_rows` reads a commit with no d-work store as no rows, so a fresh system's plan gate no longer crashes (#715).
- **syseng 0.8.1 (#714).** The closed uppercase list names `*-README.md`, so a fresh install passes its own naming
  guard on the core's README seeds.
- **cabinet 0.8.0 (#682, #689, #698, #700, #703, #705, #706).** The Operating Guide's sections for the attention
  ledger, the strategy, the next-best disposition and take-over or wait.
- **chronicle 0.5.0 (#678, #683–#685, #693, #696, #699).** Problem discovery's why-tree and its records, a segmentation
  record, a phased target-segment review and a canonical list of user symptoms; a quote in a paragraph keyed fiction is read
  as dialogue, not as a claim of verbatim record (#731).
- **sysarch 0.4.2 (#682, #723).** Lists the channels post guard and the specs craft's specification guard
  (maintenance; cut so the bundle's row has its tag).

## Known limitations (1.4.0)

- Between a release's cut and its tag, a push that changes code, and `dyad check --evidence`, are refused for the
  missing core tag. Both pass once the publishing run, after the operator's approval, has made the tag.
- The automaton's board flip after a recorded plan answer can overwrite a newer board entry. Rewrite the entry with
  `dyad board set` after the flip.
- The stores sweep can tell a standing warning as new when it carries a count that grows with the ledger. It costs
  one extra notice; nothing fails.
- The sweep's mirror check does not run: `dyad-sweep.yml` sets no `MIRROR`.
- The GitHub Release's text is a fixed one-line template. These notes are in `BUNDLE.md`.
- Under `intent-reading: on`, the intent reading's plan file needs a `Base commit:` line before it is pushed. The
  plans guard refuses a plan file without one.
- The `released` health reads each Release from the hosting without a token, and can report "not read" under the
  hosting's rate limit.
- `dyad precedent prompt` sends no record whose outcomes are an operator's acts, so such records gain no precedents.
  `agreement` measures sets under 20 cases at max_df 0.5, and no record yet carries a bar, so none converts.
- An instance whose preference table predates 1.2.0 gets a warning that `awaiting-you` has no row, until its table
  is next edited. Its absent key reads `on` either way.

## Deprecated (1.4.0)

Five question forms are deprecated by #708. Each keeps working through 1.4.x and is removed in 2.0.0. At removal,
only three questions remain, intent, plan and Done, and each of these forms becomes a clause of one of them. The
upgrade step ships with 2.0.0 (`dyad/playbooks/port.md`).

- **`merge-disposition: separate`.** In 2.0.0 the value reads as `with-done`: a PR's merge is the `merges` clause of
  its d-work's Done, never a question of its own.
- **The chat release question and its batch form** (`release <tag>?`, `release <tag-a>, <tag-b>?`). In 2.0.0 a release
  is the `releases` clause of its release d-work's Done, under the release gate (`RELEASE_APPROVAL=tap`). With the gate
  off, the release is refused, and the operator can still cut it by hand.
- **A destructive host action's own question** (`run <action>?`). In 2.0.0 the action is the plan's `runs` clause,
  behind the pre-state fence (`dyad host pre-state`, `dyad host run --plan`): the command runs only on the target state
  the plan recorded. A target the fence cannot read is delivered as an ops script.
- **The precedent question** (`admit as precedents <cases>?`). In 2.0.0 cases are admitted by the `admits` clause of
  the grooming Done.
- **The retirement form** (`archive #a, #b?`). In 2.0.0 rows are retired by the `retires` clause of a Done, the
  grooming Done for rows no delivered row's report covers.

An installing system that sets `merge-disposition: separate`, or whose own text asks any of these forms, should plan its
move during 1.4.x.

version: 1.6.0

| component | version |
|-----------|---------|
| dyad-operator | 1.6.0 |
| sysarch | 0.4.2 |
| syseng | 0.8.1 |
| sysadmin | 0.3.3 |
| cabinet | 0.9.0 |
| channels | 0.2.0 |

`disclosure` is in the tree and deliberately absent from the table: the Operator disposed that it is
not meant for release yet and is held until ready (d-work #232). Rule-11 property 7 permits an
unreleased craft to have no row, and `dyad bundle build` builds once per row, so nothing here publishes
it. The `not yet bundled` warning the guard prints for it describes that decision, not an unfinished
chore. Its first release adds its row.
