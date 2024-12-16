from setuptools import setup, find_packages

setup(
    name="kiss-ai-stack-client",
    version="0.1.0-alpha2",
    description="KISS AI Stack's Python Client SDK - Simplify AI Agent Development",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="KISS AI Stack Python SDK, Lahiru Pathirage",
    license="MIT",
    python_requires='>=3.12',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "requests~=2.32.3",
        "websockets~=14.1",
        "httpx~=0.28.0",
        "kiss-ai-stack-types~=0.1.0a2"
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
