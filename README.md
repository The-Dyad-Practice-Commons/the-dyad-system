# The Dyad System

The reference distribution of the Dyad System. A dyad pairs one human operator with one AI agent: the agent
proposes and the operator disposes, through a small set of Rules that keep the two parties distinct. This repository
holds the code every dyad system installs:

- `dyad/`: the core craft, `dyad-operator`. It holds the frame, the Agent Rules, the vocabulary, the guards, the
  play-books and the `dyad` entrypoint.
- `crafts/`: the Tended crafts. `sysarch` covers system architecture, `syseng` system engineering, `sysadmin` hosts
  and run-books, `cabinet` the organization of units, `channels` messages between systems, `specs` specifications,
  and `disclosure` redaction. `disclosure` is not yet released.
- `BUNDLE.md`: the versions this repository releases together, and the release notes.
- `.github/workflows/dyad-*.yml`: the workflows an installed system runs.

It holds no instance: no ledger, no preferences of any system, no host records. Every system keeps those in its own
repository, seeded from the templates at install.

## Install

Each release's assets include `install.sh`, stamped with its tag. Run it in a fresh directory. It checks the core
archive against its sha256, installs, and starts the first session, which follows `dyad/playbooks/first-boot.md`.
See `BUNDLE.md` for the release notes.

## How a change reaches this repository

There are three repositories and one decider.

1. **This repository** is the reference. It holds code only. `main` is protected: changes arrive by pull request,
   only the steward merges them, and releases are cut here under the release gate. Installers point here.
2. **`the-dyad-system-steward`** is a dyad system installed from this repository. Its ledger decides every change.
   Its home triages and orchestrates, its engineer unit builds the pull requests, and its automaton merges on
   recorded decisions. It is public, so anyone can read why a change was made.
3. **The channels repository** is the one intake. Any downstream system files a defect, with evidence and a
   reproduction, or an enhancement, with its operator's own words, as an `issue` post
   (`crafts/channels/playbooks/channel-post.md`), after its own operator approves. A pull request a person opens
   here is read as an intake of the same shapes, and the steward re-authors what it admits.

No message or pull request carries authority by itself. Whether a change enters is the steward operator's decision,
recorded in the steward's ledger.

## Licence

See `LICENSE`.
