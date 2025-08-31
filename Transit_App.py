from requests import get

# Used to format date/time in the requested format
from dateutil.parser import parse

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

# Let user pick a stop
choice = input("\nEnter the stop number you want to check: ")
selected_stop = next((s for s in stops if str(s['number']) == choice), None)

# If user enters invalid stop
if not selected_stop:
    print("Invalid stop number.")
    exit()

stop_num = selected_stop['number']

# Get arrival times for selected stop
url_schedule = f"https://api.winnipegtransit.com/v3/stops/{stop_num}/schedule.json?api-key={API_KEY}"
schedule_data = get(url_schedule).json()

stop_schedule = schedule_data.get('stop-schedule', {})
route_schedules = stop_schedule.get('route-schedules', {})

if not route_schedules:
    print("No upcoming buses for this stop.")
    exit()

# Display upcoming stops
print(f"\nUpcoming Arrivals at stop #{stop_num}:\n")

for route_schedule in route_schedules:
    route = route_schedule.get('route', {})
    route_name = route.get('name', 'Unknown Route')
    scheduled_stops = route_schedule.get('scheduled-stops', [])

    print(f"Route {route.get('key')} - {route_name}")
    for scheduled in scheduled_stops[:3]: # Only display the next 3 arrivals
        times = scheduled.get('times', {})
        scheduled_time_str = times.get('arrival', {}).get('scheduled')
        estimated_time_str = times.get('arrival', {}).get('estimated')

        # Parse timestamps
        if scheduled_time_str:
            scheduled_dt = parse(scheduled_time_str)
            scheduled_time_fmt = scheduled_dt.strftime("%H:%M:%S")
        else:
            scheduled_time_fmt = "N/A"

        if estimated_time_str:
            estimated_dt = parse(estimated_time_str)
            estimated_time_fmt = estimated_dt.strftime("%H:%M:%S")
        else:
            estimated_time_fmt = "N/A"

        # Output arrival info with color
        print(f"Scheduled: {scheduled_time_fmt}, Estimated: {estimated_time_fmt}")
    print()