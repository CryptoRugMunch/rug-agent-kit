# Rug Munch Intelligence — AgentKit Plugin 🛡️

**Add rug pull detection to any [Coinbase AgentKit](https://github.com/coinbase/agentkit) trading agent.**

> Your agent checks every token for scams before trading. Costs $0.04 per check.

## Install

```bash
pip install coinbase-agentkit rug-munch-agentkit
```

Or from source:

```bash
git clone https://github.com/CryptoRugMunch/rug-agent-kit.git
cd rug-agent-kit
pip install -e .
```

## Quick Start

```python
from coinbase_agentkit import (
    AgentKit, AgentKitConfig,
    CdpEvmWalletProvider, CdpEvmWalletProviderConfig,
    wallet_action_provider, erc20_action_provider,
)
from rug_munch_agentkit import rug_munch_action_provider

# Set up wallet
wallet_provider = CdpEvmWalletProvider(CdpEvmWalletProviderConfig(
    api_key_id="YOUR_CDP_KEY_ID",
    api_key_secret="YOUR_CDP_KEY_SECRET",
    wallet_secret="YOUR_WALLET_SECRET",
    network_id="base-mainnet",
))

# Create agent with Rug Munch risk intelligence
agentkit = AgentKit(AgentKitConfig(
    wallet_provider=wallet_provider,
    action_providers=[
        rug_munch_action_provider(),   # ← Risk checks before trades
        wallet_action_provider(),
        erc20_action_provider(),
    ],
))

# Use with LangChain
from coinbase_agentkit_langchain import get_langchain_tools
tools = get_langchain_tools(agentkit)

# Or use directly
result = agentkit.run_action("check_token_risk", {
    "token_address": "7GCihgDB8fe6KNjn2MYtkzZcRjQy3t9GHdC8uHYmW2hr",
    "chain": "solana",
})
```

## Available Actions

| Action | Cost | Description |
|--------|------|-------------|
| `check_token_risk` | $0.04 | Risk score, honeypot detection, SAFE/CAUTION/AVOID |
| `check_batch_risk` | $0.30 | Batch scan up to 20 tokens |
| `check_deployer_history` | $0.06 | Deployer rug count, classification |
| `get_holder_deepdive` | $0.10 | Sniper detection, whale tracking |
| `get_token_intelligence` | $0.06 | Price, volume, LP lock, holder stats |
| `marcus_quick_analysis` | $0.15 | AI forensic verdict (Claude Sonnet 4) |
| `watch_token_risk` | $0.20 | 7-day webhook monitoring |

## How It Works

```
Your LLM Agent
    ↓ "Should I buy token X?"
AgentKit calls check_token_risk
    ↓
Rug Munch API returns:
    risk_score: 85, recommendation: "AVOID"
    ↓
Agent: "This token has freeze authority and the deployer
        rugged 3 previous tokens. Skipping."
```

The agent automatically uses `check_token_risk` before executing trades when the LLM determines a risk check is appropriate. The action descriptions are designed so LLMs naturally invoke them in trading contexts.

## Configuration

```bash
# Required: API key for authenticated access (or use x402 auto-payment)
export RUG_MUNCH_API_KEY="your-api-key"

# Optional: Override API URL
export RUG_MUNCH_API_BASE="https://cryptorugmunch.app/api/agent/v1"
```

### x402 Payment (No API Key Needed)

If you don't have an API key, the API uses [x402 protocol](https://x402.org) — your agent pays per-request with USDC on Base or Solana. Just ensure your agent's wallet has USDC.

## With LangChain

```python
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

llm = ChatOpenAI(model="gpt-4o")
tools = get_langchain_tools(agentkit)

agent = create_react_agent(llm, tools)

# The agent will automatically check risk before trading
response = agent.invoke({
    "messages": [{"role": "user", "content":
        "Check if token 7GCihgDB8fe6KNjn2MYtkzZcRjQy3t9GHdC8uHYmW2hr is safe to buy"
    }]
})
```

## Links

- [Rug Munch Intelligence](https://cryptorugmunch.app)
- [API Status & Pricing](https://cryptorugmunch.app/api/agent/v1/status)
- [x402 Trading Agent Example](https://github.com/CryptoRugMunch/x402-trading-agent)
- [Coinbase AgentKit](https://github.com/coinbase/agentkit)
- [x402 Protocol](https://x402.org)

## License

MIT
