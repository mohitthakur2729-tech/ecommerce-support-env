def grade(progress):
    score = 1.0 if "respond_user" in progress else 0.0

    # STRICT RANGE (0,1)
    if score >= 1.0:
        return 0.99
    elif score <= 0.0:
        return 0.01

    return score
