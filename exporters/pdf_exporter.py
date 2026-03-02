from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


def export_to_pdf(normalized_output: dict, filename: str = "medical_report.pdf") -> None:
    """Export normalized pipeline output to a formatted PDF report."""
    normalized_data = normalized_output.get("normalized_data", normalized_output)

    doc = SimpleDocTemplate(filename)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph("<b>Medical Report Summary</b>", styles["Title"]))
    elements.append(Spacer(1, 0.3 * inch))

    # Patient Info table
    pi = normalized_data.get("patient_info", {})
    patient_rows = [
        ["Patient Name", str(pi.get("patient_name") or "—")],
        ["Age", str(pi.get("age") or "—")],
        ["Gender", str(pi.get("gender") or "—")],
        ["Date of Birth", str(pi.get("date_of_birth") or "—")],
    ]
    patient_table = Table(patient_rows, colWidths=[2.5 * inch, 3 * inch])
    patient_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 1, colors.grey),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ])
    )
    elements.append(patient_table)
    elements.append(Spacer(1, 0.4 * inch))

    # Lab Results table
    lab_results = normalized_data.get("lab_results", [])
    if lab_results:
        elements.append(Paragraph("<b>Lab Results</b>", styles["Heading2"]))
        elements.append(Spacer(1, 0.1 * inch))

        table_data = [["Test Name", "Value", "Unit", "Reference Range"]]
        for lab in lab_results:
            table_data.append([
                str(lab.get("test_name") or ""),
                str(lab.get("value") or ""),
                str(lab.get("unit") or ""),
                str(lab.get("reference_range") or ""),
            ])

        lab_table = Table(table_data, repeatRows=1, colWidths=[2.5 * inch, 1 * inch, 1 * inch, 2 * inch])
        lab_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.Color(0.95, 0.95, 0.95)]),
            ])
        )
        elements.append(lab_table)
        elements.append(Spacer(1, 0.3 * inch))

    # Validation flags
    flags = normalized_output.get("validation_flags", [])
    if flags:
        elements.append(Paragraph("<b>Validation Flags</b>", styles["Heading2"]))
        elements.append(Spacer(1, 0.1 * inch))
        for flag in flags:
            elements.append(Paragraph(f"• {flag}", styles["Normal"]))

    doc.build(elements)
    print(f"PDF saved to {filename}")
