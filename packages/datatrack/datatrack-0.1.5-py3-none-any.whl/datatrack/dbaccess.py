# datatrack: tracks your data transformations.
# Copyright (C) 2024  Roman Kindruk

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import random
from enum import IntEnum

import psycopg

from .config import config as cfg


class RunStatus(IntEnum):
    STARTED = (1,)
    FINISHED = (2,)
    ERROR = (-1,)


CONN = None


def conn():
    global CONN
    if CONN is None:
        CONN = psycopg.connect(
            cfg()["database"]["postgresql"]["conninfo"], autocommit=True
        )
    return CONN


def generate_id():
    return "".join(random.choices("0123456789abcdef", k=32))


def normalize_project_name(project):
    return project.strip("/")


def get_or_create_project(project):
    project = normalize_project_name(project)
    with conn().cursor() as cur:
        cur.execute(
            "INSERT INTO project(name) VALUES (%s) ON CONFLICT DO NOTHING", (project,)
        )
        return cur.execute(
            "SELECT project_id FROM project WHERE name = %s", (project,)
        ).fetchone()[0]


def get_or_create_experiment(project, name):
    eid = generate_id()
    prj_id = get_or_create_project(project)
    with conn().cursor() as cur:
        sql = """\
        INSERT INTO experiment(experiment_id, project_id, name)
        VALUES (%s, %s, %s)
        ON CONFLICT (project_id, name) DO NOTHING
        """
        cur.execute(sql, (eid, prj_id, name))
        return cur.execute(
            "SELECT experiment_id FROM experiment WHERE name = %s AND project_id = %s",
            (name, prj_id),
        ).fetchone()[0]


def create_run(experiment_id, user, cmdline):
    run_id = generate_id()
    conn().execute(
        """
        INSERT INTO run(run_id, experiment_id, uid, status, started, cmdline)
        VALUES(%s, %s, %s, %s, now(), %s)
        """,
        (run_id, experiment_id, user, RunStatus.STARTED, cmdline),
    )
    return run_id


def finish_run(run_id, status, logs):
    conn().execute(
        """
        UPDATE run
        SET status=%s, finished=now(), logs=%s
        WHERE run_id=%s
        """,
        (status, logs, run_id)
    )


def run_register_artifact(run_id, artifact_id, type_):
    conn().execute(
        """
        INSERT INTO run_artifact(run_id, artifact_id, type)
        VALUES(%s, %s, %s)
        """,
        (run_id, artifact_id, type_),
    )


def run_register_parameter(run_id, name, data, type_):
    conn().execute(
        """
        INSERT INTO run_parameter(run_id, name, data, type)
        VALUES(%s, %s, %s, %s)
        """,
        (run_id, name, data, type_),
    )


def create_artifact(project, name, user, parent=None):
    pid = get_or_create_project(project)
    aid = generate_id()
    conn().execute(
        "INSERT INTO artifact(artifact_id, parent, project_id, name, uid, created) values(%s, %s, %s, %s, %s, now())",
        (aid, parent, pid, name, user),
    )
    return aid


def add_artifact_objects(artifact_id, objects):
    with conn().cursor() as cur:
        cur.executemany(
            "INSERT INTO file(artifact_id, path, size, etag, modified) values(%s, %s, %s, %s, %s)",
            [
                (
                    artifact_id,
                    obj.as_uri(),
                    obj.meta["Size"],
                    obj.meta["ETag"],
                    obj.meta["LastModified"],
                )
                for obj in objects
            ],
        )


def get_artifact(artifact_id):
    with conn().cursor(row_factory=psycopg.rows.dict_row) as cur:
        return cur.execute(
            "SELECT p.name as project FROM artifact a INNER JOIN project p USING(project_id) WHERE a.artifact_id = %s",
            (artifact_id,),
        ).fetchone()
