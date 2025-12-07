from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()
setup(
    name="jira-analytics-tool",
    version="2.0.0",
    author="Sev Oren",
    author_email="your.email@example.com",
    description="Advanced JIRA Analytics Tool for task analysis with 6 types of visualizations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sev-oren/jira-analytics-tool",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Office/Business :: Scheduling",
        "Topic :: Software Development :: Bug Tracking",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "jira-analytics=src.main:main",
            "jira-analytics-gui=src.gui:main [GUI]",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["config/*.yaml", "config/*.yml", "scripts/*.bat", "scripts/*.sh"],
    },
    data_files=[
        ("config", ["config/config.yaml"]),
        ("scripts", ["scripts/run_windows.bat", "scripts/run_linux.sh"]),
    ],
    keywords="jira analytics visualization report dashboard",
    project_urls={
        "Bug Reports": "https://github.com/sev-oren/jira-analytics-tool/issues",
        "Source": "https://github.com/sev-oren/jira-analytics-tool",
        "Documentation": "https://github.com/sev-oren/jira-analytics-tool/wiki",
    },
)
