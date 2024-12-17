import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import f

class ChowTest:
    """
    A Python implementation of the Chow Test to check for structural breaks in regression models.
    """
    @staticmethod
    def chow_test(data, breakpoint, dependent_var, independent_vars):
        """
        Perform the Chow Test.

        Parameters:
            data (pd.DataFrame): The dataset containing dependent and independent variables.
            breakpoint (int): The row index at which to split the data into two subsets.
            dependent_var (str): The name of the dependent variable column.
            independent_vars (list of str): The names of the independent variable columns.

        Returns:
            dict: A dictionary containing the Chow test statistic and p-value.

        Raises:
            ValueError: If the inputs are invalid.
        """
        # Validate inputs
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Data must be a pandas DataFrame.")
        if not isinstance(breakpoint, int) or not (0 < breakpoint < len(data)):
            raise ValueError("Breakpoint must be an integer within the range of the dataset.")
        if dependent_var not in data.columns:
            raise ValueError(f"Dependent variable '{dependent_var}' not found in data.")
        if not all(var in data.columns for var in independent_vars):
            raise ValueError("Some independent variables are not in the data.")

        # Split data
        data1 = data.iloc[:breakpoint]
        data2 = data.iloc[breakpoint:]
        
        # Fit separate regressions
        X1 = sm.add_constant(data1[independent_vars])
        y1 = data1[dependent_var]
        model1 = sm.OLS(y1, X1).fit()
        
        X2 = sm.add_constant(data2[independent_vars])
        y2 = data2[dependent_var]
        model2 = sm.OLS(y2, X2).fit()
        
        # Fit combined regression
        X_combined = sm.add_constant(data[independent_vars])
        y_combined = data[dependent_var]
        model_combined = sm.OLS(y_combined, X_combined).fit()
        
        # Calculate residual sums of squares
        RSS1 = model1.ssr
        RSS2 = model2.ssr
        RSS_combined = model_combined.ssr
        
        # Degrees of freedom
        k = len(X_combined.columns)  # Number of parameters including intercept
        N1 = len(data1)
        N2 = len(data2)
        N_total = N1 + N2
        
        # Compute Chow test statistic
        chow_stat = ((RSS_combined - (RSS1 + RSS2)) / k) / ((RSS1 + RSS2) / (N_total - 2 * k))
        p_value = 1 - f.cdf(chow_stat, dfn=k, dfd=(N_total - 2 * k))
        
        return {
            "Chow Test Statistic": chow_stat,
            "P-value": p_value
        }
