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
