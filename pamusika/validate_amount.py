def validate_withdrawal_amount(amount, whatsapp, phone):
    """
    Validates the withdrawal amount entered by the user.

    Parameters:
    - amount (str): The amount to withdraw as a string.

    Returns:
    - (bool, str): A tuple where the first element indicates if the withdrawal is valid,
                    and the second element is a message regarding the validation.
    """
    # Attempt to convert input to float
    try:
        amount = float(amount)
    except ValueError:
        return False, whatsapp.send_text(
            to=phone,
            body="You have entered an invalid amount. Please enter a valid amount.",
        )

    # Check if the amount is positive
    if amount <= 0:
        return False, "Invalid amount: Withdrawal amount must be greater than zero."

    return True, "Withdrawal amount is valid."


# Example usage
if __name__ == "__main__":
    withdrawal_input = input("Enter the withdrawal amount (as a float): ")

    is_valid, message = validate_withdrawal_amount(withdrawal_input)

    print(message)

    if is_valid:
        # Proceed with further actions like updating balance
        print("You can proceed with the withdrawal.")
