from datetime import datetime
from pathlib import Path


REPORTS_DIR = Path("reports")
SCREENSHOTS_DIR = REPORTS_DIR / "screenshots"


def generate_reports(results):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

    html_file = REPORTS_DIR / f"test_report_{timestamp}.html"

    total = len(results)
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = total - passed

    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Automation Report</title>
    <style>
        body {{
            font-family: Arial;
            background: #0f172a;
            color: white;
            padding: 20px;
        }}

        .summary {{
            display: flex;
            gap: 20px;
            margin-bottom: 30px;
        }}

        .card {{
            background: #1e293b;
            padding: 20px;
            border-radius: 10px;
            width: 200px;
            text-align: center;
        }}

        .pass {{ color: #22c55e; }}
        .fail {{ color: #ef4444; }}

        table {{
            width: 100%;
            border-collapse: collapse;
            background: #1e293b;
            border-radius: 10px;
        }}

        th, td {{
            padding: 12px;
            border-bottom: 1px solid #334155;
        }}

        th {{
            background: #020617;
        }}

        .PASS {{ color: #22c55e; font-weight: bold; }}
        .FAIL {{ color: #ef4444; font-weight: bold; }}

        img {{
            width: 200px;
            border-radius: 8px;
        }}
    </style>
</head>

<body>

<h1>🚀 Automation Test Report</h1>
<p>Generated: {datetime.now()}</p>

<div class="summary">
    <div class="card">
        <h3>Total</h3>
        <p>{total}</p>
    </div>
    <div class="card">
        <h3 class="pass">Passed</h3>
        <p>{passed}</p>
    </div>
    <div class="card">
        <h3 class="fail">Failed</h3>
        <p>{failed}</p>
    </div>
</div>

<table>
<tr>
    <th>Test</th>
    <th>Status</th>
    <th>Description</th>
    <th>Time (s)</th>
    <th>Screenshot</th>
</tr>
"""

    # ADD ROWS
    for r in results:
        screenshot_html = "-"

        if r.get("status") == "FAIL" and r.get("screenshot"):
            screenshot_html = f'<a href="{r["screenshot"]}" target="_blank"><img src="{r["screenshot"]}"></a>'

        html += f"""
<tr>
    <td>{r['name']}</td>
    <td class="{r['status']}">{r['status']}</td>
    <td>{r['description']}</td>
    <td>{r['time']}</td>
    <td>{screenshot_html}</td>
</tr>
"""

    # CLOSE HTML
    html += """
</table>

</body>
</html>
"""

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n🔥 Report generated: {html_file}")