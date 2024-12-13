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


import getpass
import json
import sys
from enum import IntEnum

from . import dbaccess as db
from .artifact import Artifact


class ArtifactType(IntEnum):
    INPUT = (1,)
    OUTPUT = (2,)


class ParameterType(IntEnum):
    DEFAULT = (0,)
    OMEGACONF = (1,)


class Run:
    def __init__(self, experiment):
        self._exp = experiment
        cmdline = sys.argv
        if cmdline and cmdline[0].endswith("ipykernel_launcher.py"):
            # Runs within Jupyter don't have meaningful arguments
            cmdline = None
        else:
            cmdline = " ".join(cmdline)
        self._id = db.create_run(self._exp._id, getpass.getuser(), cmdline)

    @property
    def id(self):
        return self._id

    def get_artifact(self, artifact, path=None):
        db.run_register_artifact(self._id, artifact.id, ArtifactType.INPUT)
        return artifact.download(path)

    def create_artifact(self, path, name=None):
        aname = name or self._exp.name
        ar = Artifact.create(self._exp.project, aname, path)
        db.run_register_artifact(self._id, ar.id, ArtifactType.OUTPUT)
        return ar

    def create_parameter(self, param, name=None):
        type_ = ParameterType.DEFAULT
        try:
            from omegaconf import DictConfig, OmegaConf
            if isinstance(param, DictConfig):
                param = OmegaConf.to_container(param)
                type_ = ParameterType.OMEGACONF
        except ImportError:
            pass
        data = json.dumps(param)
        db.run_register_parameter(self._id, name, data, type_)

    def __repr__(self):
        return f"<Run id={self._id}>"
