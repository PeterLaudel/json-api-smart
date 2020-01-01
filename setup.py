from setuptools import setup

setup(
    name="json-api-smart",
    version="",
    packages=["src"],
    url="",
    license="MIT",
    author="Nilsson",
    author_email="peter.laudel@gmail.com",
    description="",
    install_requires=["requests", "inflect", "typeguard"],
    extras_require={"dev": ["pytest", "requests_mock", "coverage", "mypy"]},
)
