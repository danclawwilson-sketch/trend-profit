import os, glob

# 只保留 timestamp, open, high, low, close（去掉不需要的列）
files = sorted(glob.glob("data/*.txt"))
total_before = 0
total_after = 0

for f in files:
    total_before += os.path.getsize(f)
    with open(f, "r") as fh:
        lines = fh.readlines()
    
    header = "timestamp,open,high,low,close\n"
    trimmed = [header]
    for line in lines[1:]:  # skip original header
        parts = line.strip().split(",")
        if len(parts) >= 5:
            trimmed.append(",".join(parts[:5]) + "\n")
    
    with open(f, "w") as fh:
        fh.writelines(trimmed)
    total_after += os.path.getsize(f)

print(f"精簡前: {total_before/1024/1024:.1f} MB")
print(f"精簡後: {total_after/1024/1024:.1f} MB")
print(f"節省: {(total_before-total_after)/1024/1024:.1f} MB ({(1-total_after/total_before)*100:.0f}%)")
