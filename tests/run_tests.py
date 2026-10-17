#!/usr/bin/env python3
"""Point d’entrée des campagnes DRH-FPT ; logique dans campaign.py."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from campaign import (  # noqa: F401
    EXPECTED_CASES_PER_MODE,
    active_cases,
    build_system_context,
    campaign_signature,
    load_evidence,
    load_legal_skill,
    main,
    normalized_expectations,
    validate_evidence,
    validate_judge_result,
    validate_strict_campaign,
)


if __name__ == "__main__":
    raise SystemExit(main())
