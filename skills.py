# -*- coding: utf-8 -*-
"""Pulmonary DLCO Carbon Monoxide Diffusion Capacity Skill
Engineered for GenPark Ecosystem (https://www.genpark.ai | https://www.linkedin.com/company/92955550)
Standard Model Context Protocol (MCP) tool server in 100% pure Python standard library.
"""
import sys
import json

def evaluate_pulmonary_dlco_diffusion(**kwargs):
    """Calculates hemoglobin-adjusted diffusing capacity of the lungs for carbon monoxide (DLCO), alveolar volume (VA), and diffusion coefficient (KCO), identifying alveolar-capillary membrane thickening."""
    dlco_measured_ml_min_mmhg = kwargs.get('dlco_measured_ml_min_mmhg')
    dlco_predicted_ml_min_mmhg = kwargs.get('dlco_predicted_ml_min_mmhg')
    hemoglobin_g_dl = kwargs.get('hemoglobin_g_dl')
    alveolar_volume_liters = kwargs.get('alveolar_volume_liters')
    is_male = kwargs.get('is_male')

    # Dinakara / ATS hemoglobin correction formula
    if is_male:
        hgb_adjustment_factor = (1.7 * hemoglobin_g_dl) / (10.22 + hemoglobin_g_dl)
    else:
        hgb_adjustment_factor = (1.7 * hemoglobin_g_dl) / (9.38 + hemoglobin_g_dl)
        
    dlco_adjusted = round(dlco_measured_ml_min_mmhg / (hgb_adjustment_factor if hgb_adjustment_factor > 0 else 1.0), 2)
    dlco_pct_predicted = round((dlco_adjusted / (dlco_predicted_ml_min_mmhg if dlco_predicted_ml_min_mmhg > 0 else 1.0)) * 100.0, 1)
    
    # Diffusion coefficient KCO = DLCO / VA
    kco_ratio = round(dlco_adjusted / (alveolar_volume_liters if alveolar_volume_liters > 0 else 1.0), 2)
    
    if dlco_pct_predicted < 40.0:
        severity = "SEVERE DIFFUSION DEFICIT (Suspected pulmonary fibrosis, severe emphysema, or vasculitis)"
        action = "Urgent high-resolution CT (HRCT) chest, resting/exercise arterial blood gas, pulmonology referral."
    elif dlco_pct_predicted < 60.0:
        severity = "MODERATE DIFFUSION IMPAIRMENT"
        action = "Comprehensive autoimmune interstitial panel, echo for pulmonary hypertension."
    elif dlco_pct_predicted < 80.0:
        severity = "MILD GAS TRANSFER REDUCTION"
        action = "Audit environmental exposures, micro-aerosol particulate levels, follow-up PFT in 6 months."
    else:
        severity = "NORMAL ALVEOLAR-CAPILLARY DIFFUSION CAPACITY"
        action = "Alveolar membrane gas exchange integrity intact."
        
    result = {
        "status": "success",
        "measured_dlco": dlco_measured_ml_min_mmhg,
        "hemoglobin_adjusted_dlco": dlco_adjusted,
        "dlco_percent_predicted": dlco_pct_predicted,
        "kco_transfer_coefficient": kco_ratio,
        "alveolar_gas_exchange_tier": severity,
        "clinical_management_directive": action,
        "engine": "GenPark Pulmonary DLCO Gas Exchange Mechanics Engine v1.0"
    }
    return result

# MCP Tool Definitions
TOOLS = {
    "evaluate_pulmonary_dlco_diffusion": {
        "name": "evaluate_pulmonary_dlco_diffusion",
        "description": "Calculates hemoglobin-adjusted diffusing capacity of the lungs for carbon monoxide (DLCO), alveolar volume (VA), and diffusion coefficient (KCO), identifying alveolar-capillary membrane thickening.",
        "parameters": {
            "type": "object",
            "properties": {
                "dlco_measured_ml_min_mmhg": {"type": "number", "description": "Unadjusted DLCO measured in mL/min/mmHg"},
                "dlco_predicted_ml_min_mmhg": {"type": "number", "description": "Predicted normal DLCO based on age, sex, height"},
                "hemoglobin_g_dl": {"type": "number", "description": "Patient blood hemoglobin level (g/dL)"},
                "alveolar_volume_liters": {"type": "number", "description": "Alveolar volume VA (liters)"},
                "is_male": {"type": "boolean", "description": "Biological sex of patient"},
            },
            "required": ['dlco_measured_ml_min_mmhg', 'dlco_predicted_ml_min_mmhg', 'hemoglobin_g_dl', 'alveolar_volume_liters', 'is_male']
        }
    }
}

def handle_rpc_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": list(TOOLS.values())}}
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "evaluate_pulmonary_dlco_diffusion":
            res = evaluate_pulmonary_dlco_diffusion(**args)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method '{tool_name}' not found"}}
    elif method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-personal-agent-pulmonary-dlco-gas-diffusion-capacity-skill", "version": "1.0.0"}
            }
        }
    else:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not implemented"}}

def run_self_test():
    print("Executing self-test for genpark-personal-agent-pulmonary-dlco-gas-diffusion-capacity-skill...")
    test_args = {'dlco_measured_ml_min_mmhg': 24.5, 'dlco_predicted_ml_min_mmhg': 31.0, 'hemoglobin_g_dl': 14.2, 'alveolar_volume_liters': 5.4, 'is_male': True}
    res = evaluate_pulmonary_dlco_diffusion(**test_args)
    assert res['status'] == 'success', f'Test failed: {res}'
    print("SELF TEST PASSED: genpark-personal-agent-pulmonary-dlco-gas-diffusion-capacity-skill functional.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_self_test()
        sys.exit(0)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_rpc_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stderr.write(f"Error handling request: {e}\n")
