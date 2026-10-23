---
layout: post
title: "Oyun Seni İzliyor: Dynamic Difficulty Adjustment Nasıl Çalışır?"
math: true
categories: 
  - Bilgi
tags: 
  - oyun geliştirme
  - dda
  - yapay zeka
  - oyuncu deneyimi
  - python
  - oyun tasarımı
toc: true
image: /img/oyun-seni-izliyor-79.png
---

Bir bölümde art arda yenildiğinizde düşmanların gizlice yavaşladığını veya oyunu rahatça geçtiğinizde rakiplerin birden akıllandığını düşündünüz mü? Bu değişim her zaman hayal gücünüzün ürünü değildir. Dynamic Difficulty Adjustment, yani Dinamik Zorluk Ayarlama (DDA), oyuncunun performansını izleyip oyunun zorluk seviyesini gerçek zamanlı olarak değiştiren bir tasarım yaklaşımıdır.

![oyun-seni-izliyor-79](/img/oyun-seni-izliyor-79.svg)

``

## DDA neden kullanılır?

Geleneksel oyunlarda oyuncu başlangıçta kolay, normal veya zor gibi sabit bir seviye seçer. Ancak bir oyuncunun nişan alma becerisi iyi, kaynak yönetimi kötü olabilir. Üstelik beceri seviyesi oyun boyunca değişir. Sabit seçim, bu farklılıkları yakalamakta yetersiz kalır.

DDA'nın temel amacı oyuncuyu **akış bölgesinde** tutmaktır. Akış teorisine göre görev çok kolaysa sıkılma, çok zorsa kaygı oluşur. İdeal durumda zorluk $D$, oyuncu becerisi $S$ değerine yakın olmalıdır:

$$D \approx S$$

Aradaki fark büyüdükçe deneyim bozulabilir. Bunu basit bir denge hatasıyla gösterebiliriz:

$$E = S - D$$

$E$ büyük ve pozitifse oyun kolay, büyük ve negatifse oyun zor demektir. Sistem, $E$ değerini sıfıra yaklaştırmaya çalışır.

| Yaklaşım | Zorluk değişimi | Avantajı | Riski |
|---|---|---|---|
| Sabit seviye | Oyuncu seçer | Şeffaf ve öngörülebilir | Yanlış seçim deneyimi bozabilir |
| Kademeli ilerleme | Bölümlere göre artar | Tasarlanması kolaydır | Her oyuncuya aynı davranır |
| DDA | Performansa göre değişir | Kişiselleştirilmiş deneyim sunar | Fark edilirse yapay hissedilebilir |

## Sistem oyuncuyu nasıl ölçer?

Önce anlamlı sinyaller toplanır. Ölüm sayısı, isabet oranı, bölüm tamamlama süresi, kalan sağlık, kullanılan yardım miktarı ve başarısız deneme sayısı bunlardan bazılarıdır. Tek bir ölçüte güvenmek yanıltıcıdır; hızlı oynayan biri dikkatsiz, yavaş oynayan biri ise keşif meraklısı olabilir.

Ölçümler normalize edilerek birleşik bir beceri puanı üretilebilir:

$$S = 0.4A + 0.3H + 0.3T$$

Burada $A$ isabet oranını, $H$ hayatta kalma başarısını, $T$ ise hedef süreye göre performansı temsil eder. Katsayılar oyunun önceliklerine göre değiştirilir.

## Basit bir uygulama

Aşağıdaki Python sınıfı, son performans puanlarının ortalamasını alır ve hedef zorluğu küçük adımlarla günceller:

```python
class DifficultyManager:
    def __init__(self):
        self.difficulty = 0.5
        self.history = []

    def update(self, accuracy, survival, speed):
        score = 0.4 * accuracy + 0.3 * survival + 0.3 * speed
        self.history.append(score)
        self.history = self.history[-5:]

        skill = sum(self.history) / len(self.history)
        change = (skill - self.difficulty) * 0.2
        self.difficulty = max(0.1, min(1.0, self.difficulty + change))
        return self.difficulty
```

Son beş sonucun kullanılması, tek bir kötü maçın sistemi paniğe sürüklemesini engeller. `0.2` katsayısı değişimin hızını sınırlar; böylece düşmanlar bir anda salyangozdan terminatöre dönüşmez. Döndürülen değer düşman sağlığına, yapay zekâ tepki süresine veya kaynak miktarına uygulanabilir.

## Neler ayarlanabilir?

| Parametre | Düşük zorlukta | Yüksek zorlukta |
|---|---|---|
| Düşman sağlığı | Daha az | Daha fazla |
| Tepki süresi | Daha yavaş | Daha hızlı |
| Kaynaklar | Daha bol | Daha kıt |
| İpucu sıklığı | Daha fazla | Daha az |
| Rakip taktikleri | Basit | Koordineli |

İyi bir DDA sistemi hile yapıyormuş gibi görünmemelidir. Oyuncu sırf başarılı olduğu için kurşunlarının sebepsiz yere kaçtığını hissederse sistem güven kaybeder. Bu nedenle değişiklikler yumuşak, sınırlı ve mümkünse oyun dünyası içinde anlamlı olmalıdır.

Sonuç olarak DDA yalnızca düşmanların canını artıran bir düğme değildir; ölçüm, modelleme ve deneyim tasarımının birleşimidir. En başarılı sistem oyuncuyu cezalandırmaz veya kayırmaz. Onun becerisine uygun, heyecanlı ve adil görünen bir mücadeleyi sessizce sahneye koyar.
