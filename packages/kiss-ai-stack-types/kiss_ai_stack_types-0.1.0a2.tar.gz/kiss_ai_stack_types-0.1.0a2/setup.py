from setuptools import setup, find_packages

setup(
    name="kiss-ai-stack-types",
    version="0.1.0-alpha2",
    description="KISS AI Stack's object types",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="KISS AI Stack, Lahiru Pathirage",
    license="MIT",
    python_requires='>=3.12',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "pydantic~=2.10.3"
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
        "Documentation": "https://github.com/kiss-ai-stack/kiss-ai-stack-types/main/README.md"
    }
)
