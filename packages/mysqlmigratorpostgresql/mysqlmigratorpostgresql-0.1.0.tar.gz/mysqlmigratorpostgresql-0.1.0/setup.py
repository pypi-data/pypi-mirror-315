from setuptools import setup, find_packages

setup(
    name="mysqlmigratorpostgresql",
    version="0.1.0",
    description="A library to migrate MySQL databases to PostgreSQL with ease and automation.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="archenthusiastic",
    author_email="abuawadsantiago@gmail.com",
    url="https://github.com/archenthusiastic/mysqlmigratorpostgresql",
    project_urls={
        "Documentation": "https://github.com/archenthusiastic/mysqlmigratorpostgresql#readme",
        "Source": "https://github.com/archenthusiastic/mysqlmigratorpostgresql",
        "Tracker": "https://github.com/archenthusiastic/mysqlmigratorpostgresql/issues",
    },
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "mysql-connector-python",
        "psycopg2",
    ],
    keywords=["mysql", "postgresql", "database migration", "python"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Database",
    ],
    python_requires=">=3.7",
)
