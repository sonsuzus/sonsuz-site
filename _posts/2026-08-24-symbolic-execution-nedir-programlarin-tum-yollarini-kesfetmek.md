---
layout: post
title: "Symbolic Execution Nedir? Programların Tüm Yollarını Keşfetmek"
math: true
categories: 
  - Bilgi
tags: 
  - symbolic execution
  - yazılım testi
  - program analizi
---

Bir programı test ederken birkaç örnek girdi vermek çoğu zaman yeterli görünür: `0`, `42`, belki negatif bir sayı... Ancak bu yaklaşım, kodun karanlıkta kalan dallarını kolayca kaçırır. Symbolic Execution (sembolik çalıştırma), somut değerler yerine sembolik değişkenlerle ilerleyerek programın ulaşılabilir tüm mantıksal yollarını analiz etmeyi amaçlayan gelişmiş bir test ve hata bulma tekniğidir. Kısacası programı tek tek örneklerle değil, olası girdilerin matematiksel temsilcileriyle yürütür.

``

## Temel fikir: Değer yerine sembol kullanmak

Klasik çalıştırmada `x = 7` gibi gerçek bir değer vardır. Sembolik çalıştırmada ise `x` bilinmeyen bir semboldür. Program bir `if` koşuluna geldiğinde analiz motoru iki dünyaya ayrılır: koşulun doğru olduğu yol ve yanlış olduğu yol. Her yol için bir **yol koşulu** (path constraint) biriktirilir.

Örneğin aşağıdaki fonksiyonu ele alalım:

```python
def indirim_orani(tutar, premium):
    if tutar > 100 and premium:
        return 20
    if tutar > 100:
        return 10
    return 0
```

Motor, `tutar` ve `premium` için sembolik değerler atar. İlk dönüşe ulaşan yolun koşulu şöyledir:

$$tutar > 100 \land premium = True$$

İkinci yol için ise ilk koşulun sağlanmaması, ardından `tutar > 100` olması gerekir:

$$tutar > 100 \land premium = False$$

Son yol da $tutar \leq 100$ koşuluyla temsil edilir. Bir SMT çözücüsü bu formüllerin gerçekten sağlanıp sağlanamayacağını kontrol eder ve sağlanıyorsa somut test girdileri üretir.

| Yaklaşım | Girdi seçimi | Güçlü yanı | Temel riski |
|---|---|---|---|
| Manuel test | Geliştirici seçer | Hızlı ve anlaşılır | Köşe durumları atlanır |
| Rastgele/fuzz test | Rastgele üretilir | Beklenmeyen çökmeleri bulur | Nadir dallara ulaşamayabilir |
| Symbolic Execution | Kısıtlardan türetilir | Yol ve koşul odaklı kapsam | Yol patlaması yaşayabilir |

## Kısıt çözücü neden kritik?

Sembolik çalıştırmanın kalbinde, bir yolun mantıksal olarak mümkün olup olmadığını belirleyen çözücü bulunur. Örneğin kod hem `x > 10` hem de `x < 5` şartını aynı yolda toplarsa bu yol imkânsızdır. Çözücü buna **unsat** der; analiz motoru bu dalı kapatır. Aksi durumda **sat** sonucu gelir ve çözücü örneğin `x = 11` gibi bir model sunabilir.

Bu mekanizma özellikle doğrulama kontrolleri, sınır değer hataları ve erişilemeyen kod açısından etkilidir. Örneğin dizinin sınır dışına taşması için gereken koşul sembolik olarak aranabilir:

```c
int oku(int *dizi, int boyut, int i) {
    if (i < 0 || i >= boyut) {
        return -1;
    }
    return dizi[i];
}
```

Burada güvenli dal için $0 \leq i < boyut$ koşulu oluşur. Eğer gerçek uygulamada bu kontrol eksik olsaydı, araç taşmayı tetikleyen bir `i` değeri bulmaya çalışabilirdi. Kod parçasının amacı basitçe indeks doğrulamasını göstermektir; sembolik analiz ise bu doğrulamanın tüm olası girdilerde gerçekten çalışıp çalışmadığını sınar.

## Yol patlaması: Süper gücün bedeli

Her `if`, potansiyel olarak yol sayısını ikiye katlar. Birbirinden bağımsız $n$ koşul için teorik üst sınır yaklaşık $2^n$ yoldur. Döngüler, özyineleme ve kullanıcı girdisine bağlı karmaşık koşullar bu sayıyı hızla yönetilemez hâle getirir. Buna **path explosion** denir.

| Sorun | Neden oluşur? | Yaygın çözüm |
|---|---|---|
| Yol patlaması | Çok sayıda dal ve döngü | Yol sınırı, önceliklendirme, birleştirme |
| Karmaşık kısıtlar | String, float veya kripto işlemleri | Alan özel çözücüler, yaklaşık analiz |
| Ortam bağımlılığı | Dosya, ağ, sistem çağrıları | Mock, sembolik ortam modeli |

Pratik araçlar bu yüzden saf sembolik çalıştırmayı hibrit yöntemlerle birleştirir. **Concolic testing**, somut (concrete) ve sembolik yürütmeyi birlikte kullanır: Program gerçek bir girdiye çalıştırılır, görülen dallar için kısıtlar çıkarılır ve sonraki test girdisi bir koşul ters çevrilerek üretilir.

Sonuç olarak Symbolic Execution, “Bu fonksiyon için hangi testi yazmalıyım?” sorusunu “Bu koda ulaşan mümkün tüm mantıksal durumlar neler?” seviyesine taşır. Her yazılım projesinde sınırsız uygulanacak sihirli bir değnek değildir; fakat kritik iş kuralları, güvenlik kontrolleri ve karmaşık karar ağaçları için test stratejisine son derece güçlü bir matematiksel göz kazandırır.
