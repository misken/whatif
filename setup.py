from setuptools import find_packages, setup

setup(
    name='whatif',
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=['numpy', 'pandas'],
    version='0.1.0',
    description='What if analysis in Python',
    author='misken',
    license='MIT',
)
