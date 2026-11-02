# Imou Core — November 2026 Plan

Date: 2026-11-02  
Status: Approved for planning  
Scope: Home Assistant core `imou` integration (Gold today)

## Goal

This month:

1. **Quality:** Move the core Imou integration from Gold toward Platinum.
2. **Product:** Land the already-open PRs plus one new user-facing feature (smart-plug `number` entities).

Priority when they conflict: Platinum ladder first; open PRs and `number` continue in parallel where they do not block.

## Current state

- Core `imou` is **Gold** (`quality_scale: gold` on `dev`).
- Platinum rules still `todo`: `async-dependency`, `inject-websession`, `strict-typing`.
- Pinned library: `pyimouapi==1.4.4` (async aiohttp client, optional injected session, ships `py.typed`).
- Custom Imou Life already injects `async_get_clientsession(hass)`; core does not yet.
- Core already uses typed `ImouConfigEntry` / `runtime_data`.

## Product: what to merge this month

### Keep pushing (open)

| PR | Purpose | Merge outlook |
| --- | --- | --- |
| [#189434](https://github.com/home-assistant/core/pull/189434) | Drop idle camera streams so the next open fetches a fresh RTSP URL | High — addresses short-lived tickets after 1.4.4; needs human review |
| [#189006](https://github.com/home-assistant/core/pull/189006) | Skip ability-ref fetches for known devices | Medium — joostlek requested changes; private library patch already removed; may need a follow-up library public API later, not in Platinum PRs |

### New feature this month

- **Smart-plug `number` entities** (countdown minutes, max power watts), with a paired documentation PR on `home-assistant.io` (`next`).
- Prior art: closed core [#186419](https://github.com/home-assistant/core/pull/186419) (held for docs conflict); revive from fork branch `imou-number` rather than redesigning from scratch.

### Explicitly out of scope this month

- White-light migration to `light` (defer).
- Event-push stack (webhook, motion binary sensor, doorbell `event`, alarm `image`, local record-on-alarm).
- Configurable polling interval (forbidden by quality rules; already closed).
- Daknightuk siren **button** PR (manual siren is already a `siren` entity in core).
- Stuffing library private APIs or ability-ref retry into Platinum PRs.

## Quality: Platinum gap and feasibility

| Rule | Gap | Work |
| --- | --- | --- |
| `async-dependency` | Library already async; rule still `todo` | Mark `done` when session wiring proves no blocking I/O in the dependency path |
| `inject-websession` | Library accepts session; core constructs `ImouOpenApiClient` without one | Pass `async_get_clientsession(hass)`; do not close HA’s shared session on unload; cover setup/config-flow clients; mirror Imou Life |
| `strict-typing` | Not listed in `.strict-typing` | Add `homeassistant.components.imou`; fix mypy under strict; keep `ImouConfigEntry` throughout |

**Feasibility this month: high.** The hard library prerequisites are already in 1.4.4. Remaining risk is mypy debt volume and review queue. Do **not** bump pyimouapi for Platinum unless session/typing proves 1.4.4 insufficient.

## PR ladder (best practice: one concern per PR)

### Platinum

1. **Inject websession** — code + tests; mark `async-dependency` and `inject-websession` `done`.
2. **Strict typing** — `.strict-typing` + mypy fixes; mark `strict-typing` `done`.
3. **Raise to platinum** — `manifest.json` / `quality_scale.yaml` only; paired docs badge update.

### Product (parallel, non-blocking)

4. Continue review on #189434 and #189006.
5. **Add Imou number platform** + docs PR (after or beside session PR; avoid mixing into Platinum PRs).

## Success criteria (end of November)

- Platinum PRs 1–2 merged; PR 3 opened with green CI (merge depends on maintainers).
- `number` PR opened (ideally merged) with docs companion.
- #189434 / #189006 merged if reviewers allow; failure here does not fail the Platinum goal.

## Non-goals

Shipping Platinum and `number` in a single mega-PR; redesigning event push for core this month; changing polling UX.
