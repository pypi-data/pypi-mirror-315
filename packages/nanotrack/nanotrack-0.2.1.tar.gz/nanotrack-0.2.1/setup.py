from setuptools import setup, find_packages
from pathlib import Path

HERE = Path(__file__).parent
README = (HERE / "README.md").read_text(encoding="utf-8")

setup(
    name="nanotrack",
    version="0.2.1",  # Bumped version
    author="RAGUL T, KARTHICK RAJA E",
    author_email="tragulragul@gmail.com, e.karthickraja2004@gmail.com",
    maintainer="RAGUL T",
    description="A lightweight object detection and tracking package ",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ragultv/NanoTrack",  # Your GitHub URL
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.18.0",
        "opencv-python>=4.5.0",
        "torch>=1.7.0",
        "torchvision>=0.8.0",
        "scipy>=1.5.0",
        # Add new dependencies here
    ],
    extras_require={
        "dev": ["pytest>=6.0", "flake8>=3.8"],  # Optional dev dependencies
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Multimedia :: Video",
    ],
    keywords="object detection tracking kalman-filter lightweight",
    project_urls={
        "Documentation": "https://github.com/ragultv/NanoTrack/blob/main/README.md",
        "Source": "https://github.com/ragultv/NanoTrack",
        "Bug Tracker": "https://github.com/ragultv/NanoTrack/issues",
    },
)

