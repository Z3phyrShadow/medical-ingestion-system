import pandas as pd


def export_to_csv(normalized_output: dict, filename: str = "medical_output.csv") -> None:
    """Export normalized pipeline output to CSV and print patient info."""
    normalized_data = normalized_output.get("normalized_data", normalized_output)

    pi = normalized_data.get("patient_info", {})
    patient_info = {
        "patient_name": pi.get("patient_name"),
        "age": pi.get("age"),
        "gender": pi.get("gender"),
        "date_of_birth": pi.get("date_of_birth"),
    }

    lab_results = normalized_data.get("lab_results", [])
    df = pd.DataFrame(lab_results)
    df.to_csv(filename, index=False)

    print(f"Lab results saved to {filename}")
    print("\nPATIENT INFO")
    for k, v in patient_info.items():
        print(f"  {k}: {v}")

    flags = normalized_output.get("validation_flags", [])
    if flags:
        print("\nVALIDATION FLAGS")
        for flag in flags:
            print(f"  ⚠ {flag}")
