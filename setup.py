from setuptools import setup

setup(
    name="json-api-smart",
    version="0.0.1b",
    packages=["src"],
    url="",
    license="MIT",
    author="Nilsson",
    author_email="peter.laudel@gmail.com",
    description="Is your client library which support ths JSON:API standard.",
    install_requires=["requests", "inflect", "typeguard"],
    extras_require={"dev": ["pytest", "requests_mock", "coverage", "mypy"]},
    keywords="json:api api json rest resources",
    url="https://github.com/NilssonPL/json-api-smart",
)
