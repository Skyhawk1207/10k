from setuptools import setup, find_packages

setup(
    name='ten_thousand_hours',           # Package name
    version='0.1.0',                     # Initial version
    author='Skyhawk1207',                
    description='TUI tool to track practice hours towards 10k hours of mastery',
    py_modules=['tenK'],                  # Single-module project
    install_requires=[
        'mysql-connector-python',        # MySQL Connector
    ],
    entry_points={
        'console_scripts': [
            # Installs 'tenk-hours' command to run the script
            'tenk-hours=tenK:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
