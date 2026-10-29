---
layout: post
title: "Afet Anında En Güvenli Yol: Tahliye Rotası Optimizasyonu"
math: true
categories: 
  - Proje
tags: 
  - algoritma
  - optimizasyon
  - afet yönetimi
  - graf teorisi
  - python
  - yapay zeka
toc: true
image: /img/afet-aninda-en-29.png
---

![afet-aninda-en-29](/img/afet-aninda-en-29.svg)


Bir deprem ya da sel sırasında en kısa yol, her zaman en güvenli yol değildir. Normalde beş dakikada geçilen bir cadde yıkılmış binalar, yükselen su, yangın veya yoğun insan kalabalığı nedeniyle ölümcül hâle gelebilir. Tahliye rotası optimizasyonu; yol uzunluğunu, tehlike seviyesini, kapasiteyi ve sürekli değişen çevre koşullarını birlikte değerlendirerek insanları güvenli bölgelere yönlendirmeyi amaçlar.
``

## Şehri bir graf olarak düşünmek

Algoritmik çözümün temelinde **graf teorisi** bulunur. Bir şehir haritası, düğümler ve kenarlardan oluşan bir graf şeklinde modellenebilir. Kavşaklar, binalar, toplanma alanları ve köprüler birer düğüm; bunları birbirine bağlayan yollar ise kenardır.

Her yolun yalnızca uzunluğu değil, afet koşullarındaki riski de hesaba katılmalıdır. Bir kenarın toplam maliyeti şu şekilde tanımlanabilir:

$$
C(e) = \alpha D(e) + \beta R(e) + \gamma T(e) + \delta K(e)
$$

Burada $D(e)$ mesafeyi, $R(e)$ tehlike puanını, $T(e)$ tahmini geçiş süresini, $K(e)$ ise kalabalık veya kapasite maliyetini temsil eder. $\alpha$, $\beta$, $\gamma$ ve $\delta$ katsayıları hangi ölçütün daha önemli olduğunu belirler. Örneğin sel sırasında risk katsayısı yükseltilerek su basmış kısa yolların tercih edilmesi engellenebilir.

| Ölçüt | Normal navigasyon | Afet navigasyonu |
|---|---|---|
| Ana hedef | En kısa veya hızlı yol | En güvenli uygulanabilir yol |
| Yol maliyeti | Mesafe ve trafik | Risk, hasar, kapasite ve süre |
| Veri değişimi | Görece yavaş | Saniyeler içinde değişebilir |
| Rota yaklaşımı | Genellikle tek rota | Alternatif ve yedek rotalar |
| Kritik sonuç | Gecikme | Can güvenliği |

## Hangi algoritma kullanılmalı?

Pozitif maliyetli yollar için **Dijkstra algoritması**, başlangıç noktasından en düşük toplam maliyetli rotayı bulabilir. **A\*** algoritması ise hedefe olan tahmini uzaklığı sezgisel bilgi olarak kullanır ve büyük haritalarda aramayı hızlandırır. Ancak afet sırasında tek bir kişinin rotasını bulmak yeterli değildir. Binlerce kişinin aynı dar köprüye yönlendirilmesi, teoride güvenli görünen yolu pratikte kullanılamaz hâle getirebilir.

Bu nedenle çoklu tahliye problemlerinde maksimum akış, minimum maliyetli akış ve zaman bağımlı graf modelleri kullanılabilir. Yol kapasitesi doldukça maliyetin yükseltilmesi, algoritmanın insanları farklı güzergâhlara dağıtmasını sağlar.

Aşağıdaki Python örneği, tehlike puanını ve mesafeyi birleştirerek güvenli rotayı hesaplar:

```python
import networkx as nx

G = nx.Graph()

# Mesafe kilometre, risk ise 0 ile 10 arasındadır.
yollar = [
    ("A", "B", 2.0, 1),
    ("B", "D", 2.5, 8),  # Hasarlı köprü
    ("A", "C", 3.0, 2),
    ("C", "D", 3.0, 1),
]

for baslangic, bitis, mesafe, risk in yollar:
    maliyet = mesafe + 4 * risk
    G.add_edge(baslangic, bitis, weight=maliyet)

rota = nx.shortest_path(G, "A", "D", weight="weight")
toplam = nx.shortest_path_length(G, "A", "D", weight="weight")

print("Güvenli rota:", " -> ".join(rota))
print("Toplam maliyet:", toplam)
```

Kodda risk, mesafeden dört kat daha etkili olacak biçimde ağırlıklandırılmıştır. Böylece kısa olmasına rağmen hasarlı köprüden geçen `A-B-D` rotası yerine daha uzun fakat güvenli `A-C-D` rotası seçilebilir.

## Dinamik veriler neden önemlidir?

Afet haritaları sabit değildir. Deprem artçıları yeni yolları kapatabilir; sel suyu birkaç dakika içinde yükselebilir. Sensörler, uydu görüntüleri, dronlar, belediye verileri ve vatandaş bildirimleri grafın kenar maliyetlerini gerçek zamanlı güncelleyebilir. Bir yol kapanırsa kenar silinir; risk artarsa maliyeti yükseltilir ve rota yeniden hesaplanır.

Yine de sistem yalnızca algoritmadan ibaret değildir. Hatalı sensör verileri doğrulanmalı, internet kesintisine karşı çevrimdışı haritalar hazırlanmalı ve engelli bireyler için erişilebilir rotalar üretilmelidir. Başarılı bir tahliye sistemi, matematiksel olarak iyi bir yol bulmanın yanında belirsizliğe dayanıklı, anlaşılır ve adil olmalıdır. Çünkü afet anında algoritmanın gerçek başarısı birkaç saniye kazanmak değil, mümkün olduğunca çok insanı güvenle hedefe ulaştırmaktır.
