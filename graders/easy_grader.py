def grade(progress):
    score = 0.99 if "respond_user" in progress else 0.01
    return max(0.01, min(0.99, float(score)))