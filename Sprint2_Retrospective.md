# Sprint 2 Retrospective

## Project
N100 Financial Intelligence Platform

## Sprint Duration
Sprint 2

---

# Sprint Objective

The objective of Sprint 2 was to design and implement the complete financial ratio engine for the N100 Financial Intelligence Platform. This included profitability, leverage, efficiency, cash flow, CAGR analytics, manual validation of computed ratios, and documentation of financial data edge cases.

---

# Completed Features

## Profitability Ratios

- Return on Equity (ROE)
- Return on Capital Employed (ROCE)
- Return on Assets (ROA)
- Net Profit Margin
- Operating Profit Margin

---

## Leverage Ratios

- Debt to Equity
- Interest Coverage Ratio
- Total Debt

---

## Efficiency Ratios

- Asset Turnover Ratio

---

## Cash Flow KPIs

- Free Cash Flow
- Cash from Operations
- CapEx Intensity
- FCF Conversion
- Capital Allocation Classification

---

## Growth Metrics

- Revenue CAGR (5 Year)
- PAT CAGR (5 Year)
- EPS CAGR (5 Year)

The CAGR engine includes handling for edge cases such as missing historical values, zero base values, negative values, and insufficient financial history.

---

## Financial Ratio Engine

Successfully generated and populated the `financial_ratios` table containing:

- Profitability KPIs
- Leverage KPIs
- Efficiency KPIs
- Cash Flow KPIs
- Growth KPIs
- Composite Quality Score

for all available company-year records.

---

# Manual Verification

Manual verification was completed for the following companies:

- ABB
- TCS
- RELIANCE

The following metrics were verified manually using spreadsheet calculations:

- Return on Equity (ROE)
- Revenue CAGR (5 Year)

Observed differences between manual calculations and database values were within the acceptable tolerance of **0.1%**.

---

# Formula Decisions

The following formulas were finalized during Sprint 2:

### Return on Equity

ROE = Net Profit ÷ (Equity Capital + Reserves)

### Return on Capital Employed

ROCE = EBIT ÷ Capital Employed

### Debt to Equity

Debt to Equity = Total Borrowings ÷ Shareholders' Equity

### Asset Turnover

Asset Turnover = Sales ÷ Total Assets

### Free Cash Flow

Free Cash Flow = Operating Cash Flow − Capital Expenditure

### Revenue CAGR

Revenue CAGR = ((Current Revenue ÷ Revenue 5 Years Ago)^(1/5) − 1) × 100

---

# Edge Case Review

The following edge cases were identified and documented:

- Source ROE values inconsistent for certain companies (e.g., TCS)
- ROCE values differing from source reports due to reporting period differences
- Extremely high ROE/ROCE values caused by very small denominator values
- Banking and Financial Services companies requiring special leverage treatment
- Missing historical financial records affecting CAGR computation
- Duplicate financial statement records for selected companies

All identified issues were documented in:

`data/output/ratio_edge_cases.log`

---

# Challenges Faced

- Duplicate company-year records in financial statements
- Missing historical values required for CAGR computation
- Inconsistent source financial ratios
- Multiple reporting versions across datasets
- Financial sector companies requiring different leverage interpretation

---

# Key Learnings

- Financial ratios should always be validated using manual calculations.
- Source datasets can contain inconsistencies and outdated values.
- Edge case handling significantly improves the reliability of financial analytics.
- Proper documentation of anomalies is essential for maintaining data quality.
- Manual verification provides confidence in analytical outputs.

---

# Deliverables Completed

- Financial Ratio Engine
- CAGR Engine
- Cash Flow KPI Engine
- Composite Quality Score
- Capital Allocation Classification
- Financial Ratio SQLite Table
- Manual ROE Verification
- Manual Revenue CAGR Verification
- Ratio Edge Case Log

---

# Sprint Outcome

Sprint 2 successfully delivered a production-ready financial analytics engine capable of computing, validating, and documenting key financial KPIs across the N100 company universe. All major analytical modules, manual verification activities, and edge case documentation were completed, providing a strong foundation for the stock screener and subsequent analytics features.