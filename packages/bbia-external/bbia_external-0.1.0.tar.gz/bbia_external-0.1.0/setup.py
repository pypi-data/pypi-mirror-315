from setuptools import find_packages, setup

setup(
    name="bbia-external",
    version="0.1.0",
    description="Assistente virtual da BBoom",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "cachetools>=5.5.0",
        "langchain-community>=0.3.7",
        "langchain-groq>=0.2.1",
        "langchain-huggingface>=0.1.2",
        "langchain-pinecone>=0.2.0",
        "langserve[all]>=0.3.0",
        "pinecone-notebooks>=0.1.1",
        "pydantic-settings>=2.6.1",
    ],
)
