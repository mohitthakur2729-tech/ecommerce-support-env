def get_task(difficulty: str) -> dict:
    if difficulty == "easy":
        return {
            "query": "Customer asks about order status.",
            "expected_steps": ["respond_user"],
            "order_status": "shipped"
        }
    elif difficulty == "medium":
        return {
            "query": "Customer reports issue with payment.",
            "expected_steps": ["ask_order_id", "verify_order", "process_refund"],
            "order_status": "pending"
        }
    else:  # hard
        return {
            "query": "Complex refund request with multiple items.",
            "expected_steps": ["identify_multiple_issues", "process_refund", "handle_missing_item"],
            "order_status": "delivered"
        }
