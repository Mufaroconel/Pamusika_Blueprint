import difflib

# Define valid streets with house number ranges for each region in Mufakose
harare_residential_areas = {
    "mufakose": {
        "regions": {
            "region_1": {
                "valid_addresses": {
                    "jiri crescent": range(1, 101),
                    "muridzamhara": range(1, 151),
                    # "mukumbadzetse": range(1, 151),
                    # "donhodzo": range(1, 151),
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
                },
                "admin": "admin_region1@example.com",
            },
            "region_2": {
                "valid_addresses": {
                    "mukumbadzetse": range(1, 151),
                    "donhodzo": range(1, 151),
                    # Add more streets for region 2
                },
                "admin": "admin_region2@example.com",
            },
            # Add more regions as needed
        }
    },
    # Add more neighborhoods as needed
}


def suggest_street(street_name, neighborhood, region):
    """Suggests a close match for an invalid street name."""
    valid_streets = harare_residential_areas[neighborhood]["regions"][region][
        "valid_addresses"
    ].keys()
    suggestions = difflib.get_close_matches(street_name, valid_streets, n=1, cutoff=0.6)
    if suggestions:
        return suggestions[0]  # Return the closest match
    return None


def extract_street_name(address_parts):
    """Extracts the street name from the address parts."""
    # Join all parts except the last two (neighborhood and city)
    return (
        " ".join(address_parts[1:-2]).strip().lower()
    )  # Assuming last two parts are neighborhood and city


def validate_address(full_address):
    """Validates the full address and returns the corresponding region if valid."""
    try:
        parts = full_address.strip().lower().split(" ")
        house_number = int(parts[0])  # First part is the house number

        # Extract the street name
        street_name = extract_street_name(parts)

        # Check each neighborhood and its regions
        for neighborhood in harare_residential_areas:
            for region in harare_residential_areas[neighborhood]["regions"]:
                valid_addresses = harare_residential_areas[neighborhood]["regions"][
                    region
                ]["valid_addresses"]

                # Validate street and house number
                if street_name in valid_addresses:
                    if house_number in valid_addresses[street_name]:
                        return True, neighborhood, region  # Address is valid
                    else:
                        return False, None, None  # Invalid house number
                else:
                    suggestion = suggest_street(street_name, neighborhood, region)
                    if suggestion:
                        return False, suggestion, None  # Suggest a street if invalid

        return False, None, None  # Address not found in any neighborhood or region
    except (ValueError, IndexError):
        return False, None, None  # Handle errors in format or non-numeric house numbers


# Example usage of the validation function
address = "69 Mukumbadzetse Mufakose Harare"
is_valid, suggestion, region = validate_address(address)
if is_valid:
    print(f"The address is valid in {region} of {suggestion}.")
else:
    print(f"The address is invalid. Did you mean: {suggestion}")
