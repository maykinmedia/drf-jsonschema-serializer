import io
from setuptools import setup, find_packages

long_description = '\n'.join((
    io.open('README.rst', encoding='utf-8').read(),
))

setup(
    name='drf_jsonschema',
    version='0.1.dev0',
    description="JSON Schema support for Django REST Framework",
    long_description=long_description,
    author="ISProjects",
    author_email="support@isprojects.nl",
    license="BSD",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.5',
    ],
    install_requires=[
        'setuptools',
        'djangorestframework',
        'django',
        'jsonschema',
        'rfc3987',
        'strict-rfc3339'
    ],
    extras_require=dict(
        test=[
            'pytest >= 2.9.0',
            'pytest-remove-stale-bytecode',
            'pytest-django'
        ],
        pep8=[
            'flake8',
        ],
        coverage=[
            'pytest-cov',
        ],
        docs=[
            'sphinx',
        ],
    ),
)
