# Example: Carbon-Aware Deployment

> Run heavy workloads when and where the grid is greenest.

**Principle**: #6 Emissions Are Invisible

## carbon_scheduler.py

```python
from enum import Enum

class Urgency(Enum):
    REAL_TIME = "real_time"        # Always run
    WITHIN_HOURS = "within_hours"  # Run if grid < 400 gCO2/kWh
    BATCH = "batch"                # Run only if grid < 200
    LOW_PRIORITY = "low_priority"  # Run only if grid < 100

THRESHOLDS = {
    Urgency.REAL_TIME: float("inf"),
    Urgency.WITHIN_HOURS: 400,
    Urgency.BATCH: 200,
    Urgency.LOW_PRIORITY: 100,
}

# Approximate carbon intensity by cloud region (gCO2/kWh)
REGIONS = {
    "northamerica-northeast1": 20,   # Montreal (hydro)
    "europe-north1": 30,             # Finland
    "europe-west1": 50,              # Belgium
    "us-west1": 100,                 # Oregon
    "europe-west3": 350,             # Frankfurt
    "us-east1": 380,                 # South Carolina
    "asia-south1": 700,              # Mumbai
    "asia-east1": 550,               # Taiwan
}


def should_run_now(region, urgency):
    intensity = REGIONS.get(region, 400)
    threshold = THRESHOLDS[urgency]
    ok = intensity <= threshold
    greenest = min(REGIONS, key=REGIONS.get)
    msg = f"OK ({intensity} <= {threshold})" if ok else \
          f"DEFER — grid too dirty ({intensity} > {threshold}). Try {greenest} ({REGIONS[greenest]})"
    return {"run": ok, "intensity": intensity, "message": msg}


def estimate_carbon(llm_calls, model_size, region):
    energy_map = {"small": 0.001, "medium": 0.005, "large": 0.03}
    energy = llm_calls * energy_map.get(model_size, 0.005)
    intensity = REGIONS.get(region, 400)
    co2_g = energy * intensity
    return {
        "calls": llm_calls, "model": model_size, "region": region,
        "energy_kwh": round(energy, 2),
        "co2_grams": round(co2_g, 1),
        "co2_kg_annual": round(co2_g * 365 / 1000, 1),
        "equivalent": f"~{co2_g * 365 / 1000 / 4600:.1f} cars/year" if co2_g > 1000 else f"~{co2_g:.0f}g CO2/day",
    }


if __name__ == "__main__":
    # Should I run batch in Mumbai?
    result = should_run_now("asia-south1", Urgency.BATCH)
    print(f"Mumbai batch: {result['message']}")

    # Compare regions
    print("\n--- Same workload, different regions ---")
    for region in ["asia-south1", "us-east1", "northamerica-northeast1"]:
        est = estimate_carbon(10_000, "medium", region)
        print(f"  {region:30s} → {est['co2_grams']:>8.1f}g CO2/day  ({est['co2_kg_annual']} kg/year)")

    # Reduction
    mumbai = estimate_carbon(10_000, "medium", "asia-south1")
    quebec = estimate_carbon(10_000, "medium", "northamerica-northeast1")
    pct = (1 - quebec["co2_grams"] / mumbai["co2_grams"]) * 100
    print(f"\n  Region switch Mumbai→Quebec: {pct:.0f}% carbon reduction")
```

## Run It

```bash
python examples/carbon-aware-deployment/carbon_scheduler.py
```

## Expected Output

```
Mumbai batch: DEFER — grid too dirty (700 > 200). Try northamerica-northeast1 (20)

--- Same workload, different regions ---
  asia-south1                    →    35000.0g CO2/day  (12775.0 kg/year)
  us-east1                       →    19000.0g CO2/day  (6935.0 kg/year)
  northamerica-northeast1        →     1000.0g CO2/day  (365.0 kg/year)

  Region switch Mumbai→Quebec: 97% carbon reduction
```
