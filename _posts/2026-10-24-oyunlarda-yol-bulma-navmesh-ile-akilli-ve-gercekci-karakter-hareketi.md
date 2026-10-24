---
layout: post
title: "Oyunlarda Yol Bulma: NavMesh ile Akıllı ve Gerçekçi Karakter Hareketi"
math: true
categories: 
  - Bilgi
tags: 
  - navmesh
  - oyun geliştirme
  - yol bulma
  - yapay zeka
  - a-star
  - unity
toc: true
image: /img/oyunlarda-yol-bulma-29.png
---

Bir düşmanın oyuncuyu kovalarken duvara sürtünmesi, masanın arkasında çaresizce dönmesi veya uçurumdan aşağı atlaması komik görünebilir; ancak oyuncunun dünyaya olan inancını hızla yok eder. Navigasyon ağı, yani **NavMesh**, yürünebilir alanları geometrik bir haritaya dönüştürerek oyun karakterlerinin karmaşık ortamlarda mantıklı ve gerçekçi rotalar bulmasını sağlar.

``

## NavMesh tam olarak nedir?

NavMesh, oyun dünyasının karakterler tarafından yürünebilen bölümlerini temsil eden, birbirine bağlı dışbükey çokgenlerden oluşur. Haritanın tamamını küçük karelere bölmek yerine yalnızca geçilebilir yüzeyleri saklar. Böylece duvarlar, uçurumlar ve kapalı alanlar doğal biçimde navigasyon verisinin dışında kalır.

Çokgenlerin dışbükey olması önemlidir: Aynı dışbükey çokgen içindeki herhangi iki nokta arasında çizilen doğru, çokgenin dışına çıkmaz. Dolayısıyla karakter, aynı bölgede ek bir engel kontrolüne ihtiyaç duymadan ilerleyebilir.

| Yaklaşım | Temsil biçimi | Avantajı | Dezavantajı |
|---|---|---|---|
| Grid | Kare hücreler | Oluşturması kolaydır | Büyük haritalarda pahalıdır |
| Waypoint | Bağlı noktalar | Tasarımcı kontrolü yüksektir | Bakımı zahmetlidir |
| NavMesh | Dışbükey çokgenler | Doğal ve verimli rotalar üretir | Dinamik değişiklikler karmaşıktır |

![oyunlarda-yol-bulma-29](/img/oyunlarda-yol-bulma-29.svg)


## Yol nasıl hesaplanır?

NavMesh oluşturulduktan sonra her çokgen bir grafik düğümü, komşu çokgenler arasındaki geçişler ise kenar kabul edilir. Başlangıç ve hedef noktalarının bulunduğu çokgenler belirlenir; ardından çoğunlukla **A\*** algoritması çalıştırılır.

A\* her aday için şu değeri kullanır:

$$f(n) = g(n) + h(n)$$

Burada $g(n)$ başlangıçtan mevcut düğüme kadar ödenen gerçek maliyet, $h(n)$ ise hedefe kalan tahmini maliyettir. Öklid uzaklığı sık kullanılan bir sezgiseldir:

$$h(n) = \sqrt{(x_h-x_n)^2 + (z_h-z_n)^2}$$

Algoritmanın bulduğu çokgen dizisi henüz kusursuz bir hareket rotası değildir. Çokgen geçitlerinin ortalarından yürümek zikzak oluşturabilir. Bu nedenle **Funnel (huni) algoritması**, geçitler arasında gerilmiş hayali bir ipi sıkıştırarak daha kısa ve düzgün köşe noktaları üretir.

## Basit bir A\* maliyet örneği

Aşağıdaki sözde kod, en düşük toplam tahmine sahip düğümün nasıl seçildiğini gösterir:

```text
openSet içine başlangıç düğümünü ekle

openSet boş değilken:
    current = en düşük f değerli düğüm

    eğer current hedef ise:
        yolu geriye doğru oluştur

    current düğümünü kapat

    her komşu için:
        yeniMaliyet = current.g + geçişMaliyeti
        eğer yeniMaliyet komşu.g değerinden küçükse:
            komşu.parent = current
            komşu.g = yeniMaliyet
            komşu.f = komşu.g + heuristic(komşu, hedef)
```

Geçiş maliyeti yalnızca mesafe olmak zorunda değildir. Çamur, merdiven veya tehlikeli bölgeler farklı katsayılarla ağırlıklandırılabilir:

$$maliyet = mesafe \times yüzeyKatsayısı$$

Örneğin taş yolun katsayısı $1$, bataklığın katsayısı $4$ ise karakter, biraz daha uzun olsa bile kuru yolu tercih edebilir. Böylece rota yalnızca kısa değil, davranış açısından anlamlı olur.

## Gerçekçilik için yerel kaçınma

NavMesh küresel rotayı bulur; fakat hareket eden diğer karakterleri tek başına çözmez. **Local avoidance**, karakterlerin hız vektörlerini geçici olarak değiştirerek çarpışmaları önler. NavMesh “hangi koridordan gitmeliyim?” sorusunu, yerel kaçınma ise “önümdeki askere çarpmadan nasıl geçerim?” sorusunu yanıtlar.

| Sistem | Sorumluluk | Çalışma sıklığı |
|---|---|---|
| A\* | Genel rota bulma | Gerektiğinde |
| Funnel | Rotayı düzleştirme | Rota üretildiğinde |
| Local avoidance | Hareketli engellerden kaçma | Genellikle her karede |

Kapılar, yıkılan köprüler ve asansörler için **off-mesh link** kullanılabilir. Bu bağlantılar yürüme yüzeyleri arasında zıplama, tırmanma veya özel animasyon gerektiren geçişler tanımlar. Büyük dünyalarda ise NavMesh parçalara ayrılarak yalnızca oyuncuya yakın bölgeler bellekte tutulabilir.

İyi bir NavMesh sistemi görünmezdir: Oyuncu algoritmayı fark etmez, yalnızca karakterlerin akıllıca davrandığını hisseder. Başarının sırrı; doğru geometri, uygun maliyetler, düzgün rota sadeleştirme ve yerel kaçınmayı birlikte kullanmaktır.
