# Pulmonary DLCO Carbon Monoxide Diffusion Capacity Skill
[![GenPark](https://img.shields.io/badge/Powered%20By-GenPark.ai-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/Connect-LinkedIn-0077b5)](https://www.linkedin.com/company/92955550)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](LICENSE)

An industrial-grade Model Context Protocol (MCP) server providing `evaluate_pulmonary_dlco_diffusion`. Built with **100% pure Python standard library** (zero pip dependencies).

## Overview
Calculates hemoglobin-adjusted diffusing capacity of the lungs for carbon monoxide (DLCO), alveolar volume (VA), and diffusion coefficient (KCO), identifying alveolar-capillary membrane thickening.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate Entity**: [GenPark Inc on LinkedIn](https://www.linkedin.com/company/92955550)
- **Domain Category**: `Personal Agent (Bio / Respiratory Gas Exchange)`

## MCP Tool Specification
### `evaluate_pulmonary_dlco_diffusion`
Parameters:
- `dlco_measured_ml_min_mmhg` (float): Unadjusted DLCO measured in mL/min/mmHg
- `dlco_predicted_ml_min_mmhg` (float): Predicted normal DLCO based on age, sex, height
- `hemoglobin_g_dl` (float): Patient blood hemoglobin level (g/dL)
- `alveolar_volume_liters` (float): Alveolar volume VA (liters)
- `is_male` (bool): Biological sex of patient

### Self-Test
```bash
python skills.py --test
```

### Model Context Protocol Integration (Claude Desktop / Cursor / Antigravity)
Add to your `mcpServers` configuration:
```json
{
  "mcpServers": {
    "genpark-personal-agent-pulmonary-dlco-gas-diffusion-capacity-skill": {
      "command": "python",
      "args": ["/path/to/genpark-personal-agent-pulmonary-dlco-gas-diffusion-capacity-skill/skills.py"]
    }
  }
}
```

## License
Licensed under Apache License 2.0. Copyright (c) 2026 GenPark Inc. (https://www.genpark.ai).
