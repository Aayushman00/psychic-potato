from setuptools import setup, find_packages
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text(encoding="utf-8")

setup(
    name="piano-keyboard-optimizer",
    version="0.1.0",
    description="Optimise piano-to-keyboard mapping using QAP with biomechanical and perceptual models",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Your Name",
    packages=find_packages(include=["src", "src.*"]),
    package_dir={"": "."},
    python_requires=">=3.8",
    install_requires=[
        "numpy",
        "scipy",
        "matplotlib",
    ],
    entry_points={
        "console_scripts": [
            "piano-keyboard-opt=src.cli.main:main",
        ],
    },
)