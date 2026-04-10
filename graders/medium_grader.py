def grade(progress):
    score = 0.0

    if "ask_order_id" in progress:
        score += 0.3
    if "verify_order" in progress:
        score += 0.3
    if "process_refund" in progress:
        score += 0.3

    return max(0.01, min(0.99, float(score)))