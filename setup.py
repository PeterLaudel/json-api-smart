from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name="json-api-smart",
    version="0.0.3b",
    packages=["src"],
    url="https://github.com/NilssonPL/json-api-smart",
    license="MIT",
    author="Nilsson",
    author_email="peter.laudel@gmail.com",
    description="Is your client library which support ths JSON:API standard.",
    long_description=long_description,
    long_description_content_type='text/markdown',  # This is important!
    install_requires=["requests", "inflect", "typeguard"],
    extras_require={"dev": ["pytest", "requests_mock", "coverage", "mypy"]},
    keywords="json:api api json rest resources",
)
