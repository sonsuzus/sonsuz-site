---
layout: post
title: "Not Invented Here Sendromu: Tekerleği Yeniden İcat Etmenin Mimari Bedeli"
math: true
categories: 
  - Bilgi
tags: 
  - yazılım mimarisi
  - not invented here
  - teknik borç
  - kütüphane seçimi
  - proje yönetimi
  - mühendislik kültürü
toc: true
image: /img/not-invented-here-29.png
---

Bir ekip düşünün: Kimlik doğrulama için yıllardır kullanılan, güvenlik denetimlerinden geçmiş bir kütüphane masada duruyor. Fakat ekipten biri ayağa kalkıp “Bunu iki haftada kendimiz yazarız!” diyor. Üç ay sonra parola sıfırlama akışı hâlâ bozuk, takvim alev almış ve kimse o iki haftanın hangi gezegende geçtiğini bilmiyor. İşte **Not Invented Here (NIH)** sendromu, dışarıda üretilmiş çözümleri yalnızca “bizim değil” diye küçümseme eğilimidir.

![not-invented-here-29](/img/not-invented-here-29.svg)

``
## NIH sendromunun arkasında ne var?

Her özel çözüm kötü değildir. Bazen mevzuat, performans sınırları veya sıra dışı iş kuralları gerçekten özgün geliştirme gerektirir. NIH sendromu ise teknik zorunluluktan değil; kontrol arzusu, ego, öğrenme heyecanı ya da dış bağımlılıklara karşı ölçüsüz güvensizlikten doğar.

Mühendis açısından sıfırdan yazmak eğlencelidir: Tasarım kararları sizindir, kod tabanı temiz görünür ve öz geçmişe anlatılacak yeni bir hikâye çıkar. Ne var ki şirket, geliştiricilere yalnızca kod üretmeleri için değil, **iş problemi çözmeleri** için ödeme yapar. Kullanıcılar özel yazılmış mesaj kuyruğunu değil, çalışan ürünü satın alır.

| Yaklaşım | Avantaj | Gizli maliyet | Uygun olduğu durum |
|---|---|---|---|
| Hazır kütüphane | Hızlı başlangıç, topluluk testi | Sürüm ve tedarikçi bağımlılığı | Standart problemler |
| Sıfırdan geliştirme | Tam kontrol, özel optimizasyon | Bakım, güvenlik, dokümantasyon | Benzersiz gereksinimler |
| İnce adaptör katmanı | Değiştirilebilirlik, kontrollü entegrasyon | Ek soyutlama | Kritik dış bağımlılıklar |

## “Yazarız, biter” yanılgısı

Bir bileşenin maliyeti yalnızca ilk kodlama süresi değildir. Toplam sahip olma maliyetini kabaca şöyle düşünebiliriz:

$$TCO = G + T + B + D + O + F$$

Burada $G$ geliştirme, $T$ test, $B$ bakım, $D$ dokümantasyon, $O$ operasyon ve $F$ fırsat maliyetidir. NIH kararlarında genellikle yalnızca $G$ tahmin edilir. Oysa üretim hataları, güvenlik yamaları, yeni çalışanların eğitimi ve ekipten ayrılan “tek bilen kişi” toplam maliyeti katlayabilir.

Örneğin üç mühendisin dört hafta boyunca özel bir önbellek sistemi yazdığını varsayalım. Haftalık kişi maliyeti $C$ ise doğrudan maliyet:

$$M = 3 \times 4 \times C = 12C$$

Buna geciken ürün özelliklerinin kaybettirdiği gelir dâhil değildir. Hazır çözümün entegrasyonu iki kişi-hafta sürüyorsa aradaki on kişi-hafta, aslında görünmez bir takvim vergisidir.

## Kararı egodan veriden kurtarmak

Mimari kararlar “Ben bu kütüphaneyi sevmiyorum” düzeyinde kalmamalıdır. Gereksinimler, alternatifler, riskler ve karar gerekçesi bir **Architecture Decision Record (ADR)** içinde kaydedilebilir. Basit bir puanlama bile tartışmayı kişisel alandan çıkarır:

```python
# Alternatifleri ağırlıklı ölçütlerle karşılaştırır.
weights = {"uyum": 0.35, "guvenlik": 0.30, "bakim": 0.20, "hiz": 0.15}

def score(option):
    return sum(option[key] * weight for key, weight in weights.items())

library = {"uyum": 8, "guvenlik": 9, "bakim": 9, "hiz": 8}
custom = {"uyum": 10, "guvenlik": 5, "bakim": 4, "hiz": 3}

print(score(library), score(custom))
```

Bu kod mutlak gerçeği üretmez; varsayımları görünür kılar. Puanların neden verildiği ekipçe tartışılmalı, mümkünse küçük bir **proof of concept** ile doğrulanmalıdır.

## Hazır çözüm de otomatik olarak doğru değildir

“Build versus buy” kararında lisans, güvenlik geçmişi, bakım sıklığı, topluluk büyüklüğü, kilitlenme riski ve performans ölçülmelidir. İki yıldır güncellenmeyen bir paket, ücretsiz görünse bile pahalı bir mirasa dönüşebilir. Benzer biçimde, işin merkezindeki ayırt edici algoritmayı dışarıya bırakmak stratejik hata olabilir.

Sağlıklı ilke şudur: **Standart problemleri standart araçlarla çöz, rekabet avantajı yaratan yerde özgünleş.** Mühendislik olgunluğu her şeyi yazabilmek değil, neyi yazmamayı bilmekle de ölçülür. Tekerleği yeniden icat edecekseniz en azından yolun neden mevcut tekerleklerle geçilemediğini verilerle kanıtlayın; aksi hâlde ürettiğiniz şey yenilik değil, pahalı ve yuvarlanmayan bir daire olabilir.
