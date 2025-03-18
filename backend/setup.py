from setuptools import setup, find_packages

setup(
    name="lifeflow",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "sqlalchemy",
        "alembic",
        "cryptography",
        "pydantic",
        "uvicorn",
    ],
) 