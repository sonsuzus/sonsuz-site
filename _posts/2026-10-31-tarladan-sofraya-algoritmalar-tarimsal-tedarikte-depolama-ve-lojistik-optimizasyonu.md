---
layout: post
title: "Tarladan Sofraya Algoritmalar: Tarımsal Tedarikte Depolama ve Lojistik Optimizasyonu"
math: true
categories: 
  - Bilgi
tags: 
  - tarım
  - tedarik zinciri
  - optimizasyon
  - simülasyon
  - lojistik
  - python
toc: true
image: /img/tarladan-sofraya-algoritmalar-10.png
---

Bir kamyon domatesin yanlış depoya gitmesi, yalnızca fazladan yakıt tüketmek değildir: gecikme, bozulma ve karşılanamayan siparişler de faturaya eklenir. Tarımsal üretim zinciri simülasyonları, bu birbirine bağlı kararları bilgisayar ortamında deneyerek daha iyi planlar geliştirmemizi sağlar. Amaç, ürünleri sadece taşımak değil; doğru miktarı, doğru zamanda, uygun koşullarda müşteriye ulaştırmaktır.

``

## Problemin matematiksel iskeleti

Tedarik ağını bir grafik olarak düşünelim: çiftlikler, depolar ve müşteriler düğümleri; taşıma bağlantıları ise kenarları oluşturur. Her bağlantının maliyeti, kapasitesi ve yolculuk süresi vardır. Tarımsal ürünleri sıradan paketlerden ayıran kritik özellik, zaman geçtikçe miktarlarının veya kalitelerinin azalmasıdır. Domates, depoda beklerken yazılım güncellemesi almaz; raf ömrünü tüketir!

Karar değişkenlerimiz depoya giren ürün $x_{wt}$, müşteriye gönderilen miktar $y_{wmt}$ ve dönem sonu stoku $I_{wt}$ olsun. Depodaki dönemsel kayıp oranı $r_w$ ise basitleştirilmiş stok dengesi şöyledir:

$$I_{wt}=(1-r_w)(I_{w,t-1}+x_{wt})-\sum_m y_{wmt}$$

Bu denklem, kaybın sevkiyattan önce gerçekleştiğini varsayar. Gerçekte kayıp zamana, sıcaklığa ve ürün yaşına bağlı olabilir. Dolayısıyla dönem uzunluğu ve işlem sırası, modelin doğruluğunu doğrudan etkiler.

Toplam maliyet; taşıma, stok tutma, depo açma ve karşılanamayan talep cezalarını kapsar:

$$\min C_{taşıma}+C_{stok}+C_{depo}+C_{eksik}$$

Depo kullanımı ikili değişkenle gösterildiğinde problem, karma tamsayılı doğrusal programlama modeline dönüşür. Ayrıca üretim miktarı, depo kapasitesi ve talep dengesi için kısıtlar gerekir. Bunlar olmadan algoritma, hayali ürünleri hayali depolardan gönderebilir.

| Karar yaklaşımı | Avantajı | Sınırlılığı |
|---|---|---|
| En yakın depoyu seçmek | Hızlı ve anlaşılır | Kapasiteyi ve kayıpları birlikte değerlendirmez |
| En ucuz rotayı seçmek | Yerel maliyeti azaltır | Ağın toplam maliyetini artırabilir |
| Karma tamsayılı model | Kararları birlikte değerlendirir | Büyük örneklerde çözüm süresi uzayabilir |

## Simülasyon neden gerekli?

Optimizasyon, verilen koşullarda bir plan üretir. Simülasyon ise o planın gerçekçi belirsizlikler altında nasıl davrandığını sınar. Ya hasat beklenenden düşük çıkarsa? Ya soğutma sistemi arızalanırsa? Ya trafik teslimatı geciktirirse?

Talep, verim ve seyahat süresi için senaryolar oluşturup aynı planı tekrar çalıştırabiliriz. Özellikle bu değişkenlerin ilişkilerini korumak önemlidir: sıcak hava hem talebi hem bozulmayı artırabilir. Bağımsız rastgele örnekleme, böyle ortak riskleri gözden kaçırabilir.

## Python ile küçük bir karar modeli

Aşağıdaki PuLP örneği, ortak bir kaynaktaki 160 ton ürünü iki depo üzerinden iki müşteriye dağıtır. Maliyetler para birimi/ton, depo açma bedelleri ise sabit tutardır. Çalıştırmadan önce `pip install pulp` komutuyla kütüphaneyi kurabilirsiniz.

```python
import pulp as p

W, M = ['K', 'G'], ['A', 'B']
demand = {'A': 90, 'B': 60}
loss = {'K': 0.05, 'G': 0.02}
inbound = {'K': 2, 'G': 3}
route = {('K', 'A'): 1, ('K', 'B'): 4,
         ('G', 'A'): 3, ('G', 'B'): 1}
model = p.LpProblem('TarimsalTedarik', p.LpMinimize)
x = p.LpVariable.dicts('giris', W, lowBound=0)
y = p.LpVariable.dicts('sevkiyat', route, lowBound=0)
stock = p.LpVariable.dicts('stok', W, lowBound=0)
short = p.LpVariable.dicts('eksik', M, lowBound=0)
opened = p.LpVariable.dicts('acik', W, cat='Binary')

model += (
    p.lpSum(inbound[w]*x[w] + 0.5*stock[w]
            + 25*opened[w] for w in W)
    + p.lpSum(route[k]*y[k] for k in route)
    + 80*p.lpSum(short.values())
)
model += p.lpSum(x.values()) <= 160
for w in W:
    model += x[w] <= 100*opened[w]
    model += stock[w] == (1-loss[w])*x[w] - p.lpSum(
        y[w, m] for m in M)
for m in M:
    model += p.lpSum(y[w, m] for w in W) + short[m] == demand[m]

model.solve(p.PULP_CBC_CMD(msg=False))
print(p.LpStatus[model.status])
if model.status == p.LpStatusOptimal:
    print('Toplam maliyet:', p.value(model.objective))
    print({k: v.value() for k, v in y.items()})
```

Model, kapasiteyi depo açma kararıyla bağlar; kapalı depoya ürün gönderilemez. Eksik talep değişkeni, ürün yetersizliğinde problemi çözümsüz bırakmak yerine hizmet kaybını maliyetlendirir. Ancak ceza katsayısı keyfî seçilmemeli, ticari sonuçlarla gerekçelendirilmelidir.

Bu tek dönemli örnekte başlangıç stoku sıfırdır. Gelecek talep bulunmadığından fazla stok tutmak cazip değildir. Gerçek depolama stratejisi için dönemler, başlangıç stokları, ürün yaşları ve hasat takvimi eklenmelidir.

## Başarıyı yalnızca maliyetle ölçmeyin

| Ölçüt | Gösterdiği durum |
|---|---|
| Talep karşılama oranı | Müşteri hizmetinin sürekliliği |
| Bozulan ürün miktarı | Fiziksel kayıp ve sürdürülebilirlik |
| Kapasite kullanımı | Depolardaki darboğazlar |
| Teslimat gecikmesi | Planın operasyonel uygulanabilirliği |

Son adım, optimize edilmiş planı basit kurallarla aynı senaryolarda karşılaştırmaktır. Ortalama sonuçların yanında kötü senaryoları da inceleyin. En ucuz plan, küçük bir aksaklıkta dağılıyorsa iyi plan değildir. Başarılı algoritma, tarlanın belirsizliğini yok saymaz; onu kararların içine taşır.

![tarladan-sofraya-algoritmalar-10](/img/tarladan-sofraya-algoritmalar-10.svg)

