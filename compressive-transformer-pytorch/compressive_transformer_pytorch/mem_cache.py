import torch



mem_mapping = dict()  # mapping cur_idx: max_attach_idx
mem_expand_size = 1
patch_height = 4
patch_width = 4
for cur_idx in range(4*4):
    cur_row = cur_idx // patch_width
    cur_col = cur_idx % patch_width
    max_row = min(patch_height-1, cur_row+mem_expand_size)
    max_col = min(patch_width-1, cur_col+mem_expand_size)
    max_idx = max_row * patch_width + max_col
    mem_mapping[cur_idx] = max_idx

def update_mem(mem_pool, mem_mapping, mem, cur_idx):
    # add new_mem
    mem_pool[cur_idx] = mem

    # filter mem
    del_idxs = []
    for k in mem_pool.keys():
        if mem_mapping[k] > cur_idx:
            continue
        else:
            del_idxs.append(k)
    for del_idx in del_idxs:
        del mem_pool[del_idx]