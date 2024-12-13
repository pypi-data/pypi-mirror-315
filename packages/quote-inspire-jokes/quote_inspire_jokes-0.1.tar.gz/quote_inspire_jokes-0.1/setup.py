from setuptools import setup, find_packages

setup(
    name="quote_inspire_jokes",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'requests',  # We'll use the requests library for HTTP calls
    ],
    entry_points={
        'console_scripts': [
            'quote_inspire_jokes=quote_inspire_jokes.__main__:main',
        ],
    },
    description="A Python module to fetch quotes, inspiring quotes, and jokes from APIs",
    author="Shaik Muneer",
    url="https://github.com/francefaraz/far_quotes_python_module"
)