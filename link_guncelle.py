import os

hedef_klasor = "."
gecerli_uzantilar = (".md", ".markdown", ".html")

# SADECE dosya adlarını değiştiriyoruz. Metinleri korumak için birebir eşleşme kullanıyoruz.
degisim_sozlugu = {
    "Linux Komut Satırı.pdf": "linux-komut-satiri.pdf",
    "Linux%20Komut%20Satırı.pdf": "linux-komut-satiri.pdf", # URL kodlu boşluk ihtimaline karşı
    "Algoritma-analizi-çalışma-zamanı-veri-boyutu.png": "algoritma-analizi-calisma-zamani-veri-boyutu.png",
    "big-o-notasyonu-karesel-döngü.png": "big-o-notasyonu-karesel-dongu.png",
    "big-o-notasyonu-lineer-döngü.png": "big-o-notasyonu-lineer-dongu.png",
    "big-o-notasyonu-lineer-logaritmik-döngü.png": "big-o-notasyonu-lineer-logaritmik-dongu.png",
    "big-o-notasyonu-logaritmik-döngü.png": "big-o-notasyonu-logaritmik-dongu.png",
    "compoundInterest.png": "bilesik-faiz.png",
    "LICENSE.md": "lisans.md"
}

degisen_dosya_sayisi = 0
toplam_degisiklik = 0

print("Görsel ve PDF linkleri güncelleniyor...\n")

for root, dirs, files in os.walk(hedef_klasor):
    # Geçici ve sistem klasörlerini atla
    if "_site" in dirs:
        dirs.remove("_site")
    if ".git" in dirs:
        dirs.remove(".git")

    for file in files:
        if file.endswith(gecerli_uzantilar):
            dosya_yolu = os.path.join(root, file)

            try:
                with open(dosya_yolu, 'r', encoding='utf-8') as f:
                    icerik = f.read()

                yeni_icerik = icerik
                dosya_degisti_mi = False

                for eski_isim, yeni_isim in degisim_sozlugu.items():
                    if eski_isim in icerik:
                        degisiklik_sayisi = icerik.count(eski_isim)
                        yeni_icerik = yeni_icerik.replace(eski_isim, yeni_isim)
                        toplam_degisiklik += degisiklik_sayisi
                        dosya_degisti_mi = True

                if dosya_degisti_mi:
                    with open(dosya_yolu, 'w', encoding='utf-8') as f:
                        f.write(yeni_icerik)
                    print(f"Güncellendi: {dosya_yolu}")
                    degisen_dosya_sayisi += 1

            except Exception as e:
                print(f"Hata atlandı ({dosya_yolu}): {e}")

print("\n" + "-" * 40)
print(f"İşlem Tamam! Toplam {degisen_dosya_sayisi} dosyada, {toplam_degisiklik} adet görsel/PDF linki güncellendi.")
print("-" * 40)