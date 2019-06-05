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
    """
    sql = """
        SELECT
            release_set.description,
            release_set.shortname,
            gene_set.gene_count,
            transcript_set.transcript_count,
            release_stats.json
        FROM
            release_set
            JOIN release_stats ON (
                release_set.release_id=release_stats.release_id
            )
            JOIN (
                SELECT
                    release_set.release_id,
                    COUNT(feature_id) AS gene_count
                FROM
                    release_set
                    JOIN gene_release_tag ON (
                        release_set.release_id=gene_release_tag.release_id
                    )
                GROUP BY
                    release_set.release_id
            ) AS gene_set ON release_set.release_id=gene_set.release_id
            JOIN (
                SELECT
                    release_set.release_id,
                    COUNT(feature_id) AS transcript_count
                FROM
                    release_set
                    JOIN transcript_release_tag ON (
                        release_set.release_id=transcript_release_tag.release_id
                    )
                GROUP BY
                    release_set.release_id
            ) AS transcript_set ON release_set.release_id=transcript_set.release_id;
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
