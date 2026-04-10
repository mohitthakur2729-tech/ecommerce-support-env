from env.models import Action

def simple_agent(observation):
    query = observation.query.lower()
    progress = observation.progress or []

    # STOP LOOP
    if len(progress) > 5:
        return Action("respond_user", "Completed")

    # -------------------------
    # 🟢 EASY TASK 
    # -------------------------
    if "status" in query or "delivery" in query:
        return Action("respond_user", "Providing order status.")

    # -------------------------
    # 🔴 HARD TASK 
    # -------------------------
    if ("missing" in query and "damaged" in query) or "multiple" in query:

        if "identify_multiple_issues" not in progress:
            return Action("identify_multiple_issues", "Detected multiple issues")

        elif "process_refund" not in progress:
            return Action("process_refund", "Processing refund")

        elif "handle_missing_item" not in progress:
            return Action("handle_missing_item", "Handling missing item")

        else:
            return Action("respond_user", "All issues resolved")

    # -------------------------
    # 🟡 MEDIUM TASK
    # -------------------------
    if "ask_order_id" not in progress:
        return Action("ask_order_id", "Please provide order ID")

    elif "verify_order" not in progress:
        return Action("verify_order", "Verifying order")

    elif "process_refund" not in progress:
        return Action("process_refund", "Processing refund")

    else:
        return Action("respond_user", "Issue resolved")