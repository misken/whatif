# whatif - Do Excel style what if? analysis in Python

The whatif package helps you build business analysis oriented models in Python that you might normally build in Excel. 
Specifically, whatif includes functions that are similar to Excel's Data Tables and Goal Seek for doing
sensitivity analysis and "backsolving" (e.g. finding a breakeven point). It also includes functions
for facilitating Monte-Carlo simulation using these models.

Related blog posts

* [Part 1: Models and Data Tables](http://hselab.org/excel-to-python-1-models-datatables.html)
* [Part 2: Goal Seek](http://hselab.org/excel-to-python-2-goalseek.html)
* [Part 3: Monte-carlo simulation](http://hselab.org/excel-to-python-3-simulation.html)

## Features

The whatif package is new and quite small. It contains:

* a base ``Model`` class that can be subclassed to create new models
* Functions for doing data tables (``data_table``) and goal seek (``goal_seek``) on a models
* Functions for doing Monte-Carlo simulation with a model (``simulate``)

## Installation

Clone the whatif project from GitHub:

.. code::

    git clone https://github.com/misken/whatif.git

and then you can install it locally by running
the following from the project directory.

.. code::

	cd whatif
    pip install .
	
Getting started
---------------

See the [Getting started with whatif](TODO) page in the docs.

License
-------

The project is licensed under the MIT license.