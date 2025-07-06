from setuptools import setup,find_packages

with open('requirement.txt', 'r', encoding='utf-8') as f:
    requirement =  f.read().split('\n')

    
setup(
    name='mypackage',
    version='0.0.1',
    packages=find_packages(include=["scraping*"]),
    install_requires=requirement,
    entry_points={
        'console_scripts': [
            'wiki_scrape = scraping.main:default',
        ]
    }
)