# whatif - Do Excel style what if? analysis in Python

The whatif package helps you build business analysis oriented models in Python that you might normally build in Excel. 
Specifically, whatif includes functions that are similar to Excel's Data Tables and Goal Seek for doing
sensitivity analysis and "backsolving" (e.g. finding a breakeven point). It also includes functions
for facilitating Monte-Carlo simulation using these models.

Related blog posts

* [Part 1: Models and Data Tables](https://bitsofanalytics.org/posts/what-if-1-model-datatable/what_if_1_model_datatable.html)
* [Part 2: Goal Seek](https://bitsofanalytics.org/posts/what-if-2-goal-seek/what_if_2_goalseek.html)
* [Part 3: Monte-carlo simulation](https://bitsofanalytics.org/posts/what-if-3-simulation/what_if_3_simulation.html)
* [Part 4: Project structure and packaging](https://bitsofanalytics.org/posts/what-if-4-project-packaging/what_if_4_project_packaging.html)

This package is also developed as part of [one of the courses I teach](http://www.sba.oakland.edu/faculty/isken/courses/mis6900/index.html). You can find the course web pages at:

* [Submodule 1: What if analysis with Python](http://www.sba.oakland.edu/faculty/isken/courses/mis6900/mod3a_whatif.html)
* [Submodule 2: Creating the whatif package](http://www.sba.oakland.edu/faculty/isken/courses/mis6900/mod3b_whatif_packaging.html)
* [Submodule 3: Using Python to wrangle Excel files](http://www.sba.oakland.edu/faculty/isken/courses/mis6900/mod3c_python_excel.html)

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

See the materials in the blog posts and course webs listed above. 

License
-------

The project is licensed under the MIT license.
