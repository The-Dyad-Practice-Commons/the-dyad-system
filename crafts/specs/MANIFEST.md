# specs craft manifest (Rule-11 property 2: `requires:`)

`key: value` lines (`dyadlib.parse_kv`), read by the craft guard (`dyad/guards/craft/crafts.py`) and by
`dyad craft install`. `requires:` names the minimum version of another craft this one depends on; `dyad craft
install` refuses an unmet requirement.

`dyad-operator>=1.3.0`: the core whose `dyadlib` reads the row store and its `disposed` entries, which the guard uses to
resolve a row citation and to read a `Y done` behind `status: accepted`, rather than restating either. The craft cites
sysarch's rules in prose and imports nothing from it, so it requires the core only.

No `seeds:`. The template is copied by the writer of a specification, never by an install.

name: specs
requires: dyad-operator>=1.3.0
