---
layout: post
title: "Otonom Araç İkilemleri: Faydacı Etiği Algoritmaya Dönüştürmek"
math: true
categories: 
  - Bilgi
tags: 
  - otonom araçlar
  - yapay zekâ etiği
  - algoritma tasarımı
toc: true
---

Otonom bir araç, kazanın artık fiziksel olarak önlenemediği birkaç milisaniyede nasıl davranmalıdır? Bu soru genellikle “Yolcuyu mu, yayayı mı korusun?” biçiminde sorulsa da gerçek dünya, klasik tramvay probleminden çok daha karmaşıktır. Belirsiz sensör verileri, farklı yaralanma ihtimalleri ve hukuki yükümlülükler aynı anda değerlendirilir. Dolayısıyla etik algoritma, kime çarpılacağını seçen soğuk bir hâkim değil; beklenen zararı güvenli ve denetlenebilir kurallarla azaltmaya çalışan son savunma katmanıdır.

``

## Faydacılık makineye nasıl çevrilir?

Faydacı yaklaşım, genel olarak toplam zararı en aza indiren eylemi tercih eder. Araç için olası manevralar kümesini $A$, etkilenecek kişileri $i$ ile gösterelim. Basitleştirilmiş bir maliyet fonksiyonu şöyle kurulabilir:

$$
C(a)=\sum_i P(H_i\mid a)\cdot S(H_i)+\lambda R(a)
$$

Burada $P(H_i\mid a)$, $a$ manevrası altında kişinin zarar görme olasılığıdır. $S(H_i)$ zararın tahmini şiddetini, $R(a)$ ise manevranın oluşturduğu ek riski temsil eder. $\lambda$, bu riskin ağırlığıdır. Sistem teorik olarak

$$
a^*=\arg\min_{a\in A} C(a)
$$

seçimini yapar. Ancak insan yaşamını tek bir sayıya indirgemek hem etik hem teknik açıdan tehlikelidir. Model, kişileri yaşına, gelirine veya sosyal statüsüne göre puanlamamalıdır. Aksi hâlde matematiksel görünen sistem, toplumsal önyargıları otomatikleştirir.

| Yaklaşım | Temel soru | Güçlü yanı | Temel sorun |
|---|---|---|---|
| Faydacılık | Toplam zarar nasıl azalır? | Sonuçları karşılaştırır | Bireysel hakları ezebilir |
| Ödev etiği | Hangi kural asla çiğnenmemeli? | Haklara sınır koyar | Katı kurallar çatışabilir |
| Erdem etiği | Sorumlu bir aktör ne yapardı? | Bağlamı önemser | Kodlanması güçtür |
| Hibrit model | Hangi güvenli seçenek en az zararlı? | Denge ve denetim sağlar | Tasarımı daha karmaşıktır |

## Önce kısıtlar, sonra optimizasyon

Daha savunulabilir tasarım, sınırsız faydacılık yerine **kısıtlı optimizasyon** kullanır. Araç önce kırmızı çizgileri uygular: İnsanları özelliklerine göre ayrıştırma, belirli bir kişiyi kasıtlı hedefe dönüştürme ve doğrulanmamış manevra üretme. Ardından yalnızca güvenli kabul edilen seçenekler arasında beklenen fiziksel zararı azaltır.

Aşağıdaki örnek, bu fikrin sadeleştirilmiş bir prototipidir:

```python
from dataclasses import dataclass

@dataclass
class Manevra:
    ad: str
    yaralanma_olasiligi: float
    siddet: float
    ek_kaza_riski: float
    yasal: bool
    hedefli_zarar: bool

def maliyet(m: Manevra, risk_agirligi: float = 0.4) -> float:
    return m.yaralanma_olasiligi * m.siddet + risk_agirligi * m.ek_kaza_riski

def etik_secim(manevralar):
    uygun = [m for m in manevralar if m.yasal and not m.hedefli_zarar]
    if not uygun:
        return "acil_fren_ve_seridi_koru"
    return min(uygun, key=maliyet).ad
```

`etik_secim`, önce yasaklı eylemleri eler; sonra kalan seçenekleri maliyet fonksiyonuyla karşılaştırır. Varsayılan davranışın fren yapmak ve öngörülebilir rotayı korumak olması önemlidir. Çünkü ani ve sıra dışı bir manevra, sensörlerin henüz algılamadığı yeni mağdurlar yaratabilir.

## Belirsizlik neden merkezdedir?

Sensör “yaya olasılığı %70” diyorsa sistem bunu kesin gerçek gibi kullanmamalıdır. Tahminlerin kalibrasyonu, hata payı ve kötü hava koşulları hesaba katılmalıdır. İki manevranın maliyetleri birbirine çok yakınsa etik açıdan gösterişli bir seçim yapmak yerine kontrollü frenleme tercih edilebilir.

Ayrıca karar kayıtları sonradan incelenebilmelidir: Hangi nesneler algılandı, hangi seçenekler elendi ve hangi model sürümü kullanıldı? Bu kayıtlar açıklanabilirlik sağlar; fakat kişisel verileri koruyacak biçimde saklanmalıdır.

Sonuçta etik kod, otomobile felsefe kitabı okutmak değildir. Amaç kazaları öncelikle mühendislikle engellemek; kaçınılmaz durumda ise ayrımcılık yapmayan, doğrulanabilir ve hukuka bağlı bir zarar azaltma mekanizması kullanmaktır. En iyi etik algoritma kahramanlık tasarlayan değil, sınırlarını bilen algoritmadır.
