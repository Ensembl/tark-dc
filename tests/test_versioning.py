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


def test_ver_asm_seq_conflicts(cursor):
    """
    Test case to ensure that there are no clashes between any releases where
    the stable_id, version and assembly are the same, but the sequence checksum
    is different.

    This should ahve raised an error on the ensembl side, but this can be
    checked easily here as well.

    .. code-block:: none
       pytest tests/test_data.py
    """
    sql = """
        SELECT
            rs1.shortname,
            rs2.shortname,
            COUNT(*)
        FROM
            transcript AS t1
            JOIN transcript_release_tag trt1 ON (
                t1.transcript_id=trt1.feature_id
            )
            JOIN release_set rs1 ON (trt1.release_id=rs1.release_id)
            JOIN transcript AS t2 ON (
                t1.stable_id=t2.stable_id
                AND t1.stable_id_version=t2.stable_id_version
            )
            JOIN transcript_release_tag trt2 ON (
                t2.transcript_id=trt2.feature_id
            )
            JOIN release_set rs2 ON (
                trt2.release_id=rs2.release_id
                AND rs1.assembly_id=rs2.assembly_id
                AND rs1.description=rs2.description
            )
        WHERE
            rs1.shortname BETWEEN
                (SELECT MIN(shortname) FROM release_set) AND
                (SELECT MAX(shortname) FROM release_set)-1
            AND rs2.shortname BETWEEN
                rs1.shortname+1 AND (SELECT MAX(shortname) FROM release_set)
            AND t1.seq_checksum!=t2.seq_checksum
        GROUP BY
            rs1.shortname,
            rs2.shortname;
    """
    result = cursor.execute(sql)
    assert result == 0
