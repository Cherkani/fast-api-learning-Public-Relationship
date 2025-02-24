from setuptools import setup, find_packages

setup(
    name="api_resto",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
    ],
    extras_require={
        'test': [
            'pytest',
            'pytest-cov',
            'httpx'
        ],
    },
)
