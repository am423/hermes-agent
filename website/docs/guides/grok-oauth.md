---
sidebar_position: 12
title: "Grok OAuth (via Grok CLI)"
description: "Use Grok-4.3 and other Grok models in Hermes Agent by importing your official Grok CLI login — no separate XAI_API_KEY required"
---

# Grok OAuth (via Grok CLI Login)

Hermes Agent supports **Grok models** through OAuth tokens imported from the official Grok CLI (`grok login`) or direct browser login to grok.com. This is the recommended path if you already use the Grok CLI or grok.com chat.

The provider is registered as `xai-oauth`.

## Overview

| Item                  | Value                                      |
|-----------------------|--------------------------------------------|
| Provider ID           | `xai-oauth`                                |
| Display name          | xAI (Grok) OAuth                           |
| Auth type             | `oauth_external` (imported from Grok CLI or browser PKCE) |
| Transport             | `chat_completions` (only surface available to Grok CLI tokens) |
| Recommended models    | `grok-4.3`, `grok-4.20`, `grok-4`          |
| Base URL              | `https://api.x.ai/v1`                      |
| Requires `XAI_API_KEY`| No (falls back only for the non-OAuth `xai` provider) |
| Prompt caching        | Yes — via `x-grok-conv-id` header          |

### Base vs Fast Variants (Context Length)

- **Base `grok-4.3`** (what "current" usually resolves to): **512k** context
- **Fast variants** (`grok-4.3-fast`, some `grok-4.20` releases): up to **2M** context

Hermes includes correct fallbacks for both. If you see the wrong size, run:

```bash
rm ~/.hermes/context_length_cache.yaml
```

and start a new session.

## Quick Start

```bash
# 1. Log in with the official Grok CLI (recommended)
grok login

# 2. In Hermes, pick the provider
hermes model
# → Select "xAI (Grok) OAuth"
# → Hermes detects your ~/.grok/auth.json and imports it

# 3. Choose a model
hermes
```

Hermes will automatically import your Grok CLI credentials into `~/.hermes/auth.json` on first use.

## Alternative: Browser Login (no Grok CLI)

If you don't want to install the Grok CLI:

1. Run `hermes model`
2. Choose **"xAI (Grok) OAuth"**
3. Complete the browser-based login flow to `auth.x.ai`

Credentials are still stored the same way.

## Recommended Configuration

```yaml
# ~/.hermes/config.yaml
model:
  default: grok-4.3
  provider: xai-oauth
  reasoning_effort: high          # works well on base grok-4.3

prompt_caching:
  enabled: true
  long_lived_prefix: true         # excellent with x-grok-conv-id
```

For auxiliary tasks (compression, vision, etc.), Hermes will intelligently fall back to cheaper models when `auxiliary.*.provider: auto`.

## How It Compares to the `xai` Provider

| Feature                        | `xai-oauth` (this guide)          | `xai` (API key)                  |
|--------------------------------|-----------------------------------|----------------------------------|
| Authentication                 | Grok CLI / grok.com OAuth         | `XAI_API_KEY`                    |
| API surface                    | `chat_completions` only           | `codex_responses` (full)         |
| Native reasoning               | Good (model-native)               | Excellent (Responses API)        |
| Prompt caching                 | Yes (`x-grok-conv-id`)            | Yes                              |
| Best for                       | Users who already use Grok CLI    | Users with paid xAI API access   |
| Context for base grok-4.3      | 512k                              | 512k (or higher on fast variants)|

If you have a real `XAI_API_KEY` and want the richest reasoning experience, use `provider: xai` instead.

## Troubleshooting

### "Expected to have received `response.created` before `error`"

**Cause**: Hermes tried to use the Responses API (`codex_responses`) with a Grok CLI OAuth token.

**Fix**: Make sure you are using `provider: xai-oauth` (not `xai`). Do **not** set `model.api_mode: codex_responses` when using the OAuth path.

### Wrong context length shown in TUI

Clear the cache:

```bash
rm ~/.hermes/context_length_cache.yaml
```

Then restart your Hermes session.

### Credentials not being imported

Make sure you ran `grok login` successfully and that `~/.grok/auth.json` exists and contains a valid token. Hermes looks for it during `hermes model`.

## Implementation Notes (for contributors)

- Runtime protection lives in `hermes_cli/runtime_provider.py` (`_effective_api_mode_for_xai` helper and the `xai-oauth` branch).
- The `x-grok-conv-id` header is injected in `agent/transports/chat_completions.py` (and the codex transport) for any base URL containing `x.ai`.
- See `plugins/model-providers/xai-oauth/` for the full plugin implementation.
- Context length fallbacks are maintained in `agent/model_metadata.py`.

## Related Documentation

- [xAI Provider Overview](../integrations/providers.md#xai-grok)
- [Prompt Caching](../user-guide/configuration.md#prompt-caching)
- [Reasoning Effort](../user-guide/configuration.md#reasoning-effort)
```

The guide is now created with a professional structure matching other guides like `minimax-oauth.md` and `google-gemini.md`.