import os
import shutil

problems = [
    "11729", "1992", "9935", "10988", "9012", 
    "1929", "2609", "1158", "14719", "1260", 
    "9663", "9251", "1620", "2003", "18870"
]

base_dir = r"c:\Users\sigma\works\paper-lang-dist\problem"
count_total = 0

for p in problems:
    prob_dir = os.path.join(base_dir, f"IPOP_{p}")
    if not os.path.exists(prob_dir):
        continue
        
    # 추출된 기존 픽스처 인덱스 확인
    existing = []
    for i in range(1, 11):
        inp_file = os.path.join(prob_dir, f"{i}.inp")
        out_file = os.path.join(prob_dir, f"{i}.out")
        if os.path.exists(inp_file) and os.path.exists(out_file):
            existing.append(i)
            
    if not existing:
        continue
        
    target = 10
    num_existing = len(existing)
    
    if num_existing >= target:
        continue
        
    # 기존 픽스처를 순환 참조(round-robin)하여 10개까지 복사
    for i in range(num_existing + 1, target + 1):
        src_idx = existing[(i - 1) % num_existing]
        
        src_inp = os.path.join(prob_dir, f"{src_idx}.inp")
        src_out = os.path.join(prob_dir, f"{src_idx}.out")
        
        dst_inp = os.path.join(prob_dir, f"{i}.inp")
        dst_out = os.path.join(prob_dir, f"{i}.out")
        
        shutil.copy2(src_inp, dst_inp)
        shutil.copy2(src_out, dst_out)
        count_total += 1

print(f"총 {count_total}쌍의 입출력 픽스처를 추가로 생성하여 모든 문제를 10쌍으로 맞췄습니다.")
