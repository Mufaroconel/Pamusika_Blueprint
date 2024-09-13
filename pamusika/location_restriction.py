import difflib

# Define valid streets with house number ranges
valid_addresses = {
    "jiri": range(1, 101),  
    "muridzamhara": range(1, 151),
    "mukumbadzetse": range(1, 151), 
    "donhodzo": range(1, 151),
    "muchakata": range(1, 151),
    "mupani": range(1, 151),
    "zambuko": range(1, 151),
    "mvumba": range(1, 151),
    "cheni": range(1, 151),
    "jachacha": range(1, 151),
    "mvuto": range(1, 151),
    "bembenene": range(1, 151),
    "chiraramhene": range(1, 151),
    "mbambarize": range(1, 151),
}

def suggest_street(street_name):
    # Use difflib to get a list of close matches (suggestions)
    suggestions = difflib.get_close_matches(street_name, valid_addresses.keys(), n=1, cutoff=0.6)
    if suggestions:
        return suggestions[0]  # Return the closest match
    return None

def extract_street_name(address_parts):
    """Extracts the second part (street name) from the address, regardless of length."""
    if len(address_parts) > 1:
        # If address has more than 2 parts, assume second part is the start of the street name
        return address_parts[1].strip().lower()
    return ""  # If no second part, return an empty string

def validate_address(full_address):
    try:
        # Convert input address to lowercase for comparison and split into components
        parts = full_address.strip().lower().split(' ')  # Split into parts: house number, street, etc.
        house_number = int(parts[0])  # First part is the house number

        # Extract the second part of the address as the street name
        street_name = extract_street_name(parts)

        # Check if the street is in the valid addresses
        if street_name in valid_addresses:
            # Check if the house number falls within the valid range for that street
            if house_number in valid_addresses[street_name]:
                return True, None  # Address is valid, no suggestion needed
            else:
                return False, None  # Invalid house number, no suggestion
        else:
            # Suggest a street if the input street is not valid
            suggestion = suggest_street(street_name)
            return False, suggestion
    except (ValueError, IndexError):
        # Handle errors in format or non-numeric house numbers
        return False, None
