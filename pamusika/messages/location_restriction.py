# Define valid streets with house number ranges
valid_addresses = {
    "Jiri Crescent": range(1, 101),  # House numbers from 1 to 100 for Jiri Crescent
    "Main Street": range(1, 101),    # House numbers from 1 to 100 for Main Street
    "Broadway": range(1, 101),       # House numbers from 1 to 100 for Broadway
}

def validate_address(full_address):
    try:
        # Split the input into components, assuming first is house number and second is street
        parts = full_address.strip().split(' ', 2)  # Split into 3 parts: house number, street, and the rest
        house_number = int(parts[0])                # First part is the house number
        street = parts[1].strip().title()           # Second part is the street name
        if len(parts) > 2:
            street += f" {parts[2].strip().title()}"   # If there’s a third part, concatenate to street

        # Check if the street is in the valid addresses
        if street in valid_addresses:
            # Check if the house number falls within the valid range for that street
            if house_number in valid_addresses[street]:
                return True
            else:
                return False
        else:
            return False
    except (ValueError, IndexError):
        # Handle errors in format or non-numeric house numbers
        return False

def register_user(full_address):
    # Check if the address is valid
    if validate_address(full_address):
        print("Registration successful! Welcome!")
    else:
        print("Sorry, services are not yet available in your area.")

# Example of how to use the function
address_input = input("Enter your address (e.g., '69 Jiri Crescent Mufakose Harare'): ")
register_user(address_input)
