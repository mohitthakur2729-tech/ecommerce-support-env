def grade(progress):
    score = 0

    if "ask_order_id" in progress:
        score += 0.3

    if "verify_order" in progress:
        score += 0.3

    if "process_refund" in progress:
        score += 0.4

    score = min(score, 1.0)

    # STRICT RANGE (0,1)
    if score >= 1.0:
        return 0.99
    elif score <= 0.0:
        return 0.01

    return score
