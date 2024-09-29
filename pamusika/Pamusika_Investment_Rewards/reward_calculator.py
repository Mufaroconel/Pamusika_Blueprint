def calculate_reward(cost_price, selling_price):
    # Calculate profit per unit
    profit = selling_price - cost_price

    # Calculate profit margin
    profit_margin = (profit / cost_price) * 100 if cost_price != 0 else 0

    # Determine reward based on profit margin
    if 50 <= profit_margin <= 75:
        reward_percentage = 0.08
    elif profit_margin > 75:
        reward_percentage = 0.12
    else:
        reward_percentage = 0.05  # Default reward percentage for low-margin products

    # Calculate reward based on the percentage of the profit
    reward = profit * reward_percentage
    return reward
