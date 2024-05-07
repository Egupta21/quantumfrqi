#setup.py

from setuptools import setup, find_packages

setup(
    name="quantumfrqi",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "qiskit==0.46.0",
        "numpy==1.24.4",
        "Pillow==9.0.1",
        "openpyxl==3.1.2",
        "matplotlib==3.8.0",
        "pandas==2.1.3",
        "scikit-image==0.19.2",
        "scikit-learn==1.3.2",
        "qiskit-aer==0.14.1"
    ],
    author="Eashan",
    author_email="eashan@vt.edu",
    description="Import images to automatically convert to Quantum format using FRQI",
    keywords="Quantum Image Processing, FRQI",
    url="http://example.com/QuantumImageProcessing",  # Optional project URL
    test_suite='tests'  # This assumes your tests are in a directory called "tests"
)