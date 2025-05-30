# rwanda_paye_calculator/setup.py
from setuptools import setup, find_packages
setup(
    name="rwanda_paye_calculator",
    version="0.1.0",
    author="viella",
    author_email="iradukundavierra4@gmail.com",
    description="A standalone PAYE calculator for Rwandan workers, supporting monthly and annual calculations with custom deductions.",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[],  # add dependencies if needed
    entry_points={
        'console_scripts': [
            'rwanda-paye=rwanda_paye_calculator.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)