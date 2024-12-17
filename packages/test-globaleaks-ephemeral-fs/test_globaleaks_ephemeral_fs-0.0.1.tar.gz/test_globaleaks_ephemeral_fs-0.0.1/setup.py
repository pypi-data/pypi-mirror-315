from setuptools import setup

setup(
    name="test-globaleaks-ephemeral-fs",  # Your package name
    version="0.0.1",  # Version number
    description="An ephemeral, encrypted filesystem implementation using fusepy and cryptography suitable for whistleblowing applications",
    author="Giovanni Pellerano",
    author_email="giovanni.pellerano@globaleaks.org",
    license="AGPL-3.0-or-later",
    install_requires=["cryptography", "fusepy"],
    entry_points={
        "console_scripts": [
            "globaleaks-ephemeral-fs=globaleaks_ephemeral_fs:main",  # If you have a main entry point in the mount module
        ],
    },
    python_requires='>=3.6',  # Minimum Python version required,
    project_urls={
        'Homepage': 'https://github.com/globaleaks/globaleaks-ephemeral-fs',
        'Issues': 'https://github.com/globaleaks/globaleaks-ephemeral-fs'
    },
)
