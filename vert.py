import glob
import re

for dosya in glob.glob("_posts/*.md"):
    with open(dosya, "r+", encoding="utf-8") as f:
        icerik = f.read()
        
        # \vert sonrasında boşluk (\s) yoksa, bir boşluk ekle
        yeni_icerik = re.sub(r'\\vert(?!\s)', r'\\vert ', icerik)
        
        if icerik != yeni_icerik:
            f.seek(0)
            f.write(yeni_icerik)
            f.truncate()
            print(f"Düzeltildi: {dosya}")

print("Tüm \vert ifadeleri düzeltildi.")