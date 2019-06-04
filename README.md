# Tark Data Checks

This is a set of pytests that can be run over the Tark db to ensure that there is internal consistency within the database.

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


# Tests

## Stable ID and version matching unique sequence checksums

- Module: `tests/test_versioning.py`
- Test: `test_ver_asm_seq_conflicts`

The purpose of this test is to ensure that sequences that are matched to a given stable_id and version number and assembly number are unique. The reason the assembly number has also been included is that there are some stable ID - Version numbers that are the same between releases, but there is a minor change in the respective sequences.
