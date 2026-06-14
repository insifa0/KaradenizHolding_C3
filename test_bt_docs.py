from src.database import parse_data_file

docs = parse_data_file()
print("BT Documents and their Access Levels:")
for d in docs:
    if "BT-" in d.metadata["Dokuman_ID"]:
        print(f"{d.metadata['Dokuman_ID']}: {d.metadata['Erisim_Yetkisi']} | {d.metadata['Dokuman_Adi']}")
