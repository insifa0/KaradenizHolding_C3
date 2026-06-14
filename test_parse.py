"""Veri seti parse testi"""
import sys
sys.path.insert(0, ".")

from src.database import parse_data_file

docs = parse_data_file()
print(f"Toplam parse edilen dokuman: {len(docs)}")

types = {}
depts = {}
for d in docs:
    t = d.metadata["Dokuman_Tipi"]
    dp = d.metadata["Departman"]
    types[t] = types.get(t, 0) + 1
    depts[dp] = depts.get(dp, 0) + 1

print(f"Tip dagilimi: {types}")
print(f"Departman dagilimi: {depts}")
print()

# Ornek dokuman
d = docs[5]
print("--- Ornek Dokuman ---")
print(f"ID: {d.metadata['Dokuman_ID']}")
print(f"Ad: {d.metadata['Dokuman_Adi']}")
print(f"Tip: {d.metadata['Dokuman_Tipi']}")
print(f"Dept: {d.metadata['Departman']}")
print(f"Erisim: {d.metadata['Erisim_Yetkisi']}")
print(f"Iliskili: {d.metadata['Iliskili_Dokuman']}")
print(f"Anahtar Kelimeler: {d.metadata['Anahtar_Kelimeler'][:100]}...")
print()
print("--- Icerik Ornegi (ilk 300 karakter) ---")
print(d.page_content[:300])
