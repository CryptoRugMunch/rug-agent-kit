from setuptools import setup, find_packages

setup(
    name="rug-munch-agentkit",
    version="1.0.0",
    description="Rug Munch Intelligence plugin for Coinbase AgentKit — add rug pull detection to any trading agent",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Rug Munch Intelligence",
    author_email="dev@cryptorugmunch.app",
    url="https://github.com/CryptoRugMunch/rug-agent-kit",
    packages=find_packages(),
    install_requires=[
        "coinbase-agentkit>=0.2.0",
        "requests>=2.31.0",
        "pydantic>=2.0.0",
    ],
    python_requires=">=3.10",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries",
    ],
)
