from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pkg_platzi_final",
    version="0.3.0",
    author="odelgado",
    author_email="odelgadoo@gmail.com",
    description="Un sistema básico de gestión de reservas en Python",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Indica que el README está en formato Markdown
    url="https://github.com/Odelgadoo/pkg_platzi_final",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)