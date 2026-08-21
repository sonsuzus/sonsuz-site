import os
import re
import random
import glob

POSTS_DIR = "_posts"
IMG_DIR = "img"

# Senin yazdığın Markdown içi SVG ekleme fonksiyonu
def resim_etiketini_ekle(dosya_yolu, resim_adi):
    with open(dosya_yolu, 'r', encoding='utf-8') as f:
        satirlar = f.readlines()
        
    ekleme_noktalari = []
    tire_sayaci = 0
    
    for i, satir in enumerate(satirlar):
        if satir.strip() == '---':
            tire_sayaci += 1
            if tire_sayaci == 2:
                ekleme_noktalari.append(i + 1)
                break
                
    for i, satir in enumerate(satirlar):
        if satir.strip() == '```':
            ekleme_noktalari.append(i)
            break
            
    tablo_icinde = False
    for i, satir in enumerate(satirlar):
        if '|' in satir:
            tablo_icinde = True
        elif tablo_icinde and satir.strip() == '':
            ekleme_noktalari.append(i)
            break
            
    ekleme_noktalari.append(len(satirlar))
    secilen_satir = random.choice(list(set(ekleme_noktalari)))
    
    etiket = f"\n![{resim_adi.replace('.svg', '')}](/img/{resim_adi})\n\n"
    satirlar.insert(secilen_satir, etiket)
    
    with open(dosya_yolu, 'w', encoding='utf-8') as f:
        f.writelines(satirlar)

# Senin yazdığın Front-matter PNG ekleme fonksiyonu
def front_matter_gorsel_ekle(dosya_yolu, png_adi):
    with open(dosya_yolu, 'r', encoding='utf-8') as f:
        satirlar = f.readlines()
        
    tire_sayaci = 0
    for i, satir in enumerate(satirlar):
        if satir.strip() == '---':
            tire_sayaci += 1
            if tire_sayaci == 2:
                satirlar.insert(i, f"image: /img/{png_adi}\n")
                break
                
    with open(dosya_yolu, 'w', encoding='utf-8') as f:
        f.writelines(satirlar)

# Eşleştirme ve Kurtarma Mantığı
def kurtarma_islemi_baslat():
    if not os.path.exists(POSTS_DIR) or not os.path.exists(IMG_DIR):
        print(f"[HATA] {POSTS_DIR} veya {IMG_DIR} klasörü bulunamadı.")
        return

    postlar = glob.glob(os.path.join(POSTS_DIR, "*.md"))
    svg_dosyalari = glob.glob(os.path.join(IMG_DIR, "*.svg"))
    
    if not svg_dosyalari:
        print("[BİLGİ] img klasöründe SVG dosyası bulunamadı.")
        return

    for svg_yolu in svg_dosyalari:
        svg_adi = os.path.basename(svg_yolu)
        png_adi = svg_adi.replace('.svg', '.png')
        
        # Dosya adını parçala ve ilk 3 kelimeyi al (Örn: log-dosyalarinin-arkeolojisi)
        isim_parcalari = svg_adi.replace('.svg', '').split('-')
        if len(isim_parcalari) >= 3:
            arama_anahtari = f"{isim_parcalari[0]}-{isim_parcalari[1]}-{isim_parcalari[2]}"
        else:
            arama_anahtari = "-".join(isim_parcalari[:-1]) # Güvenlik payı
            
        eslesen_post = None
        for post in postlar:
            if arama_anahtari in post:
                eslesen_post = post
                break
                
        if not eslesen_post:
            print(f"[BULUNAMADI] '{svg_adi}' için uygun bir yazı eşleştirilemedi.")
            continue
            
        # Hedef dosyanın zaten görsel barındırıp barındırmadığını kontrol et
        with open(eslesen_post, 'r', encoding='utf-8') as f:
            icerik = f.read()
            
        if re.search(r'^image:\s*["\']?/img/', icerik, re.MULTILINE):
            print(f"[ATLANIYOR] {os.path.basename(eslesen_post)} zaten görsel içeriyor.")
            continue
            
        print(f"[EŞLEŞTİ] {svg_adi} -> {os.path.basename(eslesen_post)}")
        
        try:
            resim_etiketini_ekle(eslesen_post, svg_adi)
            front_matter_gorsel_ekle(eslesen_post, png_adi)
            print("  - Görseller başarıyla enjekte edildi.")
        except Exception as e:
            print(f"  - [HATA] Enjekte işlemi başarısız: {e}")

if __name__ == "__main__":
    kurtarma_islemi_baslat()