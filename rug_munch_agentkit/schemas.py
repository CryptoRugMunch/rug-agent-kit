"""Input schemas for Rug Munch actions."""

from pydantic import BaseModel, Field


class CheckRiskSchema(BaseModel):
    """Schema for check_token_risk action."""
    token_address: str = Field(..., description="Token mint (Solana) or contract address (EVM)")
    chain: str = Field(default="solana", description="Blockchain: solana, ethereum, base, arbitrum, polygon")


class CheckBatchSchema(BaseModel):
    """Schema for batch risk check."""
    tokens: list[str] = Field(..., description="List of token addresses (max 20)")
    chain: str = Field(default="solana")


class DeployerCheckSchema(BaseModel):
    """Schema for deployer history check."""
    deployer_address: str = Field(..., description="Deployer wallet address")


class TokenAddressSchema(BaseModel):
    """Generic schema for single token address."""
    token_address: str = Field(..., description="Token address")


class MarcusQuickSchema(BaseModel):
    """Schema for Marcus AI quick analysis."""
    token_address: str = Field(..., description="Token address")
    chain: str = Field(default="solana")
    question: str = Field(default=None, description="Optional specific question about the token")


class WatchTokenSchema(BaseModel):
    """Schema for token watch setup."""
    token_address: str = Field(..., description="Token to monitor")
    webhook_url: str = Field(..., description="HTTPS URL to POST alerts to")
    watch_type: str = Field(default="rug_detected", description="risk_change, rug_detected, price_drop, all")
