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


import io
import logging
import os
import sys
from contextlib import contextmanager
from datetime import datetime
from threading import Thread

from . import dbaccess as db
from .run import Run


def preserve_logs(out, stdout, logs):
    """
    Reads from the pipe's read end `out` and
    writes to the original stdout/pty and to
    the `logs` buffer to store it into the DB later.
    """
    buf = os.read(out, 1024)
    while buf:
        os.write(stdout, buf)
        logs.write(buf)
        buf = os.read(out, 1024)


class Experiment:
    def __init__(self, project, name):
        self.project = project
        self.name = name
        self._id = db.get_or_create_experiment(project, name)

    @contextmanager
    def run(self):
        start_time = datetime.now()

        r, w = os.pipe()
        logs = io.BytesIO()
        old_out = os.dup(sys.stdout.fileno())
        old_err = os.dup(sys.stderr.fileno())
        os.dup2(w, sys.stdout.fileno())
        os.dup2(w, sys.stderr.fileno())
        log_thread = Thread(target=preserve_logs, args=[r, old_out, logs])
        log_thread.start()

        r = Run(self)
        logging.info(f"{r}: started")

        try:
            yield r
        except:
            status = db.RunStatus.ERROR
            logging.error(f"{r}: failed after {datetime.now() - start_time}")
            raise
        else:
            status = db.RunStatus.FINISHED
            logging.info(f"{r}: finished in {datetime.now() - start_time}")
        finally:
            os.dup2(old_out, sys.stdout.fileno())
            os.dup2(old_err, sys.stderr.fileno())
            os.close(w)
            log_thread.join()
            db.finish_run(r.id, status, logs.getvalue().decode('utf-8'))

    def __repr__(self):
        return f"Experiment(project='{self.project}', name='{self.name}')"
