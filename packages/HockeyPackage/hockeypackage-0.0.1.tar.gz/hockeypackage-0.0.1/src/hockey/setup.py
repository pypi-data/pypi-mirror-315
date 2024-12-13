#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from setuptools import setup, find_packages

setup(
    name='hockey',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['Team2024.csv'], ['Team2023.csv'], ['Team2022.csv'], ['Team2021.csv'], ['Team2020.csv'],
    },
    install_requires=[
        'pandas', 
    ],
)

