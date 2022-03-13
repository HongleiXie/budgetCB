from pathlib import Path

from setuptools import find_packages, setup

long_description = Path("README.md").read_text()

setup(
    name="budgetcb",
    version="0.0.0",
    description="Constrained Contextual Bandits for Personalized Recommendation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    url="https://github.com/HongleiXie/budgetCB",
    packages=find_packages(exclude=["tests"]),
    package_data={
        "": ["py.typed"],
    },
    install_requires=[],
    extras_require={
        "dev": [
            "black==21.7b0",
            "isort==5.9.3",
            "flake8==3.9.2",
            "flake8-annotations==2.6.2",
            "flake8-colors==0.1.9",
            "pre-commit==2.14.0",
            "pytest==6.2.4",
            "numpy==1.21.0",
            "joblib==1.0.1",
            "scipy==1.8.0",
            "matplotlib==3.5.1",
            "scikit-learn==1.0.2",
        ]
    },
)