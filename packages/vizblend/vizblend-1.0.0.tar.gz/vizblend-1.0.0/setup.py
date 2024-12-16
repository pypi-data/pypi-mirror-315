from setuptools import setup, find_packages

setup(
    name="vizblend",
    version="1.0.0",
    author="Mahmoud Housam",
    author_email="mahmoudhousam60@gmail.com",
    description="A Python package to generate HTML reports from Plotly figures using Jinja2 templates.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MahmoudHousam/VizBlend",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "plotly==5.24.1",
        "black==24.10.0",
        "pytest==8.3.4",
        "pandas==2.2.3",
        "jinja2==3.1.4",
        "bs4==0.0.2",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    python_requires=">=3.9",
)
