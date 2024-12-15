from setuptools import setup, find_packages

setup(
    name="kusho-capture",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    extras_require={
        "fastapi": ["fastapi>=0.65.0"],
        "flask": ["flask>=2.0.0"],
        "django": ["django>=3.2"],
    },
    python_requires=">=3.7",
    author="KushoAI",
    author_email="support@kusho.co",
    description="HTTP traffic capture middleware for Python web applications",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kusho-co/kusho-capture",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Framework :: FastAPI",
        "Framework :: Flask",
        "Framework :: Django",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="http, middleware, traffic capture, api testing, monitoring, debugging",
)