#!/usr/bin/env python
# coding: utf-8

# # Problem 2 - Range Messaging

# In[1]:


import numpy as np
from tqdm import tqdm
import os

rng = np.random.default_rng(34893745)


# In[2]:


np.arange(5)


# In[20]:


class Case:
    def __init__(self, name, N, edges):
        print(f"+ {N}-{name}")
        self.name = name
        self.N = N
        self.edges = [(a+1, b+1) for a, b in edges]
        self.tags = []
    
    def validate(self):
        seen_edges = set()
        assert 0 <= len(self.edges) <= 100000
        assert 1 <= self.N <= 100000
        for a, b in self.edges:
            assert (a, b) not in seen_edges and (b, a) not in seen_edges
            assert 1 <= a <= self.N
            assert 1 <= b <= self.N
            seen_edges.add((a, b))
    
    def save(self, path, index):
        alltags = "-".join(self.tags)
        output_file = os.path.join(path, f"{self.N}-{self.name}-{alltags}-{index}.in")
        with open(output_file, "w") as f:
            f.write(f"{self.N} {len(self.edges)}\n")
            for a, b in self.edges:
                f.write(f"{a} {b}\n")
        return output_file

    def __str__(self):
        alltags = "-".join(self.tags)
        return f"[Case {self.N}-{self.name}-{alltags}: (N={self.N}, M={len(self.edges)}), {self.edges}]"


# In[4]:


def min_case():
    return Case("min", 1, [])

def max_case():
    return Case("max-empty", 100000, [])


# In[5]:


def sample_zipf(N, alpha):
    distr = rng.zipf(alpha, N)
    uni = np.unique(distr)
    lookup = { v: i for i, v in enumerate(uni) }
    data = [lookup[e] for e in distr]
    return f"zipf-{alpha}", N, data

def sample_weighted(N, weights):
    data = rng.choice(np.arange(len(weights)), N, True, weights)
    return "weighted", N, data

def sample_uniform(N, K):
    data = rng.permutation([i % K for i in range(N)])
    return f"uniform-{K}", N, data


# In[6]:


def connect_star(sample):
    tag, N, data = sample
    occ = {}
    edges = []
    for i, e in enumerate(data):
        if e not in occ:
            occ[e] = i
        else:
            edges.append((occ[e], i))
    c = Case("star", N, edges)
    c.tags.append(tag)
    return c

def connect_random(sample, crosslink_max=-1):
    tag, N, data = sample
    occ = {}
    edges = []
    for i, e in enumerate(data):
        if e not in occ:
            occ[e] = [i]
        else:
            edges.append((occ[e][rng.integers(0, len(occ[e]))], i))
            occ[e].append(i)
    if len(edges) < crosslink_max:
        kl = list(occ.keys())
        r = rng.integers(0, len(kl), crosslink_max - len(edges))
        for grp in np.array(kl)[r]:
            i, j = rng.integers(0, len(occ[grp]), 2)
            a, b = occ[grp][i], occ[grp][j]
            if a > b:
                a, b = b, a
            edges.append((a, b))
    c = Case("randomtree", N, list(set(edges)))
    if crosslink_max != -1:
        assert len(edges) <= crosslink_max
        c.tags.append("crosslink")
    c.tags.append(tag)
    return c


# In[29]:


def hideandseek(N):
    res = np.zeros(N, dtype=int)
    a, b = rng.choice(np.arange(0, N), 2, False)
    res[a] = 1
    res[b] = 2
    return "hidden", N, res

def zeros(N):
    res = np.zeros(N, dtype=int)
    return "zeros", N, res

def modify_sample_sub3(sample):
    for i, x in enumerate([0, 1, sample[1] - 1]):
        sample[2][x] = i
    return (sample[0] + "-sub3", sample[1], sample[2])


# In[30]:


str(modify_sample_sub3(hideandseek(100))[2])


# # Dataplan
# # M = 0
# - N = 1
# - N = max
# 
# # N <= 100, 1000, 100000
# ## Sampling
# - Sample from K things N times
# - Zipf distributed sampling (with truncation)
# 
# ## Connecting
# - Connect in a random tree
# - Connect in a star
# - Connect in a random tree + some other random edges
# 
# # Each person friends with 1, 2 or N
# - Sampling is the same
# - Set 1, 2 and N to different subsets
# - Split and connect up in special way
# 

# In[16]:


def cases_for(N):
    yield connect_star(sample_uniform(N, N))
    yield connect_star(sample_uniform(N, N//3))
    yield connect_star(sample_uniform(N, np.ceil(np.sqrt(N))))
    yield connect_star(sample_uniform(N, 3))
    
    yield connect_random(sample_uniform(N, 3), min((N*(N-1))//2, 100000))
    for alpha in [1.3, 2, 5]:
        yield connect_random(sample_zipf(N, alpha))
        yield connect_random(sample_zipf(N, alpha), min(2*N, 100000))
        yield connect_random(sample_zipf(N, alpha), min((N*(N-1))//2, 100000))


# In[34]:


def gen_all_cases():
    yield min_case()
    yield max_case()
    for c in cases_for(100):
        yield c
    for c in cases_for(1000):
        yield c
    for c in cases_for(100000):
        yield c
    yield connect_random(modify_sample_sub3(sample_uniform(100000, 3)), 100000)
    yield connect_random(modify_sample_sub3(sample_weighted(100000, [0.998, 0.001, 0.001])), 100000)
    yield connect_random(modify_sample_sub3(sample_weighted(100000, [0.9998, 0.0001, 0.0001])), 100000)
    yield connect_random(modify_sample_sub3(sample_weighted(100000, [0.9999, 0.00005, 0.00005])), 100000)
    yield connect_star(modify_sample_sub3(hideandseek(100000)))
    yield connect_star(modify_sample_sub3(hideandseek(100000)))
    yield connect_star(modify_sample_sub3(hideandseek(100000)))
    yield connect_star(modify_sample_sub3(zeros(100000)))


# In[35]:


CASES = list(tqdm(gen_all_cases()))


# In[36]:


# Validate
for c in CASES:
    try:
        c.validate()
    except AssertionError:
        print(c)
        raise
print("Validation passed!")


# In[13]:


# Output
print(os.getcwd())
OUTPUT_DIR = "."
for i, c in enumerate(CASES):
    c.save(OUTPUT_DIR, i)


# In[ ]:




