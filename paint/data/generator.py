#!/usr/bin/env python
# coding: utf-8

# # Problem 3 - Purchasing Paint

# In[98]:


from tqdm import tqdm
import numpy as np
import os

# Sometimes an assertion fails. Just shuffle the seed again when that happens. #ostrich
rng = np.random.default_rng(42838858382)


# In[99]:


class Case:
    def __init__(self, name, K, D, costs):
        self.name = name
        self.K = K
        self.D = D
        self.costs = costs
    
    def validate(self):
        N = len(self.costs)
        seen_colours = set()
        assert 1 <= N <= 2000
        assert 1 <= self.K <= 2000
        assert 1 <= self.D <= N
        for d, c in self.costs:
            assert 0 <= c <= 1000000000
            assert 1 <= d <= self.D
            seen_colours.add(d)
        assert seen_colours == set(range(1, self.D+1))
    
    def save(self, path, index):
        output_file = os.path.join(path, f"{len(self.costs)}-{self.K}-{self.D}-{self.name}-{index}.in")
        with open(output_file, "w") as f:
            f.write(f"{len(self.costs)} {self.K} {self.D}\n")
            for a, b in self.costs:
                f.write(f"{a} {b}\n")
        return output_file

    def __str__(self):
        return f"[Case {len(self.costs)}-{self.K}-{self.D}-{self.name}: {self.costs}]"


# In[100]:


def min_case():
    K, D = 1, 1
    return Case("min", K, D, [(1, 10**9)])

def max_case():
    N, K, D = 2000, 1, 2000
    return Case("max", K, D, [(i, 1000000000) for i in range(1, 2001)])

def uniform_distribute(N, D):
    res = [(N + i) // D for i in range(D)]
    assert sum(res) == N
    return np.array(res).astype(int)

def random_distribute(N, D):
    if N == 1:
        return np.array([1] + [0] * (D-1))
    res = set()
    while len(res) < D-1:
        res.add(rng.integers(1, N))
    parts = np.concatenate([np.array([0]), np.sort(list(res)), np.array([N])])
    return np.diff(parts).astype(int)


# In[101]:


def make_case(N, D, K, total, random_paints, random_weights, random_costs):
    print(f"Make {N} {D} {K} {total}")
    if random_paints:
        paints = random_distribute(N, D)
    else:
        paints = uniform_distribute(N, D)
    
    if random_weights:
        weights = random_distribute(total, D)
    else:
        weights = uniform_distribute(total, D)
    
    res = []
    for i, (p, w) in enumerate(zip(paints, weights)):
        if random_costs:
            vals = random_distribute(w, p)
        else:
            vals = uniform_distribute(w, p)
        
        vals = np.min(np.array([np.repeat(1000000000, p), vals]), axis=0)
        
        for v in vals:
            res.append((i+1, v))
    
    return Case(f"{int(random_paints)}{int(random_weights)}{int(random_costs)}", K, D, res)


# In[102]:


str(make_case(10, 1, 10, 5000000000, False, False, False))


# # Dataplan
# 
# ## Subtask 1 - K = 1
# ## Subtask 2 - K = 2
# ## Subtask 3 - N <= 18
# ## Subtask 4 - Total cost <= 2e3, Kth best is always take best
# - Generate a bunch of small cases and pray some of them end up here
# - Make N large enough and uniformly distribute paint costs
# ## Subtask 5 - No further constraints
# - Uniformly distribute paint types
# - Choose for paint costs either uniform or random
# - Shold be good enough lol
# - Worst case - consider worst possible option

# In[107]:


def gen_cases_for(N, K, total):
    if K <= N:
        yield make_case(N, 1, K, total, True, True, True)
        yield make_case(N, 1, K, total, False, False, False)
    if K * 8 <= N*N:
        yield make_case(N, 2, K, total, True, False, True)
        yield make_case(N, 2, K, total, True, True, True)
        yield make_case(N, 2, K, total, False, False, False)
    
    yield make_case(N, 10, K, total, True, True, True)
    yield make_case(N, 10, K, total, False, False, True)
    yield make_case(N, 10, K, total, False, True, True)
    
    if N >= 100:
        yield make_case(N, 100, K, total, True, True, True)
        yield make_case(N, 100, K, total, False, True, True)
    
    yield make_case(N, N//2, K, total, False, False, False)
    yield make_case(N, N//2, K, total, False, False, True)
    yield make_case(N, N//2, K, total, False, True, False)
    yield make_case(N, N//2, K, total, False, True, True)
    
    yield make_case(N, N, K, total, False, False, False)

SUBTASKS = [
    (2000, 1, 1000 * 1000000000),
    (2000, 2, 1000 * 1000000000),
    (18, 18, 2000),
    (18, 2000, 2000),
    (300, 300, 150 * 1000000000),
    (2000, 2000, 1000 * 1000000000)
]
def gen_all_cases():
    # Min, max
    yield min_case()
    yield max_case()
    
    for n, k, tot in SUBTASKS:
        for c in gen_cases_for(n, k, tot):
            yield c
    
    # Special subtask 4 stuff
    yield make_case(2000, 2, 2000, 2000, False, False, False)
    yield make_case(2000, 10, 2000, 2000, False, False, False)
    yield make_case(2000, 100, 2000, 2000, False, False, False)
    yield make_case(2000, 1000, 2000, 2000, False, False, False)
    


# In[108]:


ALL_CASES = list(tqdm(gen_all_cases()))


# In[109]:


# Validate
for c in ALL_CASES:
    try:
        c.validate()
    except AssertionError:
        print(c)
        raise
print("Validation passed!")


# In[83]:


# Output
print(os.getcwd())
OUTPUT_DIR = "."
for i, c in enumerate(ALL_CASES):
    c.save(OUTPUT_DIR, i)


# In[113]:


str(make_case(100, 2, 2000, 2000, True, True, True))


# In[ ]:




