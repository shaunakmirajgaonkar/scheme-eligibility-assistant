"""
eligibility_engine.py
Rule-based, fully local eligibility checker. No internet, no external calls.
"""

from schemes_data import SCHEMES


def check_eligibility(user):
    """
    user: dict with keys like age, gender, occupation, annual_income,
          land_owner, bpl_card, owns_pucca_house, is_student,
          is_pregnant_or_lactating, has_bank_account, location
    Returns list of (scheme_dict, status, matched_pct, reasons) sorted by likely-eligible first.
    """
    results = []

    for scheme in SCHEMES:
        crit = scheme["criteria"]
        total_checks = 0
        passed_checks = 0
        reasons = []

        # Age range
        if "min_age" in crit:
            total_checks += 1
            if user.get("age") is not None and user["age"] >= crit["min_age"]:
                passed_checks += 1
            else:
                reasons.append(f"Minimum age required: {crit['min_age']}")
        if "max_age" in crit:
            total_checks += 1
            if user.get("age") is not None and user["age"] <= crit["max_age"]:
                passed_checks += 1
            else:
                reasons.append(f"Maximum age limit: {crit['max_age']}")

        # Income ceiling
        if "max_income" in crit and crit["max_income"] is not None:
            total_checks += 1
            if user.get("annual_income") is not None and user["annual_income"] <= crit["max_income"]:
                passed_checks += 1
            else:
                reasons.append(f"Annual income should not exceed Rs. {crit['max_income']:,}")

        # Occupation
        if "occupation" in crit:
            total_checks += 1
            if user.get("occupation") in crit["occupation"]:
                passed_checks += 1
            else:
                reasons.append(f"Occupation should be one of: {', '.join(crit['occupation'])}")

        # Gender
        if "gender" in crit:
            total_checks += 1
            if user.get("gender") in crit["gender"]:
                passed_checks += 1
            else:
                reasons.append(f"Scheme applicable for: {', '.join(crit['gender'])}")

        # Location
        if "location" in crit:
            total_checks += 1
            if user.get("location") in crit["location"]:
                passed_checks += 1
            else:
                reasons.append(f"Applicable in: {', '.join(crit['location'])} areas")

        # Boolean flags
        for flag in ["land_owner", "bpl_card", "owns_pucca_house", "is_student",
                     "is_pregnant_or_lactating", "has_bank_account"]:
            if flag in crit:
                total_checks += 1
                allowed_values = crit[flag]
                user_val = user.get(flag)
                if user_val in allowed_values:
                    passed_checks += 1
                else:
                    label = flag.replace("_", " ").title()
                    reasons.append(f"Condition on '{label}' not met")

        pct = round((passed_checks / total_checks) * 100, 1) if total_checks else 100.0

        if pct >= 80:
            status = "Likely Eligible"
        elif pct >= 50:
            status = "Possibly Eligible"
        else:
            status = "Unlikely Eligible"

        results.append({
            "scheme": scheme,
            "status": status,
            "match_pct": pct,
            "reasons": reasons,
        })

    # Sort best matches first
    results.sort(key=lambda r: r["match_pct"], reverse=True)
    return results
