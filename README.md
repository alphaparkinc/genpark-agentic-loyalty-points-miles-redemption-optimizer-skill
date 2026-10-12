# genpark-agentic-loyalty-points-miles-redemption-optimizer-skill

[![GenPark AI](https://img.shields.io/badge/GenPark_AI-www.genpark.ai-blue.svg)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark_Company_92955550-0077B5.svg)](https://www.linkedin.com/company/92955550)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Dependencies](https://img.shields.io/badge/dependencies-0%20(Pure%20Stdlib)-brightgreen.svg)](requirements.txt)
[![MCP Compliant](https://img.shields.io/badge/MCP-JSON--RPC%202.0-purple.svg)](mcp_server.py)

Autonomous Loyalty Points & Airline Miles Redemption Arbitrage Optimizer. Evaluates Cents-Per-Point (CPP) valuations across credit card transfer partners (Chase UR, Amex MR, Citi, Bilt), airline alliances, and hotel portals (Expedia, Marriott, Hyatt), accounts for transfer bonuses and carrier fuel surcharges, and selects the Pareto-optimal payment path.

---

## 🌐 Official GenPark AI Ecosystem Links

- **GenPark Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Official Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550) ([https://www.llinkedin.com/company/92955550](https://www.llinkedin.com/company/92955550))

---

## 🌟 Key Features

- **100% Zero External Dependencies**: Runs entirely on the Python 3.9+ standard library.
- **Model Context Protocol (MCP) Standard**: Native support for JSON-RPC 2.0 `initialize`, `tools/list`, and `tools/call`.
- **Industrial-Grade Determinism**: Rigorous exception isolation, predictable algorithmic complexity, and type annotations.
- **Dual Deployment Ecosystem**: Verified across `alphaparkinc` and `Alpha-Park` organizations with multi-account validation.

---

## 🚀 Quick Start

### 1. Direct Python SDK Usage

```python
"""Example usage for AgenticLoyaltyPointsMilesRedemptionOptimizer."""
import sys
import json
from client import AgenticLoyaltyPointsMilesRedemptionOptimizer

sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("=== Agentic Travel & Commerce Loyalty Points Redemption Optimizer Demo ===")
    optimizer = AgenticLoyaltyPointsMilesRedemptionOptimizer()

    # Business Class Ticket to Tokyo: Cash Price $3,250
    candidates = [
        {
            "program": "AMEX_MR",
            "points_required": 85000,
            "taxes_fees_usd": 210.00,
            "transfer_bonus_pct": 20.0
        },
        {
            "program": "UNITED_MILEAGEPLUS",
            "points_required": 175000,
            "taxes_fees_usd": 45.00,
            "transfer_bonus_pct": 0.0
        }
    ]

    print("\n--- 1. Evaluating Cash ($3,250) vs Point Transfer Routes ---")
    decision = optimizer.optimize_redemption_route(cash_price_usd=3250.00, redemption_options=candidates)
    print(f"Recommended Action: {decision['recommended_action']}")
    print(f"Decision Rationale: {decision['decision_rationale']}")

    best = decision["optimal_route"]
    print(f"\n--- 2. Winning Route Breakdown ({best['program_name']}) ---")
    print(f"Quoted Award Points: {best['award_points_quoted']:,} pts (Transfer Bonus: +{best['transfer_bonus_pct']}%)")
    print(f"Actual Source Points Deducted: {best['source_points_deducted']:,} pts + ${best['taxes_and_surcharges_usd']:.2f} fees")
    print(f"Effective Valuation: {best['effective_cpp_cents']} cents/point (Benchmark: {best['baseline_hurdle_cpp']} CPP)")

if __name__ == "__main__":
    main()

```

### 2. Run as Model Context Protocol (MCP) Server

Start standard JSON-RPC 2.0 server over `stdio`:

```bash
python mcp_server.py
```

Execute embedded test harness:

```bash
python mcp_server.py --test
```

---

## 🛠️ MCP Tool Specification

Inspect [`skill.json`](skill.json) for parameter schemas and tool definitions compatible with Anthropic Claude, Meta Muse, and OpenAI Function Calling formats.

---

## 📜 License & Community

Licensed under the [MIT License](LICENSE). Copyright © 2026 [GenPark AI](https://www.genpark.ai).
Follow us on LinkedIn: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550) | [https://www.llinkedin.com/company/92955550](https://www.llinkedin.com/company/92955550)
