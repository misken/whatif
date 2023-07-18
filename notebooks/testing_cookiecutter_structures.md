Testing project folder structures
=================================

whatif_ccds
------------

Has src/ with code and __init__.py at root of src/
Has name='src' in setup.py

    pip install -e .
    
Ends up installing a package called src

In new_car_simulation notebook, had to change imports to do this:

    from src.whatif import Model
    from src.whatif import get_sim_results_df
    
Question: What happens if I change name in setup.py to whatif but
leave directory structure unchanged?

* Installs as whatif but is still only reachable with the `from src.whatif`.

whatif_ccds_aap
---------------

Has src/ with code and __init__.py in whatif/ subfolder of src/
Has name='whatif' in setup.py

    pip install -e .
    
Installs as whatif but still get `no module named 'whatif'`

Retried using 

    pip install .
    
and still get `no module named 'whatif'`

Hmm, seems like trouble finding the location of packages. I think we
need to help setup.py. See 

* https://hynek.me/articles/testing-packaging/
* https://docs.python.org/3/distutils/setupscript.html

    packages=find_packages("src"),
    package_dir={"": "src"},
    
Did 

    pip install .
    
The following works but need both whatifs

    from whatif.whatif import Model
    from whatif.whatif import get_sim_results_df
    
Ah, yes, this is where you can make life easier on the user by putting
import statements into the __init__.py file.

    from whatif.whatif import Model
    from whatif.whatif import get_sim_results_df
    
Since we installed this with pip, we can find out where it got installed to by

    import whatif
    whatif
    
    <module 'whatif' from '/home/mark/anaconda3/envs/whatif/lib/python3.9/site-packages/whatif/__init__.py'>
    
So, if we modify whatif in our src/whatif folder, the changes should NOT be accessible.
They aren't. But, what if I pip install it again. Will the autoreload work? YES! IT WORKS!

Now, what about a develop pip install?

	pip install -e .
	
After the install, this folder is created inside src/ and next to whatif/

    whatif.egg-info/
    
Yes, autoreload seems to kick in and I can make changes in src/whatif/whatif.py
that immediately are usable by the notebook without reinstalling.


