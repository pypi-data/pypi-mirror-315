from setuptools import setup, find_packages

setup(
    name="kiss-ai-stack-core",
    version="0.1.0-alpha4",
    description="KISS AI Stack's AI Agent Builder - Simplify AI Agent Development",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="KISS AI Stack, Lahiru Pathirage",
    license="MIT",
    python_requires='>=3.12',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "PyYAML~=6.0.2",
        "pydantic~=2.10.1",
        "fastapi~=0.115.5",
        "unstructured~=0.16.8",
        "tiktoken~=0.8.0",
        "pandas~=2.2.3",
        "unstructured[xlsx]",
        "unstructured[pdf]",
        "unstructured[docx]",
        "unstructured[csv]"
    ],
    keywords=["ai", "agent", "machine-learning", "llm", "document-processing"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ],
    project_urls={
        "Homepage": "https://github.com/kiss-ai-stack",
        "Repository": "https://github.com/kiss-ai-stack",
        "Documentation": "https://github.com/kiss-ai-stack/kiss-ai-stack-core/main/README.md"
    }
)
