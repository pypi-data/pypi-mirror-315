from setuptools import setup, find_packages

setup(
    name="enhanced-http",
    version="1.0.0",
    description="A lightweight, production-ready asynchronous HTTP client.",
    long_description=open("README.md", encoding="utf-8").read(),  # Specify UTF-8 encoding
    long_description_content_type="text/markdown",
    author="Dean Goss",
    author_email="dgoss@treytek.com",
    url="https://github.com/Treytek/enhanced_http",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Internet :: WWW/HTTP",
    ],
    python_requires=">=3.7",
    install_requires=[],  # Add dependencies here
    extras_require={
        "dev": ["pytest", "pytest-asyncio", "pytest-xdist"],
    },
    keywords=["http client", "websocket", "asyncio", "middleware", "caching"],
    project_urls={
        "Source": "https://github.com/Treytek/enhanced-http",  # Update this
        "Tracker": "https://github.com/Treytek/enhanced-http/issues",  # Update this
    },
)

