from setuptools import setup, find_packages

setup(
    name='bigquery_duckdb_toolkit',
    version='1.0.3',
    packages=find_packages(),
    install_requires=[
        'db-dtypes',
        'ipython',
        'google-auth',
        'google-cloud-bigquery',
        'pandas',
        'tabulate',
        'duckdb',
        'jinja2'
    ],
    author='Tiago Navarro',
    author_email='tiagornavarro@gmail.com',
    description='Toolkit para consultas e manipulação de dados no BigQuery com integração com DuckDB.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ResultadosDigitais/bigquery_duckdb_toolkit',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development :: Libraries",
        "Topic :: Scientific/Engineering :: Information Analysis"
    ],
    python_requires='>=3.8',
)
