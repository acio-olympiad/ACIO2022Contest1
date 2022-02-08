#!/usr/bin/env python
# coding: utf-8

# # Problem 1 - Squirrel Postal Service

# In[1]:


import numpy as np
from tqdm import tqdm
import os
np.random.seed(32987342)


# In[2]:


# Handmade
def gen_one_node():
    return "one_node", []

def gen_two_nodes():
    return "two_node", [(1, 2)]


# In[3]:


def gen_star(n):
    return f"star-cent-{n}", [(1, i) for i in range(2, n+1)]

def gen_star_2(n):
    return f"star-noncent-{n}", [(2, i) for i in range(1, n+1) if i != 2]

def gen_spiky(n):
    res = []
    for i in range(2, n+1):
        par = i-1 if i % 2 == 0 else i-2
        res.append((par, i))
    return f"spiky-{n}", res

def gen_complete_bintree(n):
    res = []
    for i in range(2, n+1):
        par = i // 2
        res.append((par, i))
    return f"complete-bintree-{n}", res

def gen_random_graph(n):
    res = []
    for i in range(2, n+1):
        par = np.random.randint(1, i)
        res.append((par, i))
    return f"random-{n}", res

def gen_line(n):
    return f"line-{n}", [(i-1, i) for i in range(2, n+1)]


# In[4]:


def permute(case):
    name, edges = case
    name = f"{name}-permuted"
    perm = np.random.permutation(len(edges) + 1) + 1
    return name, perm[np.array(edges) - 1]


# In[5]:


def validate(case):
    name, edges = case
    N = len(edges) + 1
    seen = set()
    for a, b in edges:
        assert a != b and (1 <= a <= N) and (1 <= b <= N)
        seen.add(a)
        seen.add(b)
    assert N == 1 or seen == set(range(1, N+1))
    return name, N, edges

def print_case(path, case):
    name, n, edges = validate(case)
    with open(os.path.join(path, f"{name}.in"), "w") as f:
        f.write(f"{n}\n")
        for a, b in edges:
            f.write(f"{a} {b}\n")


# ## Dataplan
# 
# ### Handmade
# - 1 node
# - 2 nodes
# 
# ### Subtask 1 + 3
#  - Star centered at 1
#  - Star centered at 2
#  - Spiky
#  - Complete Binary Tree
#  - Random graph
#  
# ### Subtask 2
#  - Sequential line
#  - Random line

# In[7]:


CASES = [
    gen_one_node(),
    gen_two_nodes(),

    gen_star(1000),
    gen_star_2(1000),
    gen_spiky(1000),
    permute(gen_spiky(1000)),
    gen_complete_bintree(511),
    permute(gen_complete_bintree(511)),
    gen_complete_bintree(1000),
    permute(gen_random_graph(1000)),
    permute(gen_random_graph(1000)),
    permute(gen_random_graph(1000)),
    permute(gen_random_graph(1000)),
    permute(gen_random_graph(1000)),
    
    gen_line(1000),
    permute(gen_line(1000)),
    permute(gen_line(1000)),
    permute(gen_line(1000)),
    gen_line(100000),
    permute(gen_line(100000)),
    permute(gen_line(100000)),
    permute(gen_line(100000)),
    permute(gen_line(100000)),
    permute(gen_line(100000)),
    permute(gen_line(100000)),
    
    gen_star(100000),
    gen_star_2(100000),
    gen_spiky(100000),
    permute(gen_spiky(100000)),
    gen_complete_bintree(65535),
    permute(gen_complete_bintree(100000)),
    gen_complete_bintree(100000),
    permute(gen_random_graph(100000)),
    permute(gen_random_graph(100000)),
    permute(gen_random_graph(100000)),
    permute(gen_random_graph(100000)),
    permute(gen_random_graph(100000))
]


# In[11]:


# Check you're generating to the right place!
print(os.environ["PWD"])


# In[8]:


DATAPATH = "."
for case in tqdm(CASES):
    print_case(DATAPATH, case)

