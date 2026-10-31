---
layout: post
title: "Dijital Karakterlerin Derdi Ne? Simülasyon Oyunlarında Yapay Yaşam"
math: true
categories: 
  - Bilgi
tags: 
  - yapay yaşam
  - oyun geliştirme
  - simülasyon
  - yapay zeka
  - utility ai
  - python
toc: true
image: /img/dijital-karakterlerin-derdi-34.png
---

![dijital-karakterlerin-derdi-34](/img/dijital-karakterlerin-derdi-34.svg)


Bir karakter düşünün: Karnı aç, uykusu var, ama komşusuyla dedikodu yapmayı da bırakamıyor. Simülasyon oyunlarını eğlenceli kılan tam olarak bu küçük çelişkilerdir. The Sims benzeri oyunlarda karakterler, yalnızca hazır animasyonlar oynatan kuklalar değildir; ihtiyaçları, çevresel fırsatları ve karar kuralları sayesinde yaşayan bir mahalle izlenimi yaratırlar.

``

## Yapay yaşam: Bilinç değil, etkileşim

**Yapay yaşam**, canlı sistemlerin bazı özelliklerini hesaplamalı modellerle yeniden üretmeyi amaçlar. Oyunlarda bunun karşılığı; ihtiyaçları değişen, çevresini algılayan ve eylemlerinin sonuçlarından etkilenen ajanlardır. Buradaki ajan, kendi durumunu taşıyan bir karakterdir.

İnandırıcılık için insan zihnini bütünüyle simüle etmek gerekmez. Basit kuralların birleşmesiyle **ortaya çıkan davranışlar** üretilebilir: Aynı buzdolabına yönelen iki karakterden biri bekler, diğeri sohbet eder. Küçük bir kaynak çatışması, oyuncunun gözünde komik bir hikâyeye dönüşür.

Aşağıdaki model, bu yaklaşımı öğretmek içindir; The Sims’in gerçek kaynak kodunun birebir açıklaması değildir.

## İhtiyaçları sayılara çevirmek

Her ihtiyacı $n_i$ ile gösterelim. Değerler sıfır ile bir arasında olsun: Sıfır, ihtiyaç karşılanmış; bir, ciddi eksiklik demektir. Böylece açlık ve enerji eksikliği aynı ölçekte karşılaştırılabilir.

| İhtiyaç eksikliği | Zamanla değişim | Azaltan eylem |
|---|---|---|
| Açlık | Genellikle yükselir | Yemek yemek |
| Enerji | Uyanıkken yükselir | Uyumak |
| Sosyallik | Yalnızlıkla yükselir | Sohbet etmek |

Basit bir zaman güncellemesi şöyle yazılır:

$$n_i(t+h)=\min(1,n_i(t)+r_i h)$$

Burada $h$ geçen süre, $r_i$ ise saniye başına artış hızıdır. Eylem tamamlandığında ilgili eksiklik azaltılır ve değer sıfırın altına düşmeyecek şekilde sınırlandırılır. Gerçek projelerde uyku gibi uzun eylemlerin etkisini tamamlanma anında değil, zaman boyunca uygulamak daha doğal sonuç verir.

## Karar vermek: En faydalı eylem hangisi?

**Utility AI**, uygulanabilir eylemlere fayda puanı vererek seçim yapar. Basit bir puanlama kullanabiliriz:

$$U(a)=\sum_i w_i n_i\min(n_i,d_i(a))-\lambda T(a)$$

$w_i$ ihtiyacın önemini, $d_i(a)$ eylemin sağlayacağı azalmayı, $T(a)$ süresini temsil eder. Minimum işlemi, zaten karşılanmış bir ihtiyaca gereğinden fazla fayda yazılmasını önler. Süre cezası ise uzak mutfağa yürümek gibi maliyetleri hesaba katabilir.

| Yaklaşım | Güçlü yanı | Zorlandığı nokta |
|---|---|---|
| Sabit öncelikler | Kolay uygulanır | Davranışlar tekrara düşebilir |
| Sonlu durum makinesi | Geçişler nettir | Çok ihtiyaçta karmaşıklaşır |
| Utility AI | Öncelikler dinamik değişir | Puanları dikkatle ayarlamak gerekir |

## Python ile küçük bir karar motoru

Aşağıdaki örnek, önceden uygulanabilir olduğu belirlenmiş eylemler arasından seçim yapar. Karakterin mevcut eylemini değiştirmek için küçük bir avantaj eşiği kullanır:

```python
from dataclasses import dataclass

@dataclass
class Action:
    name: str
    relief: dict[str, float]
    seconds: float

weights = {"hunger": 1.4, "energy": 1.2, "social": 0.8}
needs = {"hunger": 0.8, "energy": 0.5, "social": 0.3}

actions = [
    Action("yemek", {"hunger": 0.6}, 8),
    Action("uyumak", {"energy": 0.7}, 30),
    Action("sohbet", {"social": 0.5}, 12),
]

def score(action):
    benefit = sum(
        weights[key] * needs[key] * min(needs[key], relief)
        for key, relief in action.relief.items()
    )
    return benefit - 0.002 * action.seconds

def choose(available, current_name=None):
    if not available:
        return None
    best = max(available, key=score)
    current = next(
        (a for a in available if a.name == current_name), None
    )
    if current and score(best) < score(current) + 0.05:
        return current
    return best

print(choose(actions).name)
```

`Action`, eylemin etkisini ve süresini taşır. `score`, ihtiyaçlarla faydayı eşleştirir; `choose` ise en yüksek puanı seçer. Örnekte yemek kazanır. Eşik sayesinde karakter, puanlar birbirine yakınken sürekli fikir değiştirmez. Bu teknik **histerezis** olarak bilinir. Yine de mevcut eylem geçersizleşirse korunmaz; karar motoru başka bir seçenek arar.

## Mahalleye hayat veren ayrıntılar

Puanlama tek başına yeterli değildir. Eylem adayları üretilirken nesnenin erişilebilirliği, kullanım kapasitesi ve yol bulma sonucu kontrol edilmelidir. Tuvaleti iki karakter aynı anda kullanmaya çalışıyorsa bir rezervasyon sistemi gerekir; yoksa dijital eviniz trafik kazasına döner.

Kişilik, ağırlıkları değiştirerek davranış çeşitliliği sağlar. Dışa dönük bir karakter sosyalliğe daha çok önem verebilir. İlişkiler, sohbetin beklenen faydasını; ruh hâli, eylem tercihlerini etkileyebilir. Bunlar rastgelelikten daha tutarlı farklılıklar üretir.

Son olarak aç kalma süresi, eylem değiştirme sıklığı ve nesne önündeki kuyrukları ölçün. Zaman adımını değiştirince davranışlar bozuluyorsa modeli yeniden ayarlayın. Başarılı yapay yaşam, en karmaşık algoritma değil; oyuncunun anlamlandırabildiği, tutarlı ama şaşırtıcı küçük hikâyeler üreten sistemdir.
