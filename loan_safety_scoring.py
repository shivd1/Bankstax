def grade_ratio(metric, value):
    if metric == "Core Deposits to Total Deposits":
        if value > 0.80: return 3, "🟢 Safe"
        elif value >= 0.60: return 2, "🟡 Watch"
        else: return 1, "🔴 Risky"

    elif metric == "NPAs to Total Loans":
        if value < 0.02: return 3, "🟢 Safe"
        elif value <= 0.04: return 2, "🟡 Watch"
        else: return 1, "🔴 Risky"

    elif metric == "Liquidity Ratio":
        if value > 1.2: return 3, "🟢 Safe"
        elif value >= 1.0: return 2, "🟡 Watch"
        else: return 1, "🔴 Risky"

    elif metric == "Capital Adequacy Ratio":
        if value > 0.12: return 3, "🟢 Safe"
        elif value >= 0.08: return 2, "🟡 Watch"
        else: return 1, "🔴 Risky"

    elif metric == "Solvency Ratio":
        if value > 0.20: return 3, "🟢 Safe"
        elif value >= 0.10: return 2, "🟡 Watch"
        else: return 1, "🔴 Risky"

    elif metric == "Loans to Deposit Ratio":
        if 0.80 <= value <= 0.90: return 3, "🟢 Optimal"
        elif 0.70 <= value <= 1.00: return 2, "🟡 Acceptable"
        else: return 1, "🔴 Risky"

    return 0, "Invalid"

def calculate_loan_safety(data):
    graded = {}
    score_total = 0
    for metric, value in data.items():
        score, label = grade_ratio(metric, value)
        graded[metric] = {"value": value, "score": score, "label": label}
        score_total += score

    if score_total >= 16: grade = "🅰️ A (Very Safe)"
    elif score_total >= 13: grade = "🅱️ B (Generally Safe)"
    elif score_total >= 10: grade = "🇨 C (Caution)"
    elif score_total >= 7: grade = "🇩 D (Risky)"
    else: grade = "🇫 F (Unsafe)"

    return graded, grade
