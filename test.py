from aircraft import AIRCRAFT
from calculations import calculate_results

config = AIRCRAFT["108 PAX"]

results = calculate_results(
    config=config,
    passengers=95,
    oa=20,
    ob=45,
    oc=30,
    cargo1=1200,
    cargo4=800,
    tof=7000,
    tf=2500
)

for key, value in results.items():
    print(f"{key}: {value}")