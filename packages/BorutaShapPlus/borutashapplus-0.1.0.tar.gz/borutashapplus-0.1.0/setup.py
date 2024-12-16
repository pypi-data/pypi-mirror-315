from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name="BorutaShapPlus",
    version="0.1.0",
    description="An updated version of the SHAP-based Boruta feature selection algorithm with some new feature.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/AbhishekKaps/Boruta-Shap",
    author="Eoghan Keany",
    author_email="egnkeany@gmail.com",
    maintainer="Abhishek Kapoor",
    maintainer_email="abhishek.kaps001@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    py_modules = ["BorutaShap"],
    package_dir = {"" : "src"},
    install_requires=["scikit-learn","tqdm",
                      "statsmodels","matplotlib",
                      "pandas","numpy>=2.0.0","shap>=0.34.0","seaborn",
                      "scipy"],
    project_urls={
        "Original Repository": "https://github.com/Ekeany/Boruta-Shap",
        "Fork Repository": "https://github.com/AbhishekKaps/Boruta-Shap",
    },
)
