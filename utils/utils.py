import re
import pandas as pd

us_states = {
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming',
}

def is_coordinate_line(line):
    try:
        parts = line.split(',')
        if len(parts) == 2:
            float(parts[0])
            float(parts[1])
            return True
        return False
    except ValueError:
        return False

def is_phone_number(line):
    phone_number_pattern = r"(\d{3}[-\.\s]?\d{3}[-\.\s]?\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]?\d{4}|1\s*\d{3}[-\.\s]?\d{3}[-\.\s]?\d{4}|1\(\d{3}\)\s*\d{3}[-\.\s]?\d{4})" 
    return bool(re.search(phone_number_pattern, line))

def has_integer_string(string):
    hasInt = False
    for word in string.split():
        try:
            int(word)
            return True
        except ValueError:
            continue
    return False

def remove_duplicates(lst):
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

def state_abbreviation_map():
    return set(us_states.keys())

def flatten_list(lst):
    flat_list = []

    for ls in lst:
        for x in ls:
            flat_list.append(x)
    return flat_list

def get_geolocation(meeting):
    city = meeting.address.city
    state = meeting.address.state.value
    print(f"{city}, {state}")

    try:
        df = pd.read_csv('utils/places.csv') 

        result = df[(df['feature_name'] == city) & (df['state_name'] == state)]

        if not result.empty:  # Check if the result is not empty (row found)
            lat = result['prim_lat_dec'].values[0]  # Extract latitude
            long = result['prim_long_dec'].values[0] # Extract longitude
            meeting.setGeolocation(lat, long)
            print(f"Latitude: {lat}, Longitude: {long}") 
        else:
            print("No matching row found.")
        return meeting
    except FileNotFoundError:
        print("Error: CSV file not found. Please make sure the file exists in the correct location.")
    except KeyError as e:
        return meeting
    except Exception as e:  # Catch any other potential errors
        print(f"An unexpected error occurred: {e}")
        return meeting