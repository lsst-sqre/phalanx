from setuptools import setup
setup(
    name="multipathsecret",
    version="0.1.0",
    py_modules=['multipathsecret'],
    author='Adam Thornton',
    author_email='athornton@lsst.org',
    license="MIT",
    description="Rubin tool to add a secret to multiple Vault paths",
    install_requires=[
        'click',
        'hvac'
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
        "console_scripts": [
            "multisecret=multipathsecret.standalone:cli",
        ]
    }
)
