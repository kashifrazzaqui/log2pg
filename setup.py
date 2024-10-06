from setuptools import setup, find_packages

setup(
    name="log2pg",
    version="0.1.0",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "psycopg2-binary",
    ],
    extras_require={
        "dev": ["pytest", "httpx"],
    },
)