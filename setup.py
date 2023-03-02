import setuptools


setuptools.setup(
    name="py-confluent-cli",
    version="0.9.4",
    author="Pawel Dudzinski",
    author_email="pawel.dudzinski@saucelabs.com",
    description="Simple Python library wrapping the Confluent Cloud CLI v2",
    long_description="Simple Python library wrapping the Confluent Cloud CLI v2",
    long_description_content_type="text/markdown",
    url="https://github.com/saucelabs/py-confluent",
    py_modules=["confluent"],
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
    ],
    install_requires=[
        "executor==23.2"
    ]
 )
