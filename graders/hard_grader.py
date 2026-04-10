def grade(progress):
    score = 0.0

    if "identify_multiple_issues" in progress:
        score += 0.3
    if "process_refund" in progress:
        score += 0.3
    if "handle_missing_item" in progress:
        score += 0.3

    return max(0.01, min(0.99, float(score)))