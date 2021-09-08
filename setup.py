import os


from setuptools import setup


setup(
    packages=[
        'hathi_validate',
        'hathi_validate.xsd',
    ],
    package_data={'hathi_validate':["xsd/*.xsd", "py.typed"]},
    test_suite="tests",
    setup_requires=['pytest-runner'],
    install_requires=[
        "lxml",
        "PyYAML",
        'importlib_resources;python_version<"3.9"',
                      ],
    tests_require=['pytest'],

    entry_points={
                 'console_scripts': ['hathivalidate=hathi_validate.cli:main']
             },
)
