import setuptools


def main() -> None:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

    setuptools.setup(
        name="xoa-core",
        description="Xena Open Automation framework for Xena test suite execution, integration, and development.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="Artem Constantinov, Leonard Yu",
        author_email="aco@xenanetworks.com, hyu@xenanewtorks.com",
        maintainer="Xena Networks",
        maintainer_email="support@xenanetworks.com",
        url="https://github.com/xenanetworks/open-automation-core",
        packages=setuptools.find_packages(),
        license='Apache 2.0',
        install_requires=["xoa_driver>=2.0", "pydantic==1.10.2", "semver", "oyaml",],
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Topic :: Software Development :: Libraries :: Application Frameworks",
            "License :: OSI Approved :: Apache Software License",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
        ],
        python_requires=">=3.8.9",
    )


if __name__ == '__main__':
    main()
