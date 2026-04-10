def grade(progress):
    score = 0.0

    if "ask_order_id" in progress:
        score += 0.3
    if "verify_order" in progress:
        score += 0.3
    if "process_refund" in progress:
        score += 0.4

    # 🔥 STRICT RANGE (NO min(score,1.0))
    if score >= 1.0:
        score = 0.99
    elif score <= 0.0:
        score = 0.01

    return score