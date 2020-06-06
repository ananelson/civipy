from setuptools import setup, find_packages

setup(
        author='Ana Nelson',
        author_email='ana@ananelson.com',
        classifiers=[
            "License :: OSI Approved :: GPLv3 License"
            ],
        description='CiviCRM v3 REST API Python wrapper',
        entry_points = {
            },
        include_package_data = True,
        install_requires = [
            'requests',
            ],
        name='civipy',
        packages=find_packages(),
        version="0.0.1"
        )
