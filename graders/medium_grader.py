def grade(progress):
    score = 0

    if "ask_order_id" in progress:
        score += 0.3

    if "verify_order" in progress:
        score += 0.3

    if "process_refund" in progress:
        score += 0.4

    return min(score, 1.0)
