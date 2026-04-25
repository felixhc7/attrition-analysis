import pandas as pd
from src.metrics import (
    attrition_rate,
    attrition_by_department,
    attrition_by_overtime,
    average_income_by_attrition,
    satisfaction_summary,
)


# --- attrition_rate ---

def test_attrition_rate_returns_expected_percent():
    df = pd.DataFrame(
        {
            "employee_id": [1, 2, 3, 4],
            "department": ["Sales", "Sales", "HR", "HR"],
            "attrition": ["Yes", "No", "No", "Yes"],
        }
    )
    assert attrition_rate(df) == 50.0


def test_attrition_rate_no_leavers():
    df = pd.DataFrame({"employee_id": [1, 2], "attrition": ["No", "No"]})
    assert attrition_rate(df) == 0.0


def test_attrition_rate_all_leavers():
    df = pd.DataFrame({"employee_id": [1, 2], "attrition": ["Yes", "Yes"]})
    assert attrition_rate(df) == 100.0


# --- attrition_by_department ---

def test_attrition_by_department_returns_expected_columns():
    df = pd.DataFrame(
        {
            "employee_id": [1, 2, 3, 4],
            "department": ["Sales", "Sales", "HR", "HR"],
            "attrition": ["Yes", "No", "No", "Yes"],
        }
    )
    result = attrition_by_department(df)
    assert list(result.columns) == ["department", "employees", "leavers", "attrition_rate"]


def test_attrition_by_department_values():
    df = pd.DataFrame(
        {
            "employee_id": [1, 2, 3, 4, 5],
            "department": ["Sales", "Sales", "HR", "HR", "HR"],
            "attrition": ["Yes", "Yes", "Yes", "No", "No"],
        }
    )
    result = attrition_by_department(df)
    sales = result[result["department"] == "Sales"].iloc[0]
    hr = result[result["department"] == "HR"].iloc[0]
    assert sales["employees"] == 2
    assert sales["leavers"] == 2
    assert sales["attrition_rate"] == 100.0
    assert hr["employees"] == 3
    assert hr["leavers"] == 1
    assert hr["attrition_rate"] == 33.33


def test_attrition_by_department_sorted_descending():
    df = pd.DataFrame(
        {
            "employee_id": [1, 2, 3, 4, 5],
            "department": ["Sales", "Sales", "HR", "HR", "HR"],
            "attrition": ["Yes", "Yes", "Yes", "No", "No"],
        }
    )
    result = attrition_by_department(df)
    rates = list(result["attrition_rate"])
    assert rates == sorted(rates, reverse=True)


# --- attrition_by_overtime ---

def test_attrition_by_overtime_columns():
    df = pd.DataFrame(
        {
            "employee_id": [1, 2, 3, 4],
            "overtime": ["Yes", "Yes", "No", "No"],
            "attrition": ["Yes", "Yes", "No", "No"],
        }
    )
    result = attrition_by_overtime(df)
    assert list(result.columns) == ["overtime", "employees", "leavers", "attrition_rate"]


def test_attrition_by_overtime_values():
    df = pd.DataFrame(
        {
            "employee_id": [1, 2, 3, 4],
            "overtime": ["Yes", "Yes", "No", "No"],
            "attrition": ["Yes", "Yes", "No", "No"],
        }
    )
    result = attrition_by_overtime(df)
    yes_row = result[result["overtime"] == "Yes"].iloc[0]
    no_row = result[result["overtime"] == "No"].iloc[0]
    assert yes_row["employees"] == 2
    assert yes_row["leavers"] == 2
    assert yes_row["attrition_rate"] == 100.0
    assert no_row["employees"] == 2
    assert no_row["leavers"] == 0
    assert no_row["attrition_rate"] == 0.0


# --- average_income_by_attrition ---

def test_average_income_by_attrition_columns():
    df = pd.DataFrame({"attrition": ["Yes", "No"], "monthly_income": [4000.0, 8000.0]})
    result = average_income_by_attrition(df)
    assert list(result.columns) == ["attrition", "avg_monthly_income"]


def test_average_income_by_attrition_values():
    df = pd.DataFrame(
        {
            "attrition": ["Yes", "Yes", "No", "No"],
            "monthly_income": [3000.0, 5000.0, 7000.0, 9000.0],
        }
    )
    result = average_income_by_attrition(df)
    yes_income = result[result["attrition"] == "Yes"]["avg_monthly_income"].iloc[0]
    no_income = result[result["attrition"] == "No"]["avg_monthly_income"].iloc[0]
    assert yes_income == 4000.0
    assert no_income == 8000.0


# --- satisfaction_summary ---

def test_satisfaction_summary_columns():
    df = pd.DataFrame(
        {
            "employee_id": [1, 2, 3],
            "job_satisfaction": [1, 2, 3],
            "attrition": ["Yes", "No", "No"],
        }
    )
    result = satisfaction_summary(df)
    assert list(result.columns) == ["job_satisfaction", "total_employees", "leavers", "attrition_rate"]


def test_satisfaction_summary_attrition_rate_uses_group_total():
    # Verifies the rate is leavers/group-employees, not leavers/all-leavers.
    # Group 1: 2 employees, 2 leavers → 100%. Group 2: 3 employees, 1 leaver → 33.33%.
    df = pd.DataFrame(
        {
            "employee_id": [1, 2, 3, 4, 5],
            "job_satisfaction": [1, 1, 2, 2, 2],
            "attrition": ["Yes", "Yes", "Yes", "No", "No"],
        }
    )
    result = satisfaction_summary(df)
    row1 = result[result["job_satisfaction"] == 1].iloc[0]
    row2 = result[result["job_satisfaction"] == 2].iloc[0]
    assert row1["attrition_rate"] == 100.0
    assert row2["attrition_rate"] == 33.33


def test_satisfaction_summary_sorted_ascending():
    df = pd.DataFrame(
        {
            "employee_id": [1, 2, 3, 4],
            "job_satisfaction": [3, 1, 4, 2],
            "attrition": ["Yes", "No", "Yes", "No"],
        }
    )
    result = satisfaction_summary(df)
    assert list(result["job_satisfaction"]) == sorted(result["job_satisfaction"])
