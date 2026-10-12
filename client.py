"""
Agentic Loyalty Points & Miles Redemption Optimizer (Zero External Dependencies)
Computes Cents-Per-Point (CPP) net of surcharges and transfer bonuses to select optimal payment route.
Official Website: https://www.genpark.ai | LinkedIn: https://www.llinkedin.com/company/92955550
"""
import time
import math
import hashlib
import json
from typing import Dict, Any, List, Optional

BASELINE_CPP_HURDLE = {
    "AMEX_MR": 1.8,
    "CHASE_UR": 1.75,
    "BILT_REWARDS": 1.85,
    "MARRIOTT_BONVOY": 0.8,
    "UNITED_MILEAGEPLUS": 1.3,
    "HYATT_WORLD": 2.0,
    "GENERIC_POINTS": 1.25
}

class AgenticLoyaltyPointsMilesRedemptionOptimizer:
    def __init__(self):
        pass

    def calculate_cpp_valuation(
        self,
        cash_price_usd: float,
        points_required: int,
        taxes_fees_usd: float = 0.0,
        transfer_bonus_pct: float = 0.0,
        program_name: str = "GENERIC_POINTS"
    ) -> Dict[str, Any]:
        """
        Calculates effective Cents-Per-Point (CPP):
        Source Points Needed = ceil(points_required / (1 + transfer_bonus_pct / 100))
        CPP = ((cash_price_usd - taxes_fees_usd) * 100) / Source Points Needed
        """
        bonus_mult = 1.0 + (max(0.0, float(transfer_bonus_pct)) / 100.0)
        effective_source_points = max(1, math.ceil(int(points_required) / bonus_mult))
        net_cash_saved = max(0.0, float(cash_price_usd) - float(taxes_fees_usd))

        cpp = round((net_cash_saved * 100.0) / effective_source_points, 2)
        hurdle = BASELINE_CPP_HURDLE.get(program_name.upper(), 1.25)
        beats_hurdle = cpp >= hurdle

        return {
            "program_name": program_name.upper(),
            "cash_price_usd": float(cash_price_usd),
            "award_points_quoted": int(points_required),
            "transfer_bonus_pct": float(transfer_bonus_pct),
            "source_points_deducted": effective_source_points,
            "taxes_and_surcharges_usd": float(taxes_fees_usd),
            "effective_cpp_cents": cpp,
            "baseline_hurdle_cpp": hurdle,
            "beats_valuation_hurdle": beats_hurdle,
            "surplus_value_ratio": round(cpp / max(0.1, hurdle), 2)
        }

    def optimize_redemption_route(
        self,
        cash_price_usd: float,
        redemption_options: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Evaluates all candidate point portals and transfer routes against cash payment."""
        evaluated = []
        for opt in redemption_options:
            res = self.calculate_cpp_valuation(
                cash_price_usd=cash_price_usd,
                points_required=opt.get("points_required", 50000),
                taxes_fees_usd=opt.get("taxes_fees_usd", 11.20),
                transfer_bonus_pct=opt.get("transfer_bonus_pct", 0.0),
                program_name=opt.get("program", "CHASE_UR")
            )
            evaluated.append(res)

        if not evaluated:
            return {"recommended_payment_method": "PAY_CASH", "reason": "No point options provided"}

        # Rank by surplus_value_ratio and effective_cpp_cents descending
        evaluated.sort(key=lambda x: (x["beats_valuation_hurdle"], x["surplus_value_ratio"], x["effective_cpp_cents"]), reverse=True)
        best = evaluated[0]

        if best["beats_valuation_hurdle"]:
            recommendation = f"REDEEM_POINTS_VIA_{best['program_name']}"
            reason = f"Yields {best['effective_cpp_cents']} CPP (exceeds {best['baseline_hurdle_cpp']} CPP benchmark by {int((best['surplus_value_ratio']-1)*100)}%)"
        else:
            recommendation = "PAY_CASH_AND_EARN_POINTS"
            reason = f"Best point option only yields {best['effective_cpp_cents']} CPP, below {best['baseline_hurdle_cpp']} CPP hurdle"

        return {
            "cash_price_usd": cash_price_usd,
            "recommended_action": recommendation,
            "decision_rationale": reason,
            "optimal_route": best,
            "all_evaluated_routes": evaluated
        }
