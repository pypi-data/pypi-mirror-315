from setuptools import setup, find_packages

setup(
    name="sio_sso_lib",  # Nom de votre module
    version="0.1.3",  # Version initiale
    description="Librairie pour la gestion de l'authentification SSO en SIO",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Paul",
    author_email="contact@inoctet.fr",
    url="https://sso.inoctet.fr",  # Lien vers votre repo GitHub
    license="MIT",  # Type de licence
    packages=find_packages(),
    install_requires=[
        "requests",
        "numpy"
    ],  # Liste des dépendances dans requirements.txt
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)