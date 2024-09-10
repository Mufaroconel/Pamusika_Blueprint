import difflib

# Define valid streets with house number ranges
valid_addresses = {
    "jiri crescent": range(1, 101),  # House numbers from 1 to 100 for Jiri Crescent
    "mukumbadzetse": range(1, 101),    # House numbers from 1 to 100 for Mukumbadzetse
    "muridzamhara": range(1, 101),     # House numbers from 1 to 100 for Muridzamhara
}

def suggest_street(street_name):
    # Use difflib to get a list of close matches (suggestions)
    suggestions = difflib.get_close_matches(street_name, valid_addresses.keys(), n=1, cutoff=0.6)
    if suggestions:
        return suggestions[0]  # Return the closest match
    return None

def validate_address(full_address):
    try:
        # Convert input address to lowercase for comparison and split into components
        parts = full_address.strip().lower().split(' ', 2)  # Split into 3 parts: house number, street, and the rest
        house_number = int(parts[0])                        # First part is the house number
        street = parts[1].strip()                           # Second part is the street name
        if len(parts) > 2:
            street += f" {parts[2].strip()}"                # If there’s a third part, concatenate to street

        # Check if the street is in the valid addresses
        if street in valid_addresses:
            # Check if the house number falls within the valid range for that street
            if house_number in valid_addresses[street]:
                return True, None  # Address is valid, no suggestion needed
            else:
                return False, None  # Invalid house number, no suggestion
        else:
            # Suggest a street if the input street is not valid
            suggestion = suggest_street(street)
            return False, suggestion
    except (ValueError, IndexError):
        # Handle errors in format or non-numeric house numbers
        return False, None

def register_user(full_address):
    # Validate the user's address
    is_valid, suggestion = validate_address(full_address)

    if is_valid:
        print("Registration successful! Welcome!")
        return True  # Return True to indicate success
    else:
        if suggestion:
            print(f"Sorry, services are not yet available at this address. Did you mean '{suggestion}'?")
        else:
            print("Sorry, services are not yet available in your area.")
        return False  # Return False to indicate failure
