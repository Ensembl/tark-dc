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

## pytest mark: versioning

Alll the following tests can be run with the following command:

```
pytest -m versioning
```

### Stable ID and version matching unique sequence checksums

- Module: `tests/test_versioning.py`
- Test: `test_ver_asm_seq_conflicts`

The purpose of this test is to ensure that sequences that are matched to a given stable_id and version number and assembly number are unique. The reason the assembly number has also been included is that there are some stable ID - Version numbers that are the same between releases, but there is a minor change in the respective sequences.

## pytest mark: stats

Alll the following tests can be run with the following command:

```
pytest -m stats
```

### Feature count consistency

- Module: `tests/test_stats.py`
- Test: `test_load_stats`

Once each release for a source has been loaded into the Tark db the pipeline should leave a record of the number of features that it has loaded along with a count of the number of features that are present in the source. This test ensures that the number of features that are reported match those that are present within the db for a given release.
