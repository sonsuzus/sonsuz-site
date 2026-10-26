---
layout: post
title: "Oyunlarda Bulanık Mantık: Düşman Yapay Zekâsı Nasıl Karar Verir?"
math: true
categories: 
  - Bilgi
tags: 
  - bulanık mantık
  - oyun yapay zekâsı
  - fuzzy logic
  - oyun geliştirme
  - karar sistemleri
toc: true
image: /img/oyunlarda-bulanik-mantik-94.png
---

![oyunlarda-bulanik-mantik-94](/img/oyunlarda-bulanik-mantik-94.svg)


Bir düşmanın sizi gördüğü anda saldırması, canı yüzde 30’a düşünce kaçması ve diğer bütün durumlarda beklemesi kolay programlanır; ancak pek doğal görünmez. Gerçek hayattaki kararlar keskin eşiklerden çok belirsiz değerlendirmelere dayanır. Oyunlarda kullanılan bulanık mantık, düşmanların “yakın”, “tehlikeli” veya “yaralı” gibi dereceli kavramlarla karar vermesini sağlayarak daha inandırıcı davranışlar üretir.

``

## Kesin kurallar neden mekanik hissettirir?

Klasik bir karar sisteminde geliştirici şöyle bir kural yazabilir: “Oyuncuya olan mesafe 10 metreden azsa saldır.” Düşman 9,99 metrede saldırırken 10,01 metrede hiçbir şey yapmayabilir. Aradaki iki santimetrenin bu kadar büyük bir davranış değişikliği oluşturması oyuncuya yapay gelir.

Bulanık mantıkta bir değer yalnızca doğru veya yanlış değildir. Bunun yerine bir kümeye $0$ ile $1$ arasında değişen üyelik derecesiyle bağlanır:

$$\mu_{Yakın}(x) \in [0,1]$$

Burada $x$ mesafeyi, $\mu_{Yakın}(x)$ ise hedefin “yakın” kabul edilme derecesini gösterir. Örneğin 4 metre için değer $0.9$, 12 metre için $0.35$ olabilir.

| Özellik | Kesin mantık | Bulanık mantık |
|---|---|---|
| Mesafe yorumu | Yakın veya uzak | Kısmen yakın, oldukça uzak |
| Davranış geçişi | Ani | Kademeli |
| Kural yazımı | Basit | Daha esnek |
| Oyuncuya etkisi | Tahmin edilebilir | Doğal ve çeşitlilik içeren |

## Bulanık mantık olasılık mıdır?

Sık yapılan bir hata, üyelik derecesini doğrudan olasılık sanmaktır. “Hedef 0.7 yakın” ifadesi, hedefin yüzde 70 ihtimalle yakın olduğu anlamına gelmez. Bu değer, mevcut mesafenin “yakınlık” kavramına ne ölçüde uyduğunu belirtir. Rastgelelik eklemek istenirse bulanık sistemin ürettiği sonuç ayrıca olasılıksal seçimde kullanılabilir.

Bir düşman üç girdiyi değerlendirebilir:

- **Mesafe:** Yakın, orta veya uzak
- **Sağlık:** Kritik, yaralı veya güçlü
- **Cephane:** Az, yeterli veya fazla

Bunlardan hareketle şu kurallar tanımlanabilir:

1. Hedef yakın **ve** sağlık yüksekse saldırganlık artsın.
2. Sağlık kritik **veya** cephane azsa kaçma isteği artsın.
3. Hedef uzaktaysa siper alma isteği yükselsin.

Bulanık VE işlemi çoğunlukla minimumla hesaplanır:

$$\mu_{A \land B}=\min(\mu_A,\mu_B)$$

Bulanık VEYA içinse maksimum kullanılabilir:

$$\mu_{A \lor B}=\max(\mu_A,\mu_B)$$

Sağlığın “yüksek” üyeliği $0.8$, hedefin “yakın” üyeliği $0.6$ ise saldırı kuralının etkinliği $\min(0.8,0.6)=0.6$ olur.

## Basit bir uygulama

Aşağıdaki C# kodu, mesafe ve sağlık değerlerinden saldırı ile kaçış puanları üretir. `Math.Clamp`, sonuçların $0$ ile $1$ arasında kalmasını sağlar.

```csharp
public static class FuzzyEnemyAI
{
    static float Near(float distance)
    {
        return Math.Clamp((15f - distance) / 15f, 0f, 1f);
    }

    static float LowHealth(float healthPercent)
    {
        return Math.Clamp((50f - healthPercent) / 50f, 0f, 1f);
    }

    public static string Decide(float distance, float healthPercent)
    {
        float near = Near(distance);
        float lowHealth = LowHealth(healthPercent);

        float attackScore = Math.Min(near, 1f - lowHealth);
        float fleeScore = Math.Max(lowHealth, 1f - near);

        return attackScore > fleeScore ? "Saldır" : "Geri çekil";
    }
}
```

Bu örnekte `Near`, mesafe azaldıkça yükselen yakınlık derecesini hesaplar. `LowHealth` ise sağlık düştükçe büyür. Sistem hâlâ en yüksek puanlı davranışı seçtiği için deterministiktir. Daha az tahmin edilebilir düşmanlar için puanlar ağırlıklı rastgele seçimde kullanılabilir; örneğin saldırı puanı $0.7$, kaçış puanı $0.3$ ise seçimler bu ağırlıklara göre yapılabilir.

## Tasarımda dikkat edilmesi gerekenler

Üyelik fonksiyonlarını ayarlamak teknik olduğu kadar tasarımsal bir iştir. Çok geniş aralıklar düşmanı kararsız, çok dar aralıklar ise klasik eşik sistemi kadar mekanik yapabilir. Ayrıca davranışların her karede değişmesini önlemek için kararlar kısa süre kilitlenebilir veya önceki karara küçük bir devam bonusu verilebilir.

Bulanık mantık sihirli bir zekâ üretmez; fakat tasarımcının belirsiz kavramları sayısallaştırmasını sağlar. Sonuçta düşman “10 metreden yakınsa saldıran robot” olmaktan çıkar, koşulları birlikte değerlendiren ve oyuncuya daha canlı görünen bir rakibe dönüşür.
