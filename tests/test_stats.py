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
"""

from __future__ import print_function

import json
import pytest


@pytest.mark.stats
def test_load_stats(cursor):
    """
    Test to ensure that the logged numbers for the genes and transcripts within
    a release match between those loaded, those stated to be loaded and those
    described as being present in the original database

    .. code-block:: none
       pytest -m stats
    """
    sql = """
        SELECT
            rst.description,
            rst.shortname,
            gs.gene_count,
            ts.transcript_count,
            rss.json
        FROM
            release_set AS rst
            JOIN release_stats AS rss ON (
                rst.release_id=rss.release_id
            )
            JOIN (
                SELECT
                    rs.release_id,
                    COUNT(feature_id) AS gene_count
                FROM
                    release_set AS rs
                    JOIN gene_release_tag AS grt ON (
                        rs.release_id=grt.release_id
                    )
                GROUP BY
                    rs.release_id
            ) AS gs ON rst.release_id=gs.release_id
            JOIN (
                SELECT
                    rs.release_id,
                    COUNT(feature_id) AS transcript_count
                FROM
                    release_set AS rs
                    JOIN transcript_release_tag AS trt ON (
                        rs.release_id=trt.release_id
                    )
                GROUP BY
                    rs.release_id
            ) AS ts ON rst.release_id=ts.release_id;
    """
    cursor.execute(sql)
    results = cursor.fetchall()
    for release in results:
        json_blob = json.loads(release[4])
        assert release[2] == json_blob['gene']['core']
        assert release[2] == json_blob['gene']['tark_release']
        if release[0] == "Ensembl release " and release[1] == '75':
            continue
        assert release[3] == json_blob['transcript']['core']
        assert release[3] == json_blob['transcript']['tark_release']
