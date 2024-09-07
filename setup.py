from setuptools import setup, find_packages


setup(
    name="swiss-notificator",
    version="0.1.0",
    author="Nazar Redko",
    author_email="rednaz1990@gmail.com",
    description="A versatile notification system",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/swiss-notificator",  # Your GitHub repository URL
    packages=find_packages(),  # Automatically discover all packages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Minimum Python version
    install_requires=[
        "requests",
        "skpy",
    ],
    include_package_data=True,  # If you need to include non-code files
)