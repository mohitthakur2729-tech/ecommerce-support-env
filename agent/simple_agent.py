from env.models import Action

def simple_agent(observation):
    query = observation.query.lower()
    progress = observation.progress or []

    if len(progress) > 3:
        return Action("respond_user", "Completed")

    # 🟢 EASY: status queries
    if "status" in query or "delivery" in query:
        return Action("respond_user", "Providing order status.")

    # 🔴 HARD: multiple issues
    if (
    "multiple" in query
    or "complex" in query
    or ("missing" in query and "damaged" in query)
):
        if "identify_multiple_issues" not in progress:
            return Action("identify_multiple_issues", "")
        elif "process_refund" not in progress:
            return Action("process_refund", "")
        elif "handle_missing_item" not in progress:
            return Action("handle_missing_item", "")
        else:
            return Action("respond_user", "")

    # 🟡 MEDIUM
    if "ask_order_id" not in progress:
        return Action("ask_order_id", "")
    elif "verify_order" not in progress:
        return Action("verify_order", "")
    elif "process_refund" not in progress:
        return Action("process_refund", "")
    else:
        return Action("respond_user", "")