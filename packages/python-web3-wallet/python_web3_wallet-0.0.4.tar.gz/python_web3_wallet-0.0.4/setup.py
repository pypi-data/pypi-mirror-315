from pathlib import Path

import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="python_web3_wallet",
    version="0.0.4",
    author="Gnosis AI",
    author_email="ai@gnosis.io",
    description="Streamlit component that allows users to connect a wallet and send transactions with dynamic recipients and amounts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.7",
    install_requires=[
        "streamlit >= 1.0",
    ],
    extras_require={
        "devel": [
            "wheel",
        ]
    }
)
