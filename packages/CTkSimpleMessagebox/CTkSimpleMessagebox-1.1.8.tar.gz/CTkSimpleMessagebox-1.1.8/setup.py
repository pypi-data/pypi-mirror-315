from setuptools import setup, find_packages

setup(
    name="CTkSimpleMessagebox", 
    version="1.1.8",  
    packages=find_packages(), 
    include_package_data=True,  
    install_requires=[],  
    author="Scott",
    description="A simple Messagebox for Customtkinter.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/NotScottt/CTkSimpleMessageboxes", 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
