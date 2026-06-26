import os
from collections import Counter
import matplotlib.pyplot as plt

label_dir = "dataset/labels/train"
class_names = [
    'A','B','C','D','E','F','G','H','I','J',
    'K','L','M','N','O','P','Q','R','S','T',
    'U','V','W','X','Y','Z',
    '0','1','2','3','4','5','6','7','8','9',
    'Ayah','Halo','Kakak','Minum','Rumah','Terima kasih','Tidur'
]

counter = Counter()
for fname in os.listdir(label_dir):
    if fname.endswith(".txt"):
        with open(os.path.join(label_dir, fname)) as f:
            for line in f:
                cls_id = int(line.split()[0])
                counter[cls_id] += 1

print("=== DISTRIBUSI KELAS ===")
for i, name in enumerate(class_names):
    count = counter.get(i, 0)
    bar = "█" * (count // 10)
    status = "⚠️ SEDIKIT" if count < 100 else "✅"
    print(f"{i:2d} | {name:15s} | {count:5d} | {bar} {status}")

# Plot
counts = [counter.get(i, 0) for i in range(len(class_names))]
colors = ['red' if c < 100 else 'steelblue' for c in counts]

plt.figure(figsize=(16, 6))
plt.bar(class_names, counts, color=colors)
plt.xticks(rotation=45, ha='right')
plt.title("Distribusi Data per Kelas (Merah = < 100 sampel)")
plt.tight_layout()
plt.savefig("distribusi_kelas.png")
print("\nGrafik disimpan: distribusi_kelas.png")