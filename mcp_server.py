"""MCP Server for Agentic Loyalty Points & Miles Redemption Optimizer."""
import sys
import json
import time
from client import AgenticLoyaltyPointsMilesRedemptionOptimizer

optimizer = AgenticLoyaltyPointsMilesRedemptionOptimizer()

def handle_call_tool(params):
    name = params.get("name")
    args = params.get("arguments", {})
    if name != "optimize_loyalty_redemption":
        raise ValueError(f"Unknown tool: {name}")

    action = args.get("action", "optimize_redemption_route")
    cash = float(args.get("cash_price_usd", 1000.0))

    if action == "calculate_cpp_valuation":
        opts = args.get("redemption_options", [{}])
        first = opts[0] if opts else {}
        return optimizer.calculate_cpp_valuation(
            cash_price_usd=cash,
            points_required=int(first.get("points_required", 50000)),
            taxes_fees_usd=float(first.get("taxes_fees_usd", 25.0)),
            transfer_bonus_pct=float(first.get("transfer_bonus_pct", 0.0)),
            program_name=first.get("program", "CHASE_UR")
        )
    elif action == "optimize_redemption_route":
        return optimizer.optimize_redemption_route(cash, args.get("redemption_options", []))
    else:
        raise ValueError(f"Invalid action: {action}")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("Running self-test...")
        options = [
            {"program": "CHASE_UR", "points_required": 60000, "taxes_fees_usd": 50.0, "transfer_bonus_pct": 25.0},
            {"program": "MARRIOTT_BONVOY", "points_required": 220000, "taxes_fees_usd": 120.0, "transfer_bonus_pct": 0.0}
        ]
        res = optimizer.optimize_redemption_route(1490.0, options)
        assert res["optimal_route"]["program_name"] == "CHASE_UR"
        assert res["optimal_route"]["effective_cpp_cents"] == 3.0
        assert res["optimal_route"]["beats_valuation_hurdle"] is True
        print("Self-test PASSED!")
        sys.exit(0)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            msg_id = req.get("id")
            method = req.get("method")
            if method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "serverInfo": {"name": "AgenticLoyaltyPointsMilesRedemptionOptimizer", "version": "1.0.0"},
                        "capabilities": {"tools": {}}
                    }
                }
            elif method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [{
                            "name": "optimize_loyalty_redemption",
                            "description": "Calculate Cents-Per-Point (CPP) valuation, evaluate transfer partner bonuses, and select optimal cash vs points redemption path.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "action": {"type": "string", "enum": ["calculate_cpp_valuation", "optimize_redemption_route"]},
                                    "cash_price_usd": {"type": "number"},
                                    "redemption_options": {"type": "array"}
                                },
                                "required": ["action"]
                            }
                        }]
                    }
                }
            elif method == "tools/call":
                res = handle_call_tool(req.get("params", {}))
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
                }
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {}}
            print(json.dumps(resp), flush=True)
        except Exception as e:
            err_resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            print(json.dumps(err_resp), flush=True)

if __name__ == "__main__":
    main()
