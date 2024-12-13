#!/usr/bin/env python

"""
Tests artifact creation

Usage:
  test_artifact_create.py --project=PROJECT --name=NAME SOURCE

Arguments:
  SOURCE     a location of the files, can be a local path or S3 URI

Options:
  -p, --project=PROJECT     a name of the project
  -n, --name=NAME           a name of the project
  -h, --help                display this help and exit
"""


from docopt import docopt
from datatrack import Artifact


if __name__ == "__main__":
    args = docopt(__doc__)
    a = Artifact.create(args["--project"], args["--name"], args["SOURCE"])
    print(a)
