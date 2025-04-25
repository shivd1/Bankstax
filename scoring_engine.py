def evaluate_metric(metric, value, role):
    """
    Grades a financial ratio based on role:
    - 'depositor' = user wants to deposit safely
    - 'borrower' = corporate checking bank's lending strength
    """

    if metric == "Core Deposits to Total Deposits":
        if value > 0.80: return 3, "🟢 Strong core funding"
        elif value >= 0.60: return 2, "🟡 Moderate reliance on core deposits"
        else: return 1, "🔴 High dependence on volatile deposits"

    elif metric == "NPAs to Total Loans":
        if value < 0.02: return 3, "🟢 Very low defaults"
        elif value <= 0.04: return 2, "🟡 Some stress visible"
        else: return 1, "🔴 Risky borrower base"

    elif metric == "Liquidity Ratio":
        if value > 1.2: return 3, "🟢 Strong short-term coverage"
        elif value >= 1.0: return 2, "🟡 Adequate but tight liquidity"
        else: return 1, "🔴 Liquidity risk in short-term obligations"

    elif metric == "Capital Adequacy Ratio":
        if value > 0.12: return 3, "🟢 Well-capitalized"
        elif value >= 0.08: return 2, "🟡 Meets minimum capital"
        else: return 1, "🔴 Below safe capital thresholds"

    elif metric == "Solvency Ratio":
        if value > 0.20: return 3, "🟢 Strong long-term sustainability"
        elif value >= 0.10: return 2, "🟡 Acceptable solvency"
        else: return 1, "🔴 Weak solvency coverage"

    elif metric == "Loans to Deposit Ratio":
        if 0.80 <= value <= 0.90: return 3, "🟢 Healthy lending efficiency"
        elif 0.70 <= value <= 1.00: return 2, "🟡 Could improve balance"
        else: return 1, "🔴 Potential mismatch in funding/lending"

    return 0, "Metric unknown or not applicable"

def calculate_grades(ratios):
    depositor_metrics = [
        "Core Deposits to Total Deposits",
        "Liquidity Ratio",
        "Capital Adequacy Ratio",
        "Solvency Ratio"
    ]

    borrower_metrics = [
        "NPAs to Total Loans",
        "Loans to Deposit Ratio",
        "Liquidity Ratio",
        "Capital Adequacy Ratio"
    ]

    depositor_results = {}
    borrower_results = {}
    depositor_score = 0
    borrower_score = 0

    for metric in depositor_metrics:
        val = ratios.get(metric)
        if val is not None:
            score, reason = evaluate_metric(metric, val, "depositor")
            depositor_results[metric] = {"value": val, "score": score, "reason": reason}
            depositor_score += score

    for metric in borrower_metrics:
        val = ratios.get(metric)
        if val is not None:
            score, reason = evaluate_metric(metric, val, "borrower")
            borrower_results[metric] = {"value": val, "score": score, "reason": reason}
            borrower_score += score

    def convert_score(score, total):
        percent = score / total
        if percent >= 0.85: return "🅰️ A (Very Safe)"
        elif percent >= 0.70: return "🅱️ B (Safe)"
        elif percent >= 0.55: return "🇨 C (Watchlist)"
        elif percent >= 0.40: return "🇩 D (Risky)"
        else: return "🇫 F (Unsafe)"

    depositor_grade = convert_score(depositor_score, len(depositor_metrics) * 3)
    borrower_grade = convert_score(borrower_score, len(borrower_metrics) * 3)

    return {
        "depositor": {
            "score": depositor_score,
            "grade": depositor_grade,
            "details": depositor_results
        },
        "borrower": {
            "score": borrower_score,
            "grade": borrower_grade,
            "details": borrower_results
        }
    }
