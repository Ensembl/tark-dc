"""
.. See the NOTICE file distributed with this work for additional information
   regarding copyright ownership.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

Config setting for pytest
"""

import json
import pytest
import MySQLdb


@pytest.fixture(scope='module')
def credentials():
    """
    Fixture to extract the user credentials for logging into the Tark database.

    Requires that there is a crd.json file in the root directory of the module.

    Returns
    -------
    crd : dict
        Dictionary object of the user, password, host, port and db
    """
    with open('crd.json') as file_handle:
        crd = json.loads(file_handle.read())
    yield crd


@pytest.fixture(scope='module')
def cnxn(credentials):  # pylint: disable=redefined-outer-name
    """
    Fixture creates a connection for the period of testing, automatically
    closing the connection upon completion of the tests.

    Parameters
    ----------
    credentials : dict

    Returns
    -------
    cnxn : MySQLdb.connect object
    """
    cnxn = MySQLdb.connect(  # pylint: disable=redefined-outer-name
        user=credentials['user'],
        passwd=credentials['password'],
        host=credentials['host'],
        port=credentials['port'],
        database=credentials['db']
    )
    yield cnxn
    cnxn.close()


@pytest.fixture
def cursor(cnxn):  # pylint: disable=redefined-outer-name
    """
    Fixture to create a cursor for use by tests to access the Tark db

    Parameters
    ----------
    cnxn : MySQLdb.connect object
    """
    cursor = cnxn.cursor()  # pylint: disable=redefined-outer-name
    yield cursor
    cnxn.rollback()
