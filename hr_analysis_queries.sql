-- ============================================================================
-- HR Employee Attrition Analysis — SQL Queries
-- Author: Neha Tiwari
-- Database: hr_analytics  |  Table: employees
-- Purpose: Business-driven queries to support HR leadership reporting
-- ============================================================================

-- ── Q1: Overall attrition summary ────────────────────────────────────────────
-- What is the overall attrition rate and headcount split?
SELECT
    COUNT(*)                                             AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)  AS employees_left,
    SUM(CASE WHEN Attrition = 'No'  THEN 1 ELSE 0 END)  AS employees_stayed,
    ROUND(
        100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2
    )                                                    AS attrition_rate_pct
FROM employees;


-- ── Q2: Attrition rate by department ─────────────────────────────────────────
-- Which departments have the highest attrition risk?
SELECT
    Department,
    COUNT(*)                                             AS total,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)  AS left_count,
    ROUND(
        100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2
    )                                                    AS attrition_rate_pct
FROM employees
GROUP BY Department
ORDER BY attrition_rate_pct DESC;


-- ── Q3: Attrition by Job Level ────────────────────────────────────────────────
-- Are entry-level employees leaving more than senior employees?
SELECT
    JobLevel,
    COUNT(*)                                             AS total,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)  AS left_count,
    ROUND(
        100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2
    )                                                    AS attrition_rate_pct
FROM employees
GROUP BY JobLevel
ORDER BY JobLevel ASC;


-- ── Q4: OverTime and its impact on attrition ─────────────────────────────────
-- Is mandatory overtime driving employees to quit?
SELECT
    OverTime,
    COUNT(*)                                             AS total,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)  AS left_count,
    ROUND(
        100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2
    )                                                    AS attrition_rate_pct
FROM employees
GROUP BY OverTime
ORDER BY attrition_rate_pct DESC;


-- ── Q5: Average compensation — attrited vs retained employees ─────────────────
-- Is there a meaningful salary gap between who stayed and who left?
SELECT
    Attrition,
    ROUND(AVG(MonthlyIncome), 0)    AS avg_monthly_income,
    ROUND(AVG(PercentSalaryHike), 1) AS avg_salary_hike_pct,
    ROUND(AVG(DailyRate), 0)         AS avg_daily_rate
FROM employees
GROUP BY Attrition;


-- ── Q6: High-risk employee segment ───────────────────────────────────────────
-- Identify employees with multiple attrition risk factors
-- (Entry level + OverTime + Low income + Single)
SELECT
    EmployeeNumber,
    Age,
    Department,
    JobRole,
    JobLevel,
    OverTime,
    MonthlyIncome,
    MaritalStatus,
    YearsAtCompany,
    JobSatisfaction
FROM employees
WHERE
    Attrition = 'No'                -- Still with the company
    AND JobLevel = 1                 -- Entry level
    AND OverTime = 'Yes'            -- Working overtime
    AND MonthlyIncome < 3000         -- Low income band
    AND MaritalStatus = 'Single'     -- No financial anchors
ORDER BY MonthlyIncome ASC;


-- ── Q7: Attrition by age group ────────────────────────────────────────────────
-- Which age brackets are most vulnerable?
SELECT
    CASE
        WHEN Age BETWEEN 18 AND 25 THEN '18–25'
        WHEN Age BETWEEN 26 AND 35 THEN '26–35'
        WHEN Age BETWEEN 36 AND 45 THEN '36–45'
        ELSE '46–60'
    END                                                  AS age_group,
    COUNT(*)                                             AS total,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)  AS left_count,
    ROUND(
        100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2
    )                                                    AS attrition_rate_pct
FROM employees
GROUP BY age_group
ORDER BY attrition_rate_pct DESC;


-- ── Q8: Job satisfaction vs attrition ────────────────────────────────────────
-- Are dissatisfied employees actually leaving at higher rates?
SELECT
    JobSatisfaction,
    CASE JobSatisfaction
        WHEN 1 THEN 'Low'
        WHEN 2 THEN 'Medium'
        WHEN 3 THEN 'High'
        WHEN 4 THEN 'Very High'
    END                                                  AS satisfaction_label,
    COUNT(*)                                             AS total,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)  AS left_count,
    ROUND(
        100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2
    )                                                    AS attrition_rate_pct
FROM employees
GROUP BY JobSatisfaction
ORDER BY attrition_rate_pct DESC;


-- ── Q9: Top Job Roles by headcount lost ──────────────────────────────────────
-- Which specific roles are losing the most people in absolute numbers?
SELECT
    JobRole,
    COUNT(*)                                             AS total_in_role,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)  AS employees_lost,
    ROUND(
        100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2
    )                                                    AS attrition_rate_pct
FROM employees
GROUP BY JobRole
ORDER BY employees_lost DESC;


-- ── Q10: Tenure and attrition — are new joiners leaving early? ───────────────
-- Retention analysis by years at company (critical for onboarding strategy)
SELECT
    CASE
        WHEN YearsAtCompany <= 1  THEN '0–1 years'
        WHEN YearsAtCompany <= 3  THEN '2–3 years'
        WHEN YearsAtCompany <= 5  THEN '4–5 years'
        WHEN YearsAtCompany <= 10 THEN '6–10 years'
        ELSE '10+ years'
    END                                                  AS tenure_band,
    COUNT(*)                                             AS total,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)  AS left_count,
    ROUND(
        100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2
    )                                                    AS attrition_rate_pct
FROM employees
GROUP BY tenure_band
ORDER BY
    CASE tenure_band
        WHEN '0–1 years'  THEN 1
        WHEN '2–3 years'  THEN 2
        WHEN '4–5 years'  THEN 3
        WHEN '6–10 years' THEN 4
        ELSE 5
    END;
