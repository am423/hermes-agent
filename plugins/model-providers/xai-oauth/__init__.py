"""xAI (Grok) OAuth Provider for Hermes Agent.

This provider adds first-class support for xAI's Grok models using OAuth
authentication against auth.x.ai.

Primary authentication method:
    Automatic import from the official Grok CLI / Grok Build login
    (~/.grok/auth.json). This provides the best experience for users who
    already use the official Grok tools.

Fallback:
    Full browser-based PKCE OAuth login flow.

Technical details:
    - Uses `chat_completions` (the only surface that works with Grok-CLI OAuth tokens).
    - The richer `codex_responses` path is available only to users with a real
      XAI_API_KEY (they should use the built-in "xai" provider or set
      model.api_mode: codex_responses explicitly).
    - Benefits from xAI's built-in prompt caching via the `x-grok-conv-id` header
      (automatically handled by the transport layer for both modes).
"""

from providers import register_provider
from providers.base import ProviderProfile


class XaiOAuthProfile(ProviderProfile):
    """xAI Grok via OAuth.

    Prefers credentials imported from the official Grok CLI.
    Falls back to browser OAuth login when needed.
    """

    # Note: xAI prompt caching (x-grok-conv-id) is handled automatically
    # in the transport layer when the base URL contains "x.ai".
    # No custom prepare_messages or build_extra_body hooks are required
    # at this time.


xai_oauth = XaiOAuthProfile(
    name="xai-oauth",
    aliases=(
        "xai-oauth",
        "grok-oauth",
        "xai-portal",
        "grok-login",
        "grok-oauth-login",
        "xai-browser",
    ),
    display_name="xAI (Grok) OAuth",
    description="xAI Grok via OAuth — auto-imports from official Grok CLI login (~/.grok/auth.json)",
    # chat_completions is the only surface reliably available to tokens imported
    # from the official Grok CLI / grok.com OAuth login. The Responses API
    # (/v1/responses) produces the "response.created before `error`" failure.
    # Users with a real XAI_API_KEY should use the built-in "xai" provider instead.
    api_mode="chat_completions",
    env_vars=("XAI_API_KEY",),
    base_url="https://api.x.ai/v1",
    auth_type="oauth_external",
    signup_url="https://grok.com",
    # Curated fallback list for when the live /models catalog is unavailable
    # (common with OAuth tokens). Kept in rough order of preference.
    fallback_models=(
        "grok-4.3",
        "grok-4.20",
        "grok-4",
        "grok-3",
        "grok-3-mini",
    ),
    default_aux_model="grok-3-mini",
    default_max_tokens=32768,
)

register_provider(xai_oauth)
