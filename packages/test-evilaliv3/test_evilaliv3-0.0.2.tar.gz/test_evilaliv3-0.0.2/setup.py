from setuptools import setup, find_packages

setup(
    name="test-evilaliv3",  # Your package name
    version="0.0.2",  # Version number
    description="Ephemeral file system with secure temporary file handling",
    author="Giovanni Pellerano",
    author_email="giovanni.pellerano@globaleaks.org",
    license="AGPL-3.0-or-later",
    install_requires=["cryptography", "fusepy"],
    test_suite="tests",  # The directory for your tests
    tests_require=[
        "unittest",  # If you’re using unittest, this is the dependency
    ],
    entry_points={
        "console_scripts": [
            "mount-ephemeral-fs=globaleaks_ephemeral_fs.mount_ephemeral_fs:main",  # If you have a main entry point in the mount module
        ],
    },
    python_requires='>=3.6',  # Minimum Python version required,
    project_urls={
        'Homepage': 'https://github.com/globaleaks/globaleaks_ephemeral_fs',
        'Issues': 'https://github.com/globaleaks/globaleaks_ephemeral_fs'
    },
)
