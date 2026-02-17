from setuptools import setup, find_packages

setup(
    name="Topsis_102317186_Kashish",
    version="0.1",
    packages=find_packages(),
    install_requires=["numpy", "pandas"],
    entry_points={
        "console_scripts": [
            "topsis=topsis.topsis:main"
        ]
    },
    author="Kashish",
    description="TOPSIS implementation using Python",
)