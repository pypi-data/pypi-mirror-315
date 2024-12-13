from setuptools import setup, find_packages

setup(
    name='liver_disease_classifier',
    version='0.1.0',
    description='Library for liver disease prediction using various machine learning models',
    author='Sentongo Muhsin',
    packages=find_packages(),
    license='MIT',
    keywords=['Liver Disease classification'],
    install_requires=[
        'pandas',
        'scikit-learn',
        'imbalanced-learn',
        'scipy',
        'numpy'
    ],
)
