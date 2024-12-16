from setuptools import setup, find_packages

setup(
    name="standalone-naman1607vyas",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "langchain",
        "openai",
        "sentence-transformers",
        "faiss-cpu",
        "datasets",
        "numpy",
    ],
    entry_points={
        "console_scripts": [
            "standalone=standalone.main:main",
        ],
    },
)
