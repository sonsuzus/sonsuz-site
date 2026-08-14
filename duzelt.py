import os
import re

def degistir_matematik_ici(match):
    # Eşleşen tüm matematik bloğunu (dolar işaretleriyle beraber) al
    icerik = match.group(0)
    # Sadece bu bloğun içindeki dik çizgileri  \vert  ile değiştir
    return icerik.replace('|', r' \vert ')

def calistir():
    # Jekyll yazılarının bulunduğu klasör (genellikle _posts)
    # Eğer başka klasörlerde de .md dosyaların varsa burayı '.' yapabilirsin.
    hedef_klasor = '_posts' 
    
    # 1. $$ ... $$ (Çok satırlı) ve 2. $ ... $ (Tek satırlı) blokları yakalayan Regex
    # re.MULTILINE kullanmıyoruz çünkü [\s\S] zaten yeni satırları da kapsar
    pattern = re.compile(r'(\$\$[\s\S]*?\$\$|\$[^$\n]+?\$)', re.DOTALL)
    
    degisen_dosya_sayisi = 0

    for root, dirs, files in os.walk(hedef_klasor):
        for file in files:
            if file.endswith(('.md', '.markdown')):
                dosya_yolu = os.path.join(root, file)
                
                with open(dosya_yolu, 'r', encoding='utf-8') as f:
                    eski_icerik = f.read()
                
                # Regex ile eşleşen blokları degistir_matematik_ici fonksiyonuna gönder
                yeni_icerik = pattern.sub(degistir_matematik_ici, eski_icerik)
                
                # Eğer dosyada bir değişiklik olduysa üzerine yaz
                if eski_icerik != yeni_icerik:
                    with open(dosya_yolu, 'w', encoding='utf-8') as f:
                        f.write(yeni_icerik)
                    print(f"Güncellendi: {dosya_yolu}")
                    degisen_dosya_sayisi += 1
                    
    print(f"\nİşlem tamamlandı. Toplam {degisen_dosya_sayisi} dosya güncellendi.")

if __name__ == '__main__':
    calistir()