import os
import re

problems = [
    "11729", "1992", "9935", "10988", "9012", 
    "1929", "2609", "1158", "14719", "1260", 
    "9663", "9251", "1620", "2003", "18870"
]

base_dir = r"c:\Users\sigma\works\paper-lang-dist\problem"

count = 0
for p in problems:
    md_path = os.path.join(base_dir, f"IPOP_{p}.md")
    if not os.path.exists(md_path):
        print(f"File not found: {md_path}")
        continue
    
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    prob_dir = os.path.join(base_dir, f"IPOP_{p}")
    os.makedirs(prob_dir, exist_ok=True)
    
    in_matches = list(re.finditer(r"예제\s+입력\s+(\d+)", content))
    out_matches = list(re.finditer(r"예제\s+출력\s+(\d+)", content))
    
    if not in_matches:
        print(f"No examples found in {p}")
        continue
        
    for i in range(len(in_matches)):
        idx = in_matches[i].group(1)
        start_in = in_matches[i].end()
        
        out_match = next((om for om in out_matches if om.group(1) == idx), None)
        if not out_match:
            print(f"Mismatch: no output for input {idx} in {p}")
            continue
            
        inp_data = content[start_in:out_match.start()].strip()
        
        start_out = out_match.end()
        end_out = len(content)
        
        if i + 1 < len(in_matches):
            end_out = min(end_out, in_matches[i+1].start())
            
        # check hints or other common BOJ tail sequences
        hint_match = re.search(r"\n힌트|\n제한|\n##", content[start_out:])
        if hint_match:
            end_out = min(end_out, start_out + hint_match.start())
            
        out_data = content[start_out:end_out].strip()
        
        # Write
        with open(os.path.join(prob_dir, f"{idx}.inp"), 'w', encoding='utf-8', newline='\n') as f:
            f.write(inp_data + '\n')
            
        with open(os.path.join(prob_dir, f"{idx}.out"), 'w', encoding='utf-8', newline='\n') as f:
            f.write(out_data + '\n')
            
        count += 1
        print(f"Created {p}/{idx}.inp and {idx}.out")

print(f"\n총 {count}개의 입출력 픽스처(쌍) 추출을 완료했습니다.")
