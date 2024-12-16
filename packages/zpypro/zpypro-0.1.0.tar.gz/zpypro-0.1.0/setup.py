from setuptools import setup, find_packages

setup(
    name="zpypro",
    version="0.1.0",
    description="A python project template.",
    long_description_content_type="text/markdown",  # README format (Markdown)
    author="You Zhou",
    author_email="zhouyou.xy@gmail.com",
    url="https://github.com/you-zhou/zpypro",
    packages=find_packages(),  # Automatically find packages in the project
    include_package_data=True,  # Include non-code files specified in MANIFEST.in
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python version
    install_requires=[],  # Add dependencies here (or use requirements.txt)
    entry_points={
        "console_scripts": [
            "zpypro=zpypro.main:main",  # Enables running `pypro` from the command line
        ]
    },
)
