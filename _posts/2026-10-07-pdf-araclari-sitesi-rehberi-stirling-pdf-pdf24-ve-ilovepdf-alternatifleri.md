---
layout: post
title: "PDF Araçları Sitesi Rehberi: Stirling PDF, PDF24 ve iLovePDF Alternatifleri"
math: true
categories: 
  - Bilgi
tags: 
  - pdf
  - açık kaynak
  - docker
  - ocr
  - web araçları
  - gizlilik
toc: true
image: /img/pdf-araclari-sitesi-32.png
---

PDF birleştirmek için ayrı, sıkıştırmak için ayrı, imzalamak için bambaşka bir site kullanmak kısa sürede tarayıcı sekmesi koleksiyonculuğuna dönüşebilir. Stirling PDF, PDF24 ve iLovePDF bu sorunu çözen popüler araçlar olsa da gizlilik, çevrimdışı kullanım, açık kaynak desteği veya otomasyon ihtiyacı bizi farklı seçeneklere yöneltebilir.


![pdf-araclari-sitesi-32](/img/pdf-araclari-sitesi-32.svg)

``

## Önce PDF araçlarının mantığını anlayalım

PDF, yalnızca metin içeren bir belge değildir; yazı tiplerini, vektörel çizimleri, görselleri, form alanlarını ve sayfa koordinatlarını aynı kapsayıcıda saklayabilir. Bu nedenle “PDF küçültme” işlemi çoğunlukla metni sıkıştırmaktan ziyade görsellerin çözünürlüğünü düşürmek, gereksiz nesneleri temizlemek ve yazı tiplerini alt kümelere ayırmak anlamına gelir.

Bir sıkıştırma işleminin başarısı şu oranla ölçülebilir:

$$
R = \frac{S_{eski} - S_{yeni}}{S_{eski}} \times 100
$$

Örneğin 20 MB büyüklüğündeki dosya 8 MB’ye düşürülürse kazanç $R=60\%$ olur. Ancak yüksek oran her zaman iyi sonuç değildir; agresif JPEG sıkıştırması küçük dosya karşılığında bulanık metin üretebilir.

OCR ise taranmış sayfalardaki pikselleri harflere dönüştürür. Böylece belge aranabilir ve kopyalanabilir hâle gelir. Türkçe belgelerde aracın `tur` dil modelini desteklemesi doğruluk açısından önemlidir.

## Popüler alternatiflerin karşılaştırması

| Araç | Çalışma şekli | Güçlü yönü | Uygun olduğu senaryo |
|---|---|---|---|
| PDFsam Basic | Masaüstü, açık kaynak | Birleştirme ve bölme | Dosyayı internete yüklemek istemeyenler |
| Sejda PDF | Web ve masaüstü | Kullanıcı dostu düzenleme | Arada sırada hızlı işlem yapanlar |
| qpdf | Komut satırı | Şifreleme ve sayfa yönetimi | Otomasyon ve sunucu işlemleri |
| Ghostscript | Komut satırı | Dönüştürme ve sıkıştırma | Gelişmiş optimizasyon |
| OCRmyPDF | Komut satırı, açık kaynak | Aranabilir PDF üretme | Taranmış arşivler |
| Gotenberg | Docker tabanlı API | HTML/Office dosyalarını PDF’ye çevirme | Kendi PDF servisini geliştirenler |

PDFsam, PDF24’ün masaüstü yaklaşımına iyi bir alternatiftir ancak düzenleme özellikleri daha sınırlıdır. Sejda, iLovePDF benzeri rahat bir arayüz sunar; ücretsiz sürümünde işlem sınırları bulunur. qpdf ve Ghostscript ise süslü düğmeler yerine terminal sunar, fakat toplu işlemlerde gerçek birer iş makinesidir.

## Gizlilik mi, kullanım kolaylığı mı?

Çevrimiçi bir servise yüklenen sözleşme, kimlik fotokopisi veya finansal rapor üçüncü taraf sunuculardan geçebilir. Servis dosyaları kısa süre sonra sildiğini söylese bile kurum politikaları buna izin vermeyebilir. Hassas belgelerde masaüstü veya self-hosted çözüm kullanmak daha güvenlidir.

Seçim yaparken şu ölçütleri değerlendirin:

- Dosyalar sunucuya yükleniyor mu?
- Otomatik silme süresi açıkça belirtilmiş mi?
- Araç çevrimdışı çalışabiliyor mu?
- Kaynak kodu denetlenebiliyor mu?
- OCR, parola ve elektronik imza desteği var mı?
- Günlük işlem veya dosya boyutu sınırı uygulanıyor mu?

## Terminalde küçük bir PDF araç kutusu

Linux üzerinde qpdf ve OCRmyPDF ile basit bir iş akışı kurulabilir:

```bash
# Seçilen sayfaları tek belgede birleştirir
qpdf --empty --pages rapor.pdf 1-3 ek.pdf 2 -- birlesik.pdf

# Taranmış belgeye Türkçe OCR katmanı ekler
ocrmypdf -l tur --deskew birlesik.pdf aranabilir.pdf

# Sonucu 128 bit parola ile korur
qpdf --encrypt kullanici-parolasi yonetici-parolasi 128 -- \
  aranabilir.pdf guvenli.pdf
```

İlk komut farklı belgelerden sayfa seçer. `--deskew`, eğri taranmış sayfaları düzeltmeye çalışır. Son komut ise PDF’yi şifreler; parolaları doğrudan betiğe yazmak yerine ortam değişkenlerinden okumak daha güvenlidir.

## Kendi PDF sitesini kurmak isteyenlere

Bir PDF araçları sitesinin temel mimarisi; yükleme arayüzü, işlem kuyruğu, izole çalışan dönüştürme servisleri ve süreli dosya depolamasından oluşur. Gotenberg dönüşüm API’si, OCRmyPDF metin tanıma, qpdf ise sayfa ve parola işlemleri için kullanılabilir. İşleri kuyruklamak büyük dosyaların web sunucusunu kilitlemesini engeller.

Dosya türünü yalnızca uzantıdan doğrulamamak, işlem sürelerini sınırlamak ve yüklenen belgeleri rastgele adlarla saklamak kritik güvenlik önlemleridir. Kısacası kolay kullanım için Sejda, çevrimdışı işlemler için PDFsam, otomasyon için qpdf ve OCR için OCRmyPDF güçlü alternatiflerdir. Tam kontrol isteyenlerse bu araçları birleştirerek kendi mahremiyet odaklı PDF platformunu oluşturabilir.
