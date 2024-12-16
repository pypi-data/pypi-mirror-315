from setuptools import setup, find_packages

setup(
    name='newnowlib',
    version='0.1.0',
    author='NewNow Group Data Science Team',
    description='NEWNOW Data Analysis Library',
    url='https://github.com/newnowgroup/newnow_library',
    license='MIT',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=['numpy', 'pandas', 'tqdm', 'scikit-learn', 'plotly', 'matplotlib', 'seaborn'],
)