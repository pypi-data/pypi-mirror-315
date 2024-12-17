from setuptools import setup, find_packages

setup(
    name="pixelpalette",
    version="1.0.0",
    description="A package to extract dominant colors from images and represent them in RGB, Hex, and HSL formats.",
    author="Parth Dudhatra",
    author_email="imparth.dev@gmail.com",
    url="https://github.com/imparth7/pixelpalette",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Graphics",
        "Intended Audience :: Developers",
        "Natural Language :: English",
    ],
    packages=find_packages(),
    install_requires=[
        "numpy",
        "matplotlib",
        "scikit-learn",
    ],
    python_requires=">=3.6",
    keywords=[
        "color extraction",
        "image processing",
        "dominant colors",
        "RGB to Hex",
        "RGB to HSL"
        "color palettes",
        "image analysis",
    ],
    platforms="Any",
    project_urls={
        "Bug Tracker": "https://github.com/imparth7/pixelpalette/issues",
        "Source Code": "https://github.com/imparth7/pixelpalette",
    },
)
