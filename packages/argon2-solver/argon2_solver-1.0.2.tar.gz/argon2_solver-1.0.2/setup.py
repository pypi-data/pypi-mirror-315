from setuptools import setup, find_packages

setup(
    name="argon2-solver",
    version="1.0.2",
    author="Klez",
    author_email="klez@cock.li",
    description="A solver for Argon2-based challenges.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Klez2003/argon2-solver",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "argon2-solver=argon2_solver.main:main",
        ],
    },
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
