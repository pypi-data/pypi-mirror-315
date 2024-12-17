#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2024 UL Research Institutes
# SPDX-License-Identifier: MIT


import argparse
import sys
from typing import Any

import attrs
import markdown
from jinja2 import Environment, FileSystemLoader
from ruamel.yaml import YAML

from ..config.project.serializers import load as load_cici_config
from ..constants import CICI_DIR, CICI_FILE, PROJECT_DIR, TEMPLATE_DIR
from ..providers.gitlab.utils import get_job_names


def to_markdown(text):
    return markdown.markdown(text)


def get_yaml_data(filename):
    yaml = YAML(typ="safe")
    return yaml.load(open(filename))


def get_gitlab_ci_jobs(gitlab_ci_file) -> dict[str, Any]:
    try:
        data = get_yaml_data(gitlab_ci_file)
    except FileNotFoundError:
        return {}
    return {job: data[job] for job in get_job_names(data) if not job.startswith(".")}


def get_precommit_hooks(precommit_hooks_file) -> dict[str, Any]:
    try:
        data = get_yaml_data(precommit_hooks_file)
    except FileNotFoundError:
        return {}
    return {hook["id"]: hook for hook in data}


def readme_command(parser, args):
    environment = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
    )
    environment.filters["markdown"] = to_markdown

    template = environment.get_template("README.md.j2")

    gitlab_ci_jobs = get_gitlab_ci_jobs(CICI_DIR / ".gitlab-ci.yml")
    precommit_hooks = get_precommit_hooks(PROJECT_DIR / ".pre-commit-hooks.yaml")

    config = load_cici_config(
        args.config_file, gitlab_ci_jobs=gitlab_ci_jobs, precommit_hooks=precommit_hooks
    )

    args.output_file.write(
        template.render(
            **attrs.asdict(config),
        )
    )


def readme_parser(subparsers):
    parser = subparsers.add_parser("readme", help="generate pipeline readme")
    parser.add_argument(
        "-o",
        "--output",
        dest="output_file",
        type=argparse.FileType("w"),
        default=sys.stdout,
    )
    parser.add_argument(
        "-c",
        "--config",
        dest="config_file",
        default=CICI_FILE,
    )
    parser.set_defaults(func=readme_command)
    return parser
