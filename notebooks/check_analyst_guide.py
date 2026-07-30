from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
import os


output = "docs/analyst_guide.pdf"


os.makedirs("docs", exist_ok=True)


doc = SimpleDocTemplate(output)


styles = getSampleStyleSheet()

story = []


sections = [

(
"1. Project Overview",
"""
N100 Financial Intelligence Platform is a financial analytics system built
for analysing 92 Nifty 100 companies.

The platform provides:
- Financial KPI analysis
- Investment screening
- Peer comparison
- Sector analysis
- Company profile analytics
- Automated PDF tearsheets

The system uses ETL pipelines, SQLite database,
FastAPI backend and Streamlit dashboard.
"""
),

(
"2. System Architecture",
"""
The platform consists of four major layers:

1. Data Layer:
Stores financial statements, ratios, market data and company information.

2. Analytics Layer:
Calculates KPIs such as ROE, ROCE, CAGR,
Debt Equity ratio and quality scores.

3. API Layer:
FastAPI exposes financial data through REST endpoints.

4. Dashboard Layer:
Streamlit provides analyst-friendly visualization.
"""
),

(
"3. Setting Up The Project",
"""
Steps:

1. Activate virtual environment.

2. Install requirements.

3. Load financial datasets.

4. Run ETL pipeline.

5. Start API server.

6. Start Streamlit dashboard.
"""
),

(
"4. Using The Screener",
"""
The screener allows analysts to filter companies based on:

- ROE
- ROCE
- Debt levels
- Quality score
- Growth metrics

Users can select filters and export results as CSV.
"""
),

(
"5. Dashboard Navigation",
"""
The dashboard contains:

Company Explorer:
View individual company information.

Screener:
Filter investment opportunities.

Peer Analysis:
Compare companies against industry peers.

Sector Dashboard:
Analyse sector-level trends.
"""
),

(
"6. Company Profile Screen",
"""
The company profile displays:

- Latest financial metrics
- Profit and loss history
- Balance sheet information
- Cash flow trends
- Financial ratios
- Peer comparison
"""
),

(
"7. PDF Tearsheet Generation",
"""
The platform generates automated analyst tearsheets.

Each tearsheet contains:

- Company overview
- Financial charts
- KPI summary
- Quality indicators
- Investment insights

Generated files are stored inside:

reports/tearsheets/
"""
),

(
"8. API Usage",
"""
FastAPI provides REST endpoints.

Example:

GET /api/v1/companies/TCS

Returns company information.

GET /api/v1/screener

Returns screening results.

Health check:

GET /api/v1/health
"""
),

(
"9. Troubleshooting",
"""
Common issues:

Database not found:
Check database path in settings.

API connection error:
Ensure FastAPI server is running.

Dashboard loading error:
Verify API endpoint availability.
"""
),

(
"10. Analyst Workflow",
"""
Recommended workflow:

1. Open dashboard.
2. Select sector/company.
3. Analyse KPIs.
4. Compare peers.
5. Run screener.
6. Export results.
7. Generate tearsheet.
"""
)

]


for title, body in sections:

    story.append(
        Paragraph(title, styles["Heading2"])
    )

    story.append(
        Paragraph(body.replace("\n","<br/>"), styles["BodyText"])
    )

    story.append(Spacer(1,20))

    story.append(PageBreak())


doc.build(story)


print("Created:", output)