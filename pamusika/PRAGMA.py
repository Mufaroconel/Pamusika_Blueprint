from sqlalchemy import create_engine, inspect

# Replace with your actual database URI
engine = create_engine("sqlite:///instance/mumsikadatabase.db")
inspector = inspect(engine)

# Get foreign keys for customer_reward
foreign_keys = inspector.get_foreign_keys("customer_reward")
for fk in foreign_keys:
    print(
        f"Constraint Name: {fk['name']}, Column: {fk['constrained_columns']}, Referred Table: {fk['referred_table']}"
    )
