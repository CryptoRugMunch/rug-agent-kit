"""
Rug Munch Intelligence Action Provider for Coinbase AgentKit.

Adds token risk intelligence to any AgentKit-powered trading agent.
Checks for rug pulls, honeypots, and scams before every trade.

Usage:
    from rug_munch_agentkit import rug_munch_action_provider

    agentkit = AgentKit(AgentKitConfig(
        wallet_provider=wallet_provider,
        action_providers=[
            rug_munch_action_provider(),
            # ... other providers
        ],
    ))
"""

import json
import os
from typing import Any

import requests

from coinbase_agentkit.action_providers.action_decorator import create_action
from coinbase_agentkit.action_providers.action_provider import ActionProvider
from coinbase_agentkit.wallet_providers import WalletProvider

from .schemas import (
    CheckRiskSchema,
    CheckBatchSchema,
    DeployerCheckSchema,
    TokenAddressSchema,
    MarcusQuickSchema,
    WatchTokenSchema,
)

API_BASE = os.environ.get("RUG_MUNCH_API_BASE", "https://cryptorugmunch.app/api/agent/v1")
API_KEY = os.environ.get("RUG_MUNCH_API_KEY", "")


def _headers() -> dict:
    h = {"Content-Type": "application/json"}
    if API_KEY:
        h["X-API-Key"] = API_KEY
    return h


def _post(path: str, data: dict, timeout: int = 30) -> str:
    """POST to Rug Munch API, return JSON string."""
    try:
        resp = requests.post(f"{API_BASE}{path}", json=data, headers=_headers(), timeout=timeout)
        if resp.status_code == 402:
            return json.dumps({
                "success": False,
                "error": "Payment required (HTTP 402). Set RUG_MUNCH_API_KEY or use x402 payment.",
                "pricing": "See https://cryptorugmunch.app/api/agent/v1/status",
            })
        resp.raise_for_status()
        return json.dumps({"success": True, **resp.json()})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})


def _get(path: str, timeout: int = 30) -> str:
    """GET from Rug Munch API, return JSON string."""
    try:
        resp = requests.get(f"{API_BASE}{path}", headers=_headers(), timeout=timeout)
        if resp.status_code == 402:
            return json.dumps({
                "success": False,
                "error": "Payment required (HTTP 402). Set RUG_MUNCH_API_KEY or use x402 payment.",
            })
        resp.raise_for_status()
        return json.dumps({"success": True, **resp.json()})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})


class RugMunchActionProvider(ActionProvider[WalletProvider]):
    """
    Rug Munch Intelligence action provider for Coinbase AgentKit.

    Adds crypto token risk intelligence: rug pull detection, honeypot checking,
    deployer history, holder analysis, and AI forensic analysis.
    """

    def __init__(self):
        super().__init__("rug_munch", [])

    @create_action(
        name="check_token_risk",
        description="""CRITICAL: Check a token's rug pull risk BEFORE buying or trading.

Returns a 0-100 risk score, honeypot detection, freeze authority check,
holder concentration, deployer history, and a SAFE/CAUTION/AVOID recommendation.

ALWAYS call this before executing any token swap or purchase.
Cost: $0.04 per check — the cheapest insurance in crypto.

Inputs:
- token_address: Token mint (Solana) or contract address (EVM)
- chain: Blockchain (solana, ethereum, base, etc.) — defaults to solana

Example output:
{
  "risk_score": 85,
  "risk_level": "critical",
  "recommendation": "AVOID",
  "honeypot_risk": true,
  "risk_factors": ["Freeze authority enabled", "Top 10 hold 94%", "Serial rugger deployer"]
}""",
        schema=CheckRiskSchema,
    )
    def check_token_risk(self, args: dict[str, Any]) -> str:
        validated = CheckRiskSchema(**args)
        return _post("/check-risk", {
            "token_address": validated.token_address,
            "chain": validated.chain,
        })

    @create_action(
        name="check_batch_risk",
        description="""Batch risk check for up to 20 tokens at once.
Use for portfolio screening or evaluating multiple tokens.
Cost: $0.30 (~$0.015 per token).

Inputs:
- tokens: List of token addresses (max 20)
- chain: Blockchain (defaults to solana)""",
        schema=CheckBatchSchema,
    )
    def check_batch_risk(self, args: dict[str, Any]) -> str:
        validated = CheckBatchSchema(**args)
        return _post("/check-batch", {
            "tokens": validated.tokens[:20],
            "chain": validated.chain,
        })

    @create_action(
        name="check_deployer_history",
        description="""Check a token deployer's full history.
Returns tokens deployed, rug count, and classification:
legitimate_builder, suspicious, or serial_rugger.
Essential for evaluating new token trustworthiness. Cost: $0.06.

Inputs:
- deployer_address: The deployer's wallet address""",
        schema=DeployerCheckSchema,
    )
    def check_deployer_history(self, args: dict[str, Any]) -> str:
        validated = DeployerCheckSchema(**args)
        return _get(f"/deployer/{validated.deployer_address}")

    @create_action(
        name="get_holder_deepdive",
        description="""Deep holder analysis for a token.
Detects: snipers, Jito bundles, fresh wallet clusters, whale concentration,
connected wallet patterns, and coordinated manipulation. Cost: $0.10.

Inputs:
- token_address: Token to analyze""",
        schema=TokenAddressSchema,
    )
    def get_holder_deepdive(self, args: dict[str, Any]) -> str:
        validated = TokenAddressSchema(**args)
        return _get(f"/holder-deepdive/{validated.token_address}")

    @create_action(
        name="get_token_intelligence",
        description="""Comprehensive token data: price, volume, market cap, holder stats,
LP lock status, authority flags, buy/sell ratios, and top holders. Cost: $0.06.

Inputs:
- token_address: Token to look up""",
        schema=TokenAddressSchema,
    )
    def get_token_intelligence(self, args: dict[str, Any]) -> str:
        validated = TokenAddressSchema(**args)
        return _get(f"/token-intel/{validated.token_address}")

    @create_action(
        name="marcus_quick_analysis",
        description="""AI forensic verdict by Marcus Aurelius (powered by Claude Sonnet 4).
One-paragraph analysis with risk score, key flags, and recommendation.
Use for quick expert opinion on borderline tokens. ~5-30s. Cost: $0.15.

Inputs:
- token_address: Token to analyze
- chain: Blockchain (defaults to solana)
- question: Optional specific question about the token""",
        schema=MarcusQuickSchema,
    )
    def marcus_quick_analysis(self, args: dict[str, Any]) -> str:
        validated = MarcusQuickSchema(**args)
        payload = {"token_address": validated.token_address, "chain": validated.chain}
        if validated.question:
            payload["question"] = validated.question
        return _post("/marcus-quick", payload, timeout=60)

    @create_action(
        name="watch_token_risk",
        description="""Set up real-time token monitoring with webhook alerts.
When risk changes, rug detected, or price drops, we POST to your webhook.
Covers 7 days of monitoring. Cost: $0.20.

Inputs:
- token_address: Token to monitor
- webhook_url: HTTPS URL to receive alerts
- watch_type: risk_change, rug_detected, price_drop, or all""",
        schema=WatchTokenSchema,
    )
    def watch_token_risk(self, args: dict[str, Any]) -> str:
        validated = WatchTokenSchema(**args)
        return _post("/watch", {
            "token_address": validated.token_address,
            "webhook_url": validated.webhook_url,
            "watch_type": validated.watch_type,
        })

    def supports_network(self, network: "Network") -> bool:
        """Rug Munch works on any network (Solana, Base, Ethereum, etc.)."""
        return True


def rug_munch_action_provider() -> RugMunchActionProvider:
    """Create a Rug Munch Intelligence action provider instance."""
    return RugMunchActionProvider()
