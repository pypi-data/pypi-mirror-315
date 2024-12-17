from setuptools import setup, find_packages

setup(
    name="pkg_platzi_final",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # Lista de dependencias
    ],
    author="odelgadoo",
    author_email="odelgadoo@gmail.com",
    description="Este paquete implementa un ejemplo de un sistema básico de gestión de reservas en Python.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/Odelgadoo/pkg_platzi_final",
        classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10'
    
)