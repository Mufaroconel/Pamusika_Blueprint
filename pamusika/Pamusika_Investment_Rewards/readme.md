# Pamusika Investment Rewards

## Overview

**Pamusika Investment Rewards** is a reward system integrated into the Pamusika platform that allows customers to earn rewards based on their purchases. By incentivizing buying behavior, this functionality encourages customer loyalty while enhancing their shopping experience. Customers can view their rewards as an investment in future savings.

## Features

- **Dynamic Reward Calculation**: Automatically calculates rewards based on product profit margins.
- **Tiered Reward Structure**: Provides varying reward percentages based on profit margins:
  - **>75% Profit Margin**: 10% Reward
  - **50% - 75% Profit Margin**: 7% Reward
  - **30% - 50% Profit Margin**: 5% Reward
  - **<30% Profit Margin**: 2% Reward
- **User-Friendly Dashboard**: Customers can track their accumulated rewards and redeem them easily.
- **Promotional Campaigns**: Ability to run promotions that temporarily increase reward percentages.

### Input Parameters

The following parameters are required to compute rewards for an individual customer:

- `cost_price`: The price at which Pamusika buys the product.
- `selling_price`: The price at which the product is sold to customers.
- `quantity_purchased`: The number of units purchased by the customer.

### Example Calculation

Here’s a simple example of how to use the reward calculation functionality:

```python
cost_price = 0.60  # Cost price of tomatoes
selling_price = 1.00  # Selling price of tomatoes
quantity_purchased = 10  # Quantity purchased

# Calculate profit and rewards
profit_per_unit = calculate_profit(cost_price, selling_price)
total_profit = profit_per_unit * quantity_purchased
reward_percentage = get_reward_percentage(total_profit / (cost_price * quantity_purchased))
total_reward = calculate_reward(total_profit, reward_percentage)

print(f"Total Reward for Customer: ${total_reward:.2f}")
```

### Output

The output will display the total reward earned by the customer based on their purchase.

## Contribution

Contributions are welcome! If you have suggestions for improvements or new features, please submit a pull request or open an issue.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries or support regarding the Pamusika Investment Rewards functionality, please contact:

- Email: support@pamusika.com

---

Thank you for using Pamusika Investment Rewards! We hope you enjoy earning rewards while shopping!
```

### Conclusion

This README.md template provides a comprehensive overview of the **Pamusika Investment Rewards** functionality, including its features, installation instructions, usage examples, and contact information. You can customize it further based on your specific implementation details or additional features you may want to include. If you need further modifications or additional sections, feel free to ask!

Citations:
[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/6683732/186caf2d-49fd-4a1f-8e7c-1bcb633d7723/paste.txt