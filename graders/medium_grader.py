def grade(progress):
    score = 0.05
    if "ask_order_id" in progress:
        score += 0.25
    if "verify_order" in progress:
        score += 0.25
    if "process_refund" in progress:
        score += 0.25
    return round(max(0.01, min(0.99, float(score))), 4)