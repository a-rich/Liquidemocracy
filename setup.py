from setuptools import setup

#TODO: figure out how to override PyPi installation of Slate in favore of this
# forked version that doesn't have the relative import error:
#    https://github.com/alkivi-sas/slate/tree/python3

setup(
    name='liquidemocracy',
    packages=['liquidemocracy'],
    include_package_data=True,
    python_requires='~=3.5.2',
    install_requires=[
        'flask', 'flask_cors', 'flask_jwt_simple', 'flask-mongoengine',
        'pytest-flask', 'python-dateutil', 'requests', 'beautifulsoup4',
        'numpy', 'scipy', 'pandas', 'scikit-learn', 'slate', 'gunicorn',
        ],
)
