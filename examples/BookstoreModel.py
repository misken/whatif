import numpy as np

from whatif import Model

class BookstoreModel(Model):
    """Bookstore model

    This example is based on the "Walton Bookstore" problem in *Business Analytics: Data Analysis and Decision Making* (Albright and Winston) in the chapter on Monte-Carlo simulation. Here's the basic problem (with a few modifications):

    * we have to place an order for a perishable product (e.g. a calendar),
    * there's a known unit cost for each one ordered,
    * we have a known selling price,
    * demand is uncertain but we can model it with some simple probability distribution,
    * for each unsold item, we can get a partial refund of our unit cost,
    * we need to select the order quantity for our one order for the year; orders can only be in multiples of 25.

    Attributes
    ----------
    unit_cost: float or array-like of float, optional
        Cost for each item ordered (default 7.50)
    selling_price : float or array-like of float, optional
        Selling price for each item (default 10.00)
    unit_refund : float or array-like of float, optional
        For each unsold item we receive a refund in this amount (default 2.50)
    order_quantity : float or array-like of float, optional
        Number of items ordered in the one time we get to order (default 200)
    demand : float or array-like of float, optional
        Number of items demanded by customers (default 193)
    """
    def __init__(self, unit_cost=7.50, selling_price=10.00, unit_refund=2.50,
                 order_quantity=200, demand=193):
        self.unit_cost = unit_cost
        self.selling_price = selling_price
        self.unit_refund = unit_refund
        self.order_quantity = order_quantity
        self.demand = demand

    def order_cost(self):
        """Compute total order cost"""
        return self.unit_cost * self.order_quantity

    def num_sold(self):
        """Compute number of items sold

        Assumes demand in excess of order quantity is lost.
        """
        return np.minimum(self.order_quantity, self.demand)

    def sales_revenue(self):
        """Compute total sales revenue based on number sold and selling price"""
        return self.num_sold() * self.selling_price

    def num_unsold(self):
        """Compute number of items ordered but not sold

        Demand was less than order quantity
        """
        return np.maximum(0, self.order_quantity - self.demand)

    def refund_revenue(self):
        """Compute total sales revenue based on number unsold and unit refund"""
        return self.num_unsold()  * self.unit_refund

    def total_revenue(self):
        """Compute total revenue from sales and refunds"""
        return self.sales_revenue() + self.refund_revenue()

    def profit(self):
        """Compute profit based on revenue and cost"""
        profit = self.sales_revenue() + self.refund_revenue() - self.order_cost()
        return profit