# xAI (Grok) OAuth Provider

This provider adds first-class support for [xAI Grok](https://grok.com) models in Hermes Agent using OAuth tokens imported from the official Grok CLI or browser login.

## Features

- Uses standard OpenAI **Chat Completions** (`chat_completions`) — the only API surface reliably available to tokens imported from the official Grok CLI / grok.com OAuth login.
- The dedicated `xai` provider (with a real `XAI_API_KEY`) can use the richer Responses API (`codex_responses`) for native reasoning when desired.
- Automatically benefits from xAI's prompt caching via the `x-grok-conv-id` header (injected for any `*.x.ai` base URL when a `session_id` is active).
- **Primary authentication**: Seamless auto-import from the official Grok CLI login (`~/.grok/auth.json`).
- Optional browser-based OAuth login to `auth.x.ai` as a fallback.

## Recommended Setup

The best experience is to first log in with the official Grok CLI:

```bash
grok login
```

Then in Hermes:

```bash
hermes model
# → select "xAI (Grok) OAuth"
```

Hermes will automatically detect and import your existing Grok CLI credentials into `~/.hermes/auth.json`.

## Alternative: Browser Login

If you prefer not to use the Grok CLI, you can authenticate directly via browser when selecting the provider in `hermes model`.

> **Note**: Browser login uses xAI's public desktop OAuth client. Some environments may have redirect URI restrictions.

## Context Length Notes (Important)

The base `grok-4.3` model (what "current" usually resolves to in the Grok CLI) has a **512k** context window. Faster variants (`grok-4.3-fast`, some `grok-4.20` releases) support up to 2M.

Hermes ships with correct fallbacks for both. If you see an incorrect value, clear your cache:

```bash
rm ~/.hermes/context_length_cache.yaml
```

## Aliases

This provider accepts the following names:

- `xai-oauth`
- `grok-oauth`
- `xai-portal`
- `grok-login`
- `grok-oauth-login`
- `xai-browser`

## Model Examples

```yaml
model:
  default: grok-4.3
  provider: xai-oauth
```

Other popular choices:

- `grok-4.20`
- `grok-4`
- `grok-3-mini` (good cheap auxiliary model)

## Related Providers

| Provider | When to use |
|----------|-------------|
| `xai-oauth` (this plugin) | You use the official Grok CLI or grok.com login |
| `xai` | You have a real `XAI_API_KEY` from the xAI console and want Responses API + native reasoning |

## Environment Variables

| Variable | Purpose | Notes |
|----------|---------|-------|
| `XAI_API_KEY` | Fallback for the non-OAuth `xai` provider | Low priority for this plugin |

## Implementation Notes

- `api_mode`: `chat_completions` (hard requirement for Grok CLI OAuth tokens)
- Prompt caching header (`x-grok-conv-id`) is injected in both `chat_completions` and `codex_responses` transports for any `api.x.ai` endpoint.
- Credential import logic lives in `hermes_cli/auth.py` (`_import_grok_cli_into_hermes`).
- Runtime protection lives in `hermes_cli/runtime_provider.py` (`_effective_api_mode_for_xai` + the `xai-oauth` branch).

## Troubleshooting

**"Expected to have received `response.created` before `error`"**

You are hitting the Responses API with an OAuth token. This plugin forces `chat_completions`. If you still see the error, ensure you are using `provider: xai-oauth` (not `xai`) and that no `model.api_mode: codex_responses` override exists in your config.

**Context bar shows wrong size**

Clear the cache (see "Context Length Notes" above) and start a new session.

## Contributing

This plugin was added to give users of the official Grok tools a first-class, zero-config experience inside Hermes. Improvements to credential import, header handling, or model catalog behavior for xAI OAuth are very welcome.