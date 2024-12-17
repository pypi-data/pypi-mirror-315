from setuptools import setup, find_packages

setup(
    name="rvcapture",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "certifi==2024.8.30",
        "charset-normalizer==3.4.0",
        "click==8.1.7",
        "colorama==0.4.6",
        "halo==0.0.31",
        "idna==3.10",
        "log-symbols==0.0.14",
        "markdown-it-py==3.0.0",
        "mdurl==0.1.2",
        "pyfiglet==1.0.2",
        "Pygments==2.18.0",
        "requests==2.32.3",
        "rich==13.9.4",
        "shellingham==1.5.4",
        "six==1.16.0",
        "spinners==0.0.24",
        "tabulate==0.9.0",
        "termcolor==2.5.0",
        "typer==0.13.1",
        "typing_extensions==4.12.2",
        "urllib3==2.2.3",
    ],
    entry_points={
        "console_scripts": [
            "rvcapture=RVCapture.main:app",
        ],
    },
    author="Roojh Health",
    author_email="roojh@roojh.com",
    description="A CLI tool for RVCapture",
    url="https://roojh.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    include_package_data=True,
    package_data={
        "RVCapture": ["appConfigs.json"],
    },
)
