# grammar

## Summary

A command-line spelling/grammar/punctuation checker, like the basic
"correctness" layer of Grammarly: it flags objective errors only, never style
opinions (no passive-voice, wordiness, tone, Oxford-comma, or US/UK spelling
nags).

- `.factory/agents/grammar.md`: the factory standalone agent (prompt + `report_error` tool).
- `tools/gate.py`: the gate; rejects reports whose context/suggestion can't be applied.
- `bin/grammar`: the CLI (symlinked to `~/.local/bin/grammar`). Splits long input
  at blank lines (never inside code fences), runs chunks in parallel, maps each
  report back to `file:line:col`.
- `test/sample.md`: a fixture with 12 real errors and a set of style traps.

## Usage

    grammar notes.md              # report errors (exit 1 if any)
    pbpaste | grammar             # stdin
    grammar -s "their it is"      # a string
    grammar --fix notes.md        # print corrected text
    grammar -w notes.md           # fix in place
    grammar --json notes.md       # machine-readable
    grammar -t notes.md           # deepseek-v4-pro: slower, catches more

Default model is `chatgpt/gpt-6-luna`: factory's builtin harness calling
ChatGPT's Codex endpoint with the ChatGPT login in `~/.codex/auth.json` (your
subscription, no API key), at the model's default effort (medium). On
`test/sample.md`: ~22-27s, 6-28k input tokens, 10-12 of 12 errors, and every run
covered the whole file. `-t` uses `deepseek/deepseek-v4-pro` (~2.5 min, 12/12).
Avoid `--harness codex` for this agent: Codex's own prompt and code mode cost
43-209k tokens per run and sometimes stopped partway.

## The app (`app/`)

A minimal native macOS window around the CLI, written in Coil (AppKit via the
Objective-C runtime). Type or paste text and press ⌘↩: errors are underlined in
red with the correction written in green directly under each one. Click a
correction to apply it (undoable), or Fix All (⇧⌘↩, one undo step). The status
bar shows the explanation for the error under the caret; right-click an error
for its correction too. Edits while results are showing keep the remaining
corrections in place.

    cd app && coil build          # build/release/grammar-app (symlinked to ~/.local/bin/grammar-app)
    grammar-app &                 # run it from a terminal: it runs `grammar` from PATH

- `src/objc.coil`: Objective-C runtime bridge (`msg` macro, NSString helpers).
- `src/check.coil`: runs `grammar --json FILE` on a worker thread, decodes it with
  serde, maps code-point offsets to NSString UTF-16 offsets.
- `src/ui.coil`: window, text view delegate, correction labels, menus.
- `tools/snapshot.coil`: dev tool that drives the real window through a check,
  a caret move, a resize, and fixes, writing PNGs of each step:
  `coil build tools/snapshot.coil && build/release/snapshot DIR`.
