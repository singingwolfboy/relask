from setuptools import setup

requirements = [
    'Flask-SQLAlchemy',
    'relask>=0.1.0',
]

setup(
    name='relasksa',
    version='0.1.0',
    description="A Relask demo with SQLAlchemy",
    author="Fantix King",
    author_email='fantix.king@gmail.com',
    url='https://github.com/decentfox/relask',
    packages=[
        'relasksa',
    ],
    install_requires=requirements,
    license="BSD license",
    zip_safe=False,
    keywords='relask',
)
