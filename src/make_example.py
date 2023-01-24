from utils.const import EPS

import math
import random
import pandas as pd

import matplotlib.pyplot as plt

def create_ieal_g_h(N):
    g_h_dif = [random.random() for _ in range(N)]
    g_h_list = [g_h_dif[0]]
    for i in range(1, N):
        g_h_list.append(g_h_list[i-1] + g_h_dif[i])

    unnormed_h = [random.random() for _ in range(N)]
    sum_unnormed_h = sum(unnormed_h)
    h = [uh / sum_unnormed_h for uh in unnormed_h]

    unnormed_g = [h * g_h for h, g_h in zip(h, g_h_list)]
    sum_unnormed_g = sum(unnormed_g)
    g= [ug / sum_unnormed_g for ug in unnormed_g]

    return g, h


def create_easy_g_h(N):
    g_dif = [random.random() for _ in range(N)]
    unnormed_g = [0 for _ in range(N)]
    unnormed_g[0] = g_dif[0]
    for i in range(1, N):
        unnormed_g[i] = unnormed_g[i-1] + g_dif[i]
    sum_unnormed_g = sum(unnormed_g)
    g= [ug / sum_unnormed_g for ug in unnormed_g]


    h_dif = [random.random() for _ in range(N)]
    unnormed_h = [0 for _ in range(N)]
    unnormed_h[N-1] = h_dif[N-1]
    for i in reversed(range(N-1)):
        unnormed_h[i] = unnormed_h[i+1] + h_dif[i]
    sum_unnormed_h = sum(unnormed_h)
    h = [uh / sum_unnormed_h for uh in unnormed_h]


    return g, h


if __name__ == "__main__":
    pos_num = 30
    neg_num = 70
    N = 10

    label_score_list = []
    # g, h = create_ieal_g_h(N)

    g, h = create_easy_g_h(N)

    for region_idx, (g_, h_) in enumerate(zip(g, h)):
        pos_ = math.floor(pos_num * g_ + 0.5)
        neg_ = math.floor(neg_num * h_ + 0.5)
        for _ in range(pos_):
            label_score_list.append([1, (region_idx + random.random()) / N])
        for _ in range(neg_):
            label_score_list.append([0, (region_idx + random.random()) / N])
    random.shuffle(label_score_list)

    key_label_score_list = []
    for idx, (label, score) in enumerate(label_score_list):
        key = f"k{idx}"
        key_label_score_list.append(
            [key, label, score]
        )

    df = pd.DataFrame(key_label_score_list, columns=['key', 'label', 'score'])

    df.to_csv("data/example.csv")
    

    pos_scores = df[df['label'] == 1]['score']
    neg_scores = df[df['label'] == 0]['score']

    plt.hist(pos_scores, label="pos", alpha = 0.5)
    plt.hist(neg_scores, label="neg", alpha = 0.5)
    plt.show()
    

