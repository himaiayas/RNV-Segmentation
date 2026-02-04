from collections import deque
import numpy as np
from PIL import Image
import os


DIR = ((1, 0), (0, 1), (-1, 0), (0, -1))

def fill_color(mat):


    q = deque()

    for j in range(len(mat[0])):
        q.append((0, j))
        q.append((len(mat)-1, j))

    for i in range(len(mat)):
        q.append((i, 0))
        q.append((i, len(mat[0])-1))


    while q:
        i, j = q.popleft()
        val = mat[i][j]

        if val == 0:
            mat[i][j] = -1

            for di, dj in DIR:
                n_i, n_j = i + di, j + dj
                if (0 <= n_i < len(mat)) and (0 <= n_j < len(mat[0])):
                    q.append((n_i, n_j))

    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j] == 0:
                mat[i][j] = 1
            elif mat[i][j] == -1:
                mat[i][j] = 0
    return mat

with os.scandir('data/prelabled') as it:
    for entry in it:

        img = Image.open(f'data/prelabled/{entry.name}')
        mat = np.array(img.convert('L'))//255
        mat = mat.astype('int32')
        mat = fill_color(mat)*255
        Image.fromarray(mat).convert('RGB').save(f'data/output/{entry.name}')


