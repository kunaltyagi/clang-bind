#! /usr/bin/env python

from generic import utils

from enum import Enum
import os
from typing import Dict, List, Optional


class MatchingRule(Enum):
    STRICT = 1
    FROM_ROOT = 2
    RELAXED = 3


def matching(
    filename: str,
    user_provided_names: List[str],
    options: MatchingRule = MatchingRule.RELAXED,
    root: str = "",
) -> bool:
    if options == MatchingRule.STRICT:
        return filename in user_provided_names
    elif options == MatchingRule.FROM_ROOT:
        splits = filename.split(root, 1)
        if len(splits) == 1:
            return False
        _, filename = splits
        return splits[1] in user_provided_names
    elif options == MatchingRule.RELAXED:
        any(name.endswith(filename) for name in user_provided_names)
    raise ValueError(
        f"Bad value ({options}) for matching rule. Valid values are {[value for value in MatchingRule]}"
    )


def find_similar(
    targets: List[Dict[str, str]],
    selections: List[str],
    options: MatchingRule,
    root: str = "",
) -> List[str]:
    return [
        target["file"]
        for target in targets
        if matching(target["file"], selections, options, root)
    ]


def get_file_list(
    directory: str,
    selected_files: Optional[List[str]] = None,
    ignored_files: List[str] = [],
    matcher: MatchingRule = MatchingRule.STRICT,
) -> Dict[str, str]:
    name = "compile_commands.json"
    if name not in os.listdir(directory):
        return {}
    target_list = utils.read_json(utils.join_path(directory, name))
    if len(target_list) == 0:
        return {}

    assert directory == target_list[0]["directory"]

    if selected_files is None:
        selected_files = [target["file"] for target in target_list]
    else:
        selected_files = find_similar(target_list, selected_files, matcher, directory)
    if len(selected_files) == 0:
        return {}
    for target in target_list:
        pass
    return {}
