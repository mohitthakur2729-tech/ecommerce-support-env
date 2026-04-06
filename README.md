# Ecommerce Support RL Environment

## Overview
This project simulates a real-world ecommerce customer support system where an AI agent handles customer queries.

## Tasks
- Easy: Respond to delivery queries
- Medium: Handle damaged product refund
- Hard: Handle multiple issues (missing + damaged items)

## Action Space
- respond_user
- ask_order_id
- verify_order
- process_refund
- identify_multiple_issues
- handle_missing_item

## Observation Space
- query
- history
- progress
- order_status

## Reward System
- Partial reward for correct steps
- Final reward = 1.0
- Penalty for wrong steps

## Run Instructions

```bash
python inference.py