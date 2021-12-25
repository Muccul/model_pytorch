import torch
from collections import namedtuple

mem_to_max_patch_idx = namedtuple('mem_to_max_patch_idx', ['cur_idx', 'max_attach_idx'])
mem_mapping = []
mem_expand_size = 1
patch_height = 4
patch_width = 4
for cur_idx in range(4 * 4):
    cur_row = cur_idx // patch_width
    cur_col = cur_idx % patch_width
    max_row = min(patch_height - 1, cur_row + mem_expand_size)
    max_col = min(patch_width - 1, cur_col + mem_expand_size)
    max_idx = max_row * patch_width + max_col
    mem_mapping.append(mem_to_max_patch_idx(cur_idx=cur_idx, max_attach_idx=max_idx))
