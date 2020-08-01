from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name="json-api-smart",
    version="0.0.5",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
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
