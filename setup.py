from setuptools import setup

setup(
    name='liquidemocracy',
    packages=['liquidemocracy'],
    include_package_data=True,
    python_requires='~=3.5.2',
    install_requires=[
        'flask', 'flask_cors', 'flask_jwt_simple', 'flask-mongoengine',
        'pytest-flask', 'python-dateutil', 'requests', 'beautifulsoup4',
        'nltk', 'numpy', 'scipy', 'pandas', 'scikit-learn', 'slate',
        'gunicorn',
        ],
)
