import torch



mem_mapping = dict()  # mapping cur_idx: max_attach_idx
mem_expand_size = 1
patch_height = 4
patch_width = 4
for cur_patch_idx in range(4*4):
    cur_row = cur_patch_idx // patch_width
    cur_col = cur_patch_idx % patch_width
    max_row = min(patch_height-1, cur_row+mem_expand_size)
    max_col = min(patch_width-1, cur_col+mem_expand_size)
    max_idx = max_row * patch_width + max_col
    mem_mapping[cur_patch_idx] = max_idx

def update_mem(mem_pool, mem_mapping, mem, cur_patch_idx):
    # add new_mem
    mem_pool[cur_patch_idx] = mem

    # filter mem
    del_idxs = []
    for k in mem_pool.keys():
        if mem_mapping[k] > cur_patch_idx:
            continue
        else:
            del_idxs.append(k)
    for del_idx in del_idxs:
        del mem_pool[del_idx]


def get_mem_from_pool(mem_pool, cur_patch_idx, mem_expand_size=1, patch_height=4, patch_width=4):
    cur_patch_row = cur_patch_idx // patch_width
    cur_patch_col = cur_patch_idx % patch_width

    rows = torch.arange(max(0, cur_patch_row - mem_expand_size), min(patch_height, cur_patch_row + 1))
    cols = torch.arange(max(0, cur_patch_col - mem_expand_size), min(patch_width, cur_patch_col + mem_expand_size + 1))

    coords_init = torch.stack(torch.meshgrid([rows, cols]), dim=-1).reshape(-1, 2)
    coords_filtered = [coord for coord in coords_init if coord[0] < cur_patch_row or coord[1] < cur_patch_col]
    mem_idxs = [int(coord[0] * patch_width + coord[1]) for coord in coords_filtered]

    return [mem_pool[idx] for idx in mem_idxs]
