# TArK Data Checks

This is a set of pytests that can be run over the TArK db to ensure that there is internal consistency within the database.

# Requirements
1. Python 3.6+
2. MySQL Client libraries

# Installation

```
pyenv virtualenv 3.6.5 tarkDC
pyenv activate tarkDB

git clone https://github.com/Ensembl/tark-dc.git
cd tark-dc
pip install .
```

# Running Tests
1. Create a database configuration file called `crd.json`:
```
{
    "user": "example_username"
    "password": "example_pswd",
    "host": "mysql-tark-db",
    "port": "3306",
    "db": "tark_v1"
}
```
2. Run the following command:
```
pytest
```

