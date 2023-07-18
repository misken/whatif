import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from numpy.random import default_rng

# Numpy financial functions have been removed to their own package
# See https://numpy.org/numpy-financial/
import numpy_financial as npf

from whatif import Model
from whatif import get_sim_results_df


class NewCarModel(Model):
    """New car model

    This example is based on one in the textbook
    [Business Analytics: Data Analysis and Decision Making (Albright and Winston)
    This example is in Section 16.3 in the 7th edition. Here's the basic problem (with a few modifications):

    * we are developing a new car,
    * there's a fixed development cost,
    * we have estimated a unit margin per car which decays at a known rate each year,
    * demand in the first year is uncertain and we will model it with a triangular distribution,
    * demand in years 2 through 5 are based on the previous years demand and a decay rate modeled with another triangular distribution,
    * depreciation is modeled using the straight line method and theirs a known fixed tax rate.

    Attributes
    ----------
    fixed_dev_cost: float, optional
        Development cost (default 600e+6)
    base_margin : float, optional
        Unit margin in year 1 (default 4e+3)
    annual_margin_decr : float, optional
        Fractional annual decrease in unit margin (default 0.04)
    yr1_demand : float, optional
        Number of items ordered in the one time we get to order (default 53560.0)
    demand_decr : float or array-like of float, optional
        Fractional annual decrease in demand (default 0.077)
    tax_rate : float or array-like of float, optional
        Tax rate (default 0.21)
    discount_rate : float, optional
        Used for NPV calculation (default 0.07)
    num_years : int, optional
        Number of years in the model (default 5)
    """

    def __init__(self, fixed_dev_cost=600e+6, base_margin=4e+3, annual_margin_decr=0.04,
                 yr1_demand=53560, demand_decr=0.077,
                 tax_rate=0.21, discount_rate=0.07, num_years=5
                 ):

        self.fixed_dev_cost = fixed_dev_cost
        self.base_margin = base_margin
        self.annual_margin_decr = annual_margin_decr

        self.yr1_demand = yr1_demand
        self.demand_decr = demand_decr

        self.tax_rate = tax_rate
        self.discount_rate = discount_rate
        self.num_years = num_years

    def sales(self):
        """Sales by year

        Depends on random base value in year 0 which is then modified by a percent decay rate that may
        vary by year.
        """

        # Scalar to range (consider creating function for this)
        if np.isscalar(self.demand_decr):
            self.demand_decr = np.full((1, self.num_years - 1), self.demand_decr)

        # Year 1 demand
        # This is the key to multi-period models - how to best do this?
        if np.isscalar(self.yr1_demand):
            sales_array = np.zeros((1, self.num_years))
        else:
            sales_array = np.zeros((len(self.yr1_demand), self.num_years))

        sales_array[:, 0] = self.yr1_demand

        # Compute sales in subsequent years
        for t in range(1, self.num_years):
            sales_array[:, t] = (1 - self.demand_decr[:, t - 1]) * sales_array[:, t - 1]

        return sales_array

    def unit_contribution(self):
        """Unit contribution by year

        Depends on random base value in year 0 which is then modified by a fixed percent decay rate.
        """

        _unit_contribution = np.array([self.base_margin * (1 - self.annual_margin_decr) ** n
                                       for n in range(self.num_years)])

        return _unit_contribution

    def net_revenue(self):
        """Net revenue by year

        Sales multiplied by unit_contribution for each year
        """

        _net_revenue = self.sales() * self.unit_contribution()
        return _net_revenue

    def depreciation(self):
        """Depreciation by year

        Assumes straight line depreciation
        """

        _depreciation = np.full(self.num_years, self.fixed_dev_cost / self.num_years)
        return _depreciation

    def before_tax_profit(self):
        """Before tax profit by year

        Net revenue minus depreciation
        """

        _before_tax_profit = self.net_revenue() - self.depreciation()
        return _before_tax_profit

    def after_tax_profit(self):
        """After tax profit by year

        Before tax profit after taxes removed
        """
        _after_tax_profit = self.before_tax_profit() * (1 - self.tax_rate)
        return _after_tax_profit

    def cash_flow(self):
        """Cash flow by year

        After tax profit plus depreciation
        """
        _cash_flow = self.after_tax_profit() + self.depreciation()
        return _cash_flow

    def npv(self):
        """NPV of cash flow adjusted for initial investment

        The `numpy_financial.npv()` function wants the initial investment as a
        negative cash flow in year 1 or a zero cash flow in year 1 and then need to
        subtract off the initial investment.
        """

        cash_flow = self.cash_flow()
        # If more than one row in cash_flow, we must be simulating or creating a
        # data table.
        n_rows = cash_flow.shape[0]

        # Create an (nrows x 1) array filled with initial investment values
        col0 = np.full(nrows, -self.fixed_dev_cost)
        col0 = col0.reshape((nrows, 1))

        # Insert the initial investment at start of cash flow stream
        adj_cash_flow = np.concatenate((col0, self.cash_flow()), axis=1)

        # Compute npv for each row of cash flow streams
        _npv = np.array([npf.npv(self.discount_rate, adj_cash_flow[i, :]) for i in range(nrows)])

        return _npv

    def model_to_df(self, transpose=True):
        """Create DataFrame version of financial model table

        Financial model table is transposed so that financial measures are columns.
        """
        X = np.vstack([self.sales(), self.unit_contribution(),
                       self.net_revenue(), self.depreciation(),
                       self.before_tax_profit(), self.after_tax_profit(), self.cash_flow()])

        if transpose:
            X = np.transpose(X)
            df = pd.DataFrame(X, columns=['sales', 'unit_contribution', 'net_revenue',
                                          'depreciation', 'before_tax_profit', 'after_tax_profit',
                                          'cash_flow'])
        else:
            df = pd.DataFrame(X, index=['sales', 'unit_contribution', 'net_revenue',
                                        'depreciation', 'before_tax_profit', 'after_tax_profit',
                                        'cash_flow'])

        return df


model_default = NewCarModel()
print(model_default.sales())
print(model_default.model_to_df())
