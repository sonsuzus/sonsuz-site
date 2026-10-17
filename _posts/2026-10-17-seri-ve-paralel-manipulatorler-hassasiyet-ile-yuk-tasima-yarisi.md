---
layout: post
title: "Seri ve Paralel Manipülatörler: Hassasiyet ile Yük Taşıma Yarışı"
math: true
categories: 
  - Bilgi
tags: 
  - robotik
  - manipülatör
  - seri robot
  - paralel robot
  - hassasiyet
  - mekatronik
toc: true
image: /img/seri-ve-paralel-53.png
---

![seri-ve-paralel-53](/img/seri-ve-paralel-53.svg)


Bir robot kolundan kahve fincanını nazikçe kaldırmasını da otomobil parçasını milimetrik doğrulukla yerleştirmesini de isteyebiliriz. Ancak hassasiyet, yük kapasitesi ve çalışma alanı aynı tasarımda kolayca zirveye çıkmaz. Robotik manipülatörün seri veya paralel kinematik yapıda kurulması, bu mühendislik pazarlığının sonucunu doğrudan belirler.
``

## Temel mimari farkı

**Seri manipülatörde** eklemler ve bağlantılar tabandan uç efektöre kadar zincir şeklinde sıralanır. İnsan kolu ve klasik altı eksenli endüstriyel robotlar bu yapıdadır. Her bağlantı, kendisinden sonra gelen bağlantıları ve yükü taşır.

**Paralel manipülatörde** ise uç platform, tabana birden fazla bağımsız kinematik zincirle bağlanır. Delta robotlar ve Stewart platformları yaygın örneklerdir. Yük, birkaç kol arasında paylaştırıldığı için sistem mekanik açıdan daha rijit davranır.

| Özellik | Seri manipülatör | Paralel manipülatör |
|---|---|---|
| Çalışma alanı | Geniş ve erişilebilir | Daha dar ve geometrik olarak sınırlı |
| Yük taşıma | Görece düşük | Görece yüksek |
| Rijitlik | Düşük veya orta | Yüksek |
| Konum hassasiyeti | Hata birikimine açık | Genellikle yüksek |
| Ters kinematik | Çoğu yapıda zor | Çoğu yapıda daha kolay |
| İleri kinematik | Genellikle kolay | Karmaşık ve çok çözümlü olabilir |

## Hassasiyet neden değişiyor?

Bir manipülatörün küçük eklem hatalarını uç efektör konumuna taşıyan ilişki Jacobian matrisiyle açıklanır:

$$δx = J(q)δq$$

Burada $δq$ eklem konumlarındaki küçük hataları, $J(q)$ Jacobian matrisini, $δx$ ise uç efektörde oluşan konum ve yönelim hatasını temsil eder. Seri robotta her eklemin boşluğu, sensör hatası ve bağlantı esnemesi zincir boyunca birikebilir. Özellikle uzun kollarda küçük bir açısal hata, uç noktada şaşırtıcı derecede büyük doğrusal sapma üretir:

$$δx \approx Lδθ$$

Örneğin bir metrelik kol için $0.001$ radyanlık hata yaklaşık bir milimetrelik sapmaya dönüşebilir. Robotun “neredeyse doğru” açısı, üretim hattı için pek de doğru olmayabilir.

Paralel mimaride kapalı kinematik çevrimler birbirini mekanik olarak sınırlar. Bir bacağın hatası diğer zincirler tarafından kısmen bastırılabilir. Bu durum yüksek tekrarlanabilirlik ve rijitlik sağlar. Bununla birlikte paralel robotlar tekillik bölgelerine yaklaştığında kuvvet veya hız davranışı kötüleşebilir; dolayısıyla yalnızca katalogdaki hassasiyet değeri değil, çalışma noktasındaki Jacobian koşulu da incelenmelidir.

## Yük taşıma ve kuvvet dağılımı

Seri robotta tabana yakın motorlar hem yükü hem de sonraki bağlantıları taşır. Bir eklemde gereken yaklaşık tork şu şekilde düşünülebilir:

$$τ = rF$$

$F$ taşınan kuvvet, $r$ ise kuvvetin ekleme olan dik uzaklığıdır. Kol uzadıkça moment büyür; daha güçlü motor, daha ağır redüktör ve daha kalın bağlantı gerekir. Eklenen ağırlık da önceki eklemlerin yükünü artırarak küçük bir mühendislik kartopu oluşturur.

Paralel robotlarda kuvvet birden fazla bacağa dağıtılır. Aktüatörler çoğu zaman sabit tabana yerleştirilebildiğinden hareketli kütle azalır. Sonuç; yüksek ivme, güçlü taşıma oranı ve daha iyi dinamik performanstır.

Aşağıdaki basit Python örneği, seri bir kolun ilk eklemindeki statik torku yaklaşık olarak hesaplar:

```python
def eklem_torku(yuk_kg, kol_m, kol_kutlesi_kg):
    g = 9.81
    yuk_torku = yuk_kg * g * kol_m
    kol_torku = kol_kutlesi_kg * g * (kol_m / 2)
    return yuk_torku + kol_torku

print(eklem_torku(8, 1.2, 4))  # Newton-metre
```

Fonksiyon, yükün kol ucunda; kol kütlesinin ise ağırlık merkezinde toplandığını varsayar. Gerçek tasarımda ivme, redüktör verimi, güvenlik katsayısı ve bağlantı esnekliği de hesaba katılmalıdır.

## Hangisi seçilmeli?

Geniş erişim, engellerin çevresinden dolaşma ve yüksek yönelim serbestliği gerekiyorsa seri robot daha uygundur. Kaynak, boyama ve genel amaçlı taşıma buna örnektir. Dar bir hacimde yüksek hız, rijitlik, tekrarlanabilirlik veya yüksek yük-kütle oranı aranıyorsa paralel yapı öne çıkar. Elektronik parça dizme, uçuş simülatörü ve hassas işleme platformları bu sınıftadır.

Kısacası seri manipülatör çevik bir jimnastikçi, paralel manipülatör ise koordineli çalışan bir halter takımı gibidir. En iyi tasarım, en güçlü görünen değil; görev uzayını, tekillikleri, hassasiyet bütçesini ve yük çevrimini birlikte karşılayandır.
