from app.services.workload_generator import generate_workload


workload = generate_workload(
    duration_minutes=1440,
    interval_seconds=60,
    random_seed=42
)

output_file = "data/synthetic_workload.csv"

workload.to_csv(output_file, index=False)

print(f"Dataset generated successfully!")
print(f"Saved to: {output_file}")
print(f"Rows: {len(workload)}")
print(f"Columns: {len(workload.columns)}")