-- 1. Total Companies
SELECT COUNT(*) FROM companies;

-- 2. Top 10 Companies by Market Cap
SELECT company_id, market_cap
FROM market_cap
ORDER BY market_cap DESC
LIMIT 10;

-- 3. Highest Sales in 2024
SELECT company_id, sales
FROM profitandloss
WHERE year=2024
ORDER BY sales DESC
LIMIT 10;

-- 4. Companies with Negative Net Profit
SELECT company_id, year, net_profit
FROM profitandloss
WHERE net_profit < 0;

-- 5. Average ROE
SELECT AVG(roe_percentage)
FROM companies;

-- 6. Companies with Highest EPS
SELECT company_id, year, eps
FROM profitandloss
ORDER BY eps DESC
LIMIT 10;

-- 7. Latest Stock Prices
SELECT company_id, date, close_price
FROM stock_prices
ORDER BY date DESC
LIMIT 20;

-- 8. Number of Documents per Company
SELECT company_id, COUNT(*)
FROM documents
GROUP BY company_id
ORDER BY COUNT(*) DESC;

-- 9. Companies in Each Sector
SELECT sector, COUNT(*)
FROM sectors
GROUP BY sector;

-- 10. Financial Ratios Available
SELECT company_id, COUNT(*)
FROM financial_ratios
GROUP BY company_id
ORDER BY COUNT(*) DESC;