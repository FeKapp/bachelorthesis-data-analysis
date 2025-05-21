import pandas as pd
import numpy as np

# Analyze the percentage of negative returns in a dataset of S&P 500 and risk-free rate (one month treasury bills)

filename = "data/returns/historical/rf_95-19.csv"
output_file = "data/returns/results/results-rf_95-19.txt"
date_col = "dateff"
return_col = "rf"

df = pd.read_csv(filename, parse_dates=[date_col], dayfirst=True)

df = df.sort_values(date_col).set_index(date_col)

# Define monthly negative percentages (based on 'b5ret')
total_months = len(df)
negative_months = df[df[return_col] < 0].shape[0]
pct_negative_months = (negative_months / total_months) * 100

# For compounding returns in quarter, year, 5-year
df["1_plus_r"] = 1 + df[return_col]

# Quarterly negative %
quarterly_returns = df["1_plus_r"].resample("Q").prod().copy() - 1
print(quarterly_returns)
negative_quarters = (quarterly_returns < 0).sum()
total_quarters = len(quarterly_returns)
pct_negative_quarters = (negative_quarters / total_quarters) * 100

# Yearly negative %
yearly_returns = df["1_plus_r"].resample("Y").prod().copy() - 1
negative_years = (yearly_returns < 0).sum()
total_years = len(yearly_returns)
pct_negative_years = (negative_years / total_years) * 100

# Every 5 years negative %
fiveyr_returns = df["1_plus_r"].resample("5A").prod().copy() - 1
print(fiveyr_returns)
negative_5yrs = (fiveyr_returns < 0).sum()
total_5yrs = len(fiveyr_returns)
pct_negative_5yrs = (negative_5yrs / total_5yrs) * 100

# Mean and standard deviation of monthly returns
mean_monthly = df[return_col].mean()  # decimal form
std_monthly = df[return_col].std()    # decimal form

# Annualized mean and std
mean_annual_arith = 12 * mean_monthly
mean_annual_geom = (1 + mean_monthly)**12 - 1
std_annual = std_monthly * np.sqrt(12)

# Prepare results for printing (in percentage form, two decimals)
results_str = [
    f"Percentage of months with negative returns:        {pct_negative_months:.2f}%",
    f"Percentage of quarters with negative returns:      {pct_negative_quarters:.2f}%",
    f"Percentage of years with negative returns:         {pct_negative_years:.2f}%",
    f"Percentage of 5-year periods with negative returns:{pct_negative_5yrs:.2f}%",
    "",
    f"Mean monthly return:         {mean_monthly*100:.2f}%",
    f"Std dev monthly returns:     {std_monthly*100:.2f}%",
    f"Annualized mean (arith):     {mean_annual_arith*100:.2f}%",
    f"Annualized mean (geom):      {mean_annual_geom*100:.2f}%",
    f"Annualized std dev:          {std_annual*100:.2f}%"
]

# Print to console
for line in results_str:
    print(line)

# Write results to a text file
with open(output_file, "w") as f:
    for line in results_str:
        f.write(line + "\n")