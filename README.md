---
title: Ecommerce Support RL Environment
emoji: 🛒
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# Ecommerce Support RL Environment

RL environment simulating ecommerce customer support tasks.

## Environment Description
Customer support agent that handles refunds, missing items, and complex queries.

## Action Space
- ask_order_id
- verify_order
- process_refund
- respond_user
- identify_multiple_issues
- handle_missing_item

## Observation Space
- query: customer message
- progress: list of completed actions

## Tasks
- Easy: respond_user → score 1.0
- Medium: ask_order_id → verify_order → process_refund → score 1.0
- Hard: identify_multiple_issues → process_refund → handle_missing_item → score 1.0

## Setup
```bash
pip install -r requirements.txt
python inference.py
```

## Baseline Scores
- Easy: 1.0
- Medium: 1.0
- Hard: 1.0