from setuptools import setup, find_packages

setup(
    name="CTkSimpleMessagebox",  # Name des Pakets
    version="1.1.6",  # Version des Pakets
    packages=find_packages(),  # Automatische Paketfindung
    include_package_data=True,  # Einbinden zusätzlicher Dateien (aus MANIFEST.in)
    package_data={
        "src": ["resources/ErrorIcon.ico"],
        "src": ["resources/InfoIcon.ico"]
    },
    install_requires=[],  # Abhängigkeiten hier auflisten
    author="Scott",
    description="A simple Messagebox for Customtkinter.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/NotScottt/CTkSimpleMessageboxes",  # Link zu deinem Repository
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
