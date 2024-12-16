from setuptools import setup, find_packages
import os

# خواندن محتوای فایل README.md
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="microjwt",  
    version="0.1.0",  
    description="A simple HMAC-based JWT implementation for MicroPython",
    long_description=long_description,  # اضافه کردن محتوای README
    long_description_content_type="text/markdown",  # مشخص کردن فرمت Markdown
    author="Arman Ghobadi",  
    author_email="arman.ghobadi.ag@gmai.com",  
    url="https://github.com/armanghobadi/microjwt",  
    packages=find_packages(),  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  
)
