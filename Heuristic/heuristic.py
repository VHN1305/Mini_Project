# Có N đồ án tốt nghiệp 1, 2, … , 𝑁 và 𝑀
# thầy cô cần được chia vào 𝐾 hội đồng
# • Mỗi đồ án 𝑖 có 𝑡(𝑖) là giáo viên hướng 
# dẫn
# • Giữa 2 đồ án 𝑖 và 𝑗 có độ tương đồng 
# 𝑠(𝑖,𝑗)
# • Giữa đồ án 𝑖 và giáo viên 𝑗 có độ tương 
# đồng 𝑔(𝑖,𝑗)
# • Yêu cầu
# • Số đồ án trong mỗi HĐ phải lớn hơn hoặc 
# bằng 𝑎 và nhỏ hơn hoặc bằng 𝑏
# • Số giáo viên trong mỗi HĐ phải lớn hơn 
# hoặc bằng 𝑐 và nhỏ hơn hoặc bằng 𝑑
# • Giáo viên không được ngồi hội đồng của 
# sinh viên mình hướng dẫn
# • Độ tương đồng giữa các đồ án trong cùng 
# hội đồng phải lớn hơn hoặc bằng 𝑒
# • Độ tương đồng giữa đồ án với giáo viên 
# trong hội đồng phải lớn hơn hoặc bằng 𝑓
# • Tổng độ tương đồng giữa các đồ án và 
# giữa đồ án với giáo viên trong các hội 
# đồng phải lớn nhất
# Similarity matrix between thesis i and thesis j is as follows: 0 2 4 1 2 5 2 0 5 5 3 5 4 5 0 4 3 5 1 5 4 0 3 2 2 3 3 3 0 3 5 5 5 2 3 0
import random
import sys
from input import read_input, data_input

sys.stdin = open(data_input[0], 'r')

num_theses, num_teachers, num_councils, a, b, c, d, e, f, s, g, q = read_input()

temp = [[0] * num_teachers for _ in range(num_theses)]

for i, val in enumerate(q):
    temp[i][val-1] = 1
q = temp

p = [[0 for _ in range(num_councils)] for _ in range(num_teachers)]
h = [[0 for _ in range(num_councils)] for _ in range(num_theses)]

# Randomly assign teachers to councils
for i in range(num_teachers):
    p[i][random.randint(0, num_councils - 1)] = 1

# Randomly assign theses to councils
for i in range(num_theses):
    h[i][random.randint(0, num_councils - 1)] = 1

# Heuristic optimization
# Reassign based on the heuristic to satisfy the constraints

# function to get the total similarity score within a council
def get_council_similarity(council):
    score = 0
    for i in range(num_theses):
        for j in range(i + 1, num_theses):
            if h[i][council] == 1 and h[j][council] == 1:
                score += s[i][j]
    return score

# function to get the total similarity score between theses and teachers within a council
def get_council_teacher_similarity(council):
    score = 0
    for i in range(num_theses):
        for j in range(num_teachers):
            if h[i][council] == 1 and p[j][council] == 1:
                score += g[i][j]
    return score

# Optimize the assignments for each council
for k in range(num_councils):
    council_theses = [i for i in range(num_theses) if h[i][k] == 1]
    council_teachers = [j for j in range(num_teachers) if p[j][k] == 1]
    
    # Ensure the number of theses in the council is within [a, b]
    while len(council_theses) < a:
        i = random.choice([i for i in range(num_theses) if h[i][k] == 0])
        h[i][k] = 1
        council_theses.append(i)
        
    while len(council_theses) > b:
        i = random.choice([i for i in council_theses])
        h[i][k] = 0
        council_theses.remove(i)
    
    # Ensure the number of teachers in the council is within [c, d]
    while len(council_teachers) < c:
        j = random.choice([j for j in range(num_teachers) if p[j][k] == 0])
        p[j][k] = 1
        council_teachers.append(j)
        
    while len(council_teachers) > d:
        j = random.choice([j for j in council_teachers])
        p[j][k] = 0
        council_teachers.remove(j)
    
    # Ensure each thesis is assigned to exactly one council
    for i in range(num_theses):
        if h[i][k] == 1 and sum(h[i]) > 1:
            other_council = random.choice([c for c in range(num_councils) if c != k])
            h[i][k] = 0
            h[i][other_council] = 1
    
    # Ensure each teacher is assigned to exactly one council
    for j in range(num_teachers):
        if p[j][k] == 1 and sum(p[j]) > 1:
            other_council = random.choice([c for c in range(num_councils) if c != k])
            p[j][k] = 0
            p[j][other_council] = 1

    # for i in range(num_theses):
    #     if h[i][k] == 1:
    #         for j in range(num_teachers):
    #             if p[j][k] == 1:
    #                 if g[i][j] < e:
    #                     p[j][k] = 1 - p[j][k]
    #                     break
    #         if sum(p[j]) > 1:
    #             p[j][k] = 1 - p[j][k]
    #             break
    # for j in range(num_teachers):
    #     if p[j][k] == 1:
    #         for i in range(num_theses):
    #             if h[i][k] == 1:
    #                 if g[i][j] < f:
    #                     h[i][k] = 1 - h[i][k]
    #                     break
    #         if sum(h[i]) > 1:
    #             h[i][k] = 1 - h[i][k]
    #             break
    # Similarity score between each pair of thesis in each council is at least e
    # s[i][j] >= e * h[i, k] * h[j, k]
    for i in range(num_theses):
        for j in range(i + 1, num_theses):
            if h[i][k] == 1 and h[j][k] == 1 and s[i][j] < e:
                h[i][k] = 1 - h[i][k]
                break
        if sum(h[i]) > 1:
            h[i][k] = 1 - h[i][k]
            break

    # Similarity score between each pair of thesis and teacher in each council is at least f
    # g[i][j] >= f * h[i, k] * p[j, k]
    for i in range(num_theses):
        for j in range(num_teachers):
            if h[i][k] == 1 and p[j][k] == 1 and g[i][j] < f:
                p[j][k] = 1 - p[j][k]
                break
        if sum(p[j]) > 1:
            p[j][k] = 1 - p[j][k]
            break

# Print the results
print(num_theses)
for i in range(num_theses):
    for j in range(num_councils):
        if h[i][j] == 1:
            print(j + 1, end=' ')
print()

print(num_teachers)
for i in range(num_teachers):
    for j in range(num_councils):
        if p[i][j] == 1:
            print(j + 1, end=' ')
print()
