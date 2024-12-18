from setuptools import setup, find_packages
import os
import re


def get_version():
    version = None
    version_pattern = r'__version__ = ["\']([^"\']+)["\']'

    with open(
        os.path.join(os.path.dirname(__file__), "key_vault_interface", "__init__.py")
    ) as f:
        for line in f:
            match = re.search(version_pattern, line)
            if match:
                version = match.group(1)
                break

    if version is None:
        raise ValueError("Version not found in __init__.py")

    return version


setup(
    name="key-vault-interface",
    version=get_version(),
    packages=find_packages(),
    install_requires=[
        "azure-identity>=1.19.0",
        "azure-keyvault-secrets>=4.9.0",
        # "setuptools>=75.6.0",  # No need to list this unless absolutely needed for a package install
        "yarg>=0.1.9",
    ],
    extras_require={
        "dev": [
            "pytest>=8.3.4",  # For testing purposes
            "pipdeptree>=2.24.0",
        ],
        "docs": [
            "sphinx>=8.1.3",  # Documentation dependencies
            "docopt>=0.6.2",
            "ipython>=8.12.3",
            "nbconvert>=7.16.4",
        ],
    },
)
