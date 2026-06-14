with open("Ornek yapay veri.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

print("Searching for 'şifre' or 'parola' or 'sunucu' or 'altyapı' in Ornek yapay veri.txt:")
for i, line in enumerate(lines, 1):
    lower = line.lower()
    if any(k in lower for k in ["şifre", "parola", "sunucu", "altyapı"]):
        print(f"Line {i}: {line.strip()}")
