from setuptools import setup, find_packages

setup(
    name="easy_tree_maker",
    version="0.1.6",
    author="Mahrez BENHAMAD",
    author_email="contact@mahrezbenhamad.com",
    description="A tool to create a directory and file structure from JSON or Python object",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MahrezBH/easy_tree_maker",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'easy_tree_maker=easy_tree_maker.cli:main'
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
