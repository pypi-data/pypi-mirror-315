# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import yaml

like_tool_yaml = """
type: function
function:
  name: like_post
  description: Like this post, because I thinkit is good
  parameters: 
    type: object
    properties: 
      like:
        type: string
        description: yes or no,
    required:
      - like
"""

like_tool = yaml.safe_load(like_tool_yaml)
...