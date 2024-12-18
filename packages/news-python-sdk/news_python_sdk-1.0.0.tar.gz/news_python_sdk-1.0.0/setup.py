from setuptools import setup, find_packages

setup(
    name="news-python-sdk",  # Replace with your package name
    version='1.0.0',
    description="News API v3 Python SDK test",
    author="Your Name",
    author_email="your-email@example.com",
    packages=find_packages(where="src/python"),
    package_dir={"": "src/python"},
    python_requires=">=3.7",
)
