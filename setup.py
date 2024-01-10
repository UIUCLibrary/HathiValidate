import os


from setuptools import setup


setup(
    packages=[
        'hathi_validate',
        'hathi_validate.xsd',
    ],
    package_data={'hathi_validate':["xsd/*.xsd", "py.typed"]},
    test_suite="tests",
    install_requires=[
        "lxml<5.1.0; sys_platform == 'darwin' and python_version == '3.8' and platform_machine == 'arm64'",
        "lxml; sys_platform != 'darwin' or python_version != '3.8' or platform_machine != 'arm64'",
        "PyYAML",
        'importlib_resources;python_version<"3.9"',
                      ],
    tests_require=['pytest'],
    entry_points={
                 'console_scripts': ['hathivalidate=hathi_validate.cli:main']
             },
)
