from sqlalchemy import create_engine, inspect

# Replace with your actual database URI
engine = create_engine('sqlite:///instance/mumsikadatabase.db')
inspector = inspect(engine)

# Check if customer_reward table exists
if 'customer_reward' in inspector.get_table_names():
    print("Table 'customer_reward' exists.")
else:
    print("Table 'customer_reward' does not exist.")