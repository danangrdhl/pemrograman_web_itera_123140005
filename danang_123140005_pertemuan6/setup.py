import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requires = [
    'plaster_pastedeploy',
    'pyramid',
    'pyramid_jinja2',
    'pyramid_tm',
    'pyramid_retry',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    'alembic',
    'psycopg2-binary',
]

tests_require = [
    'WebTest',
    'pytest',
]

setup(
    name='pyramid_mahasiswa',
    version='0.0',
    description='Aplikasi RESTful API Manajemen Mahasiswa dan Matakuliah',
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='Danang Ridho Laksono',
    author_email='danang.123140005@student.itera.ac.id',
    url='',
    keywords='web pyramid pylons rest api sqlalchemy alembic postgresql',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': tests_require,
    },
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = pyramid_mahasiswa:main',
        ],
        'console_scripts': [
            'initialize_pyramid_mahasiswa_db=pyramid_mahasiswa.scripts.initialize_db:main',
        ],
    },
)
