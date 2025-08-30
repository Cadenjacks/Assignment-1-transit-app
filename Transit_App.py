from requests import get

API_KEY = 'qYqjPyOCoMV_rD3dCF89'

# Ask for user input
lon = float(input("Enter longitude (e.g. -97.138): ").strip())
lat = float(input("Enter latitude (e.g. 49.895): ").strip())
distance = int(input("Enter search radius in meters (e.g. 100): ").strip())

# Get nearby bus stops
url_stops = f"https://api.winnipegtransit.com/v3/stops.json?lon={lon}&lat={lat}&distance={distance}&api-key={API_KEY}"
nearby_stops = get(url_stops).json()
stops = nearby_stops.get('stops', [])

# If none found, inform the user
if not stops:
    print("No bus stops found nearby.")
    exit()

# Display all nearby stops
print("\nNearby Bus Stops:")
for i, stop in enumerate(stops, start=1):
    stop_num = stop['number']
    stop_name = stop['name']
    street = stop['street']['name']
    print(f"{i}. Stop #{stop_num} - {stop_name} at {street}")
    