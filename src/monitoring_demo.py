import pandas as pd
# Try this more modern import structure
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

def generate_drift_report():
    try:
        # Load your actual data from the notebook folder [cite: 28]
        reference_data = pd.read_csv("notebooks/data.csv")
        current_data = reference_data.sample(frac=0.8) 

        report = Report(metrics=[DataDriftPreset()])
        report.run(reference_data=reference_data, current_data=current_data)
        
        report.save_html("drift_report.html")
        print("✅ Success! Drift report generated: drift_report.html")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    generate_drift_report()