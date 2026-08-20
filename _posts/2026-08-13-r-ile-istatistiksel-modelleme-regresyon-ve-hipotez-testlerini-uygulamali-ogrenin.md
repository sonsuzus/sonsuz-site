---
layout: post
title: "R ile İstatistiksel Modelleme: Regresyon ve Hipotez Testlerini Uygulamalı Öğrenin"
math: true
categories: 
  - Bilgi
tags: 
  - r
  - istatistik
  - regresyon
  - hipotez testi
  - veri analizi
---

R dili, istatistiksel modelleme dünyasında hem akademisyenlerin hem de veri analistlerinin vazgeçilmez araçlarından biridir. Bunun sebebi yalnızca zengin paket ekosistemi değildir: R, veri temizlemeden görselleştirmeye, regresyondan hipotez testlerine kadar analiz sürecini okunabilir kodlarla kurmayı sağlar. Bu yazıda yerleşik `mtcars` veri setini kullanarak doğrusal regresyon kuracak, model sonuçlarını yorumlayacak ve iki grubun ortalamasını t testiyle karşılaştıracağız.
``

## Modelleme mantığı: Soruyu denkleme dönüştürmek

İstatistiksel modelleme, verideki rastlantısal dalgalanmayı tamamen yok etmeye çalışmaz. Bunun yerine değişkenler arasındaki sistematik ilişkiyi tahmin eder. Örneğin bir otomobilin yakıt tüketimi (`mpg`) ile ağırlığı (`wt`) arasında çoğunlukla ters yönlü bir ilişki bekleriz.

Basit doğrusal regresyon denklemi şöyledir:

$$
y_i = \beta_0 + \beta_1x_i + \varepsilon_i
$$

Burada $y_i$ yakıt tüketimini, $x_i$ ağırlığı, $\beta_0$ sabit terimi, $\beta_1$ ağırlığın etkisini ve $\varepsilon_i$ ise modelin açıklayamadığı hata payını temsil eder. Amaç, gözlemlere en iyi uyan doğruyu bulmaktır. R bunu en küçük kareler yöntemiyle yapar; yani hata kareleri toplamını minimize eder:

$$
\min \sum_{i=1}^{n}(y_i - \hat{y}_i)^2
$$

## Regresyon ve hipotez testi: Aynı laboratuvarın farklı araçları

| Yaklaşım | Temel soru | Tipik çıktı | Ne zaman kullanılır? |
|---|---|---|---|
| Doğrusal regresyon | Bir değişken diğerini ne kadar etkiliyor? | Katsayı, $R^2$, p-değeri | Sayısal sonuç tahmini ve ilişki analizi |
| t testi | İki grubun ortalaması farklı mı? | t istatistiği, güven aralığı, p-değeri | İki bağımsız grubun karşılaştırılması |
| ANOVA | Üç veya daha fazla ortalama farklı mı? | F istatistiği, p-değeri | Birden çok grubun karşılaştırılması |

Önce veri setini inceleyelim. `mtcars`, 1970'li yıllardaki otomobillerin motor ve performans özelliklerini içerir. `wt` değişkeni ağırlığı, `mpg` ise galon başına mil değerini gösterir.

```r
# Yerleşik veri setinin ilk satırlarını incele
head(mtcars)

# Temel özet istatistikler
summary(mtcars[, c("mpg", "wt", "hp", "am")])

# mpg ile wt ilişkisini görselleştir
plot(mtcars$wt, mtcars$mpg,
     pch = 19, col = "steelblue",
     xlab = "Ağırlık (1000 lb)",
     ylab = "Yakıt Tüketimi (mpg)")
```

Grafikte noktaların aşağı yönlü eğilim göstermesi, ağır araçların daha düşük `mpg` değerine sahip olabileceğine dair ilk ipucudur. Ancak görsel sezgi tek başına yeterli değildir; bu ilişkiyi modelle ölçmeliyiz.

## R ile doğrusal regresyon kurmak

R'de `lm()` fonksiyonu doğrusal model oluşturur. Aşağıdaki model, yakıt tüketimini ağırlık üzerinden tahmin eder.

```r
# mpg ~ wt: mpg bağımlı, wt bağımsız değişkendir
model <- lm(mpg ~ wt, data = mtcars)

# Katsayılar, p-değerleri ve R-kareyi görüntüle
summary(model)

# Tahmin doğrusunu grafiğe ekle
abline(model, col = "firebrick", lwd = 2)

# Yeni bir araç için tahmin üret
predict(model, newdata = data.frame(wt = 3.0), interval = "prediction")
```

`summary(model)` çıktısındaki `wt` katsayısı negatifse, ağırlık arttıkça beklenen yakıt verimliliğinin düştüğünü söyleriz. Katsayı örneğin $-5.34$ ise, ağırlıktaki her bir birimlik artış için `mpg` değerinin ortalama 5.34 azalması beklenir. Katsayının p-değeri genellikle şu sıfır hipotezini sınar:

$$
H_0: \beta_1 = 0 \qquad H_1: \beta_1 \ne 0
$$

$p < 0.05$ sonucu, seçilen anlamlılık düzeyinde ağırlık ile yakıt tüketimi arasında istatistiksel olarak anlamlı bir ilişki bulunduğuna işaret eder. Yine de p-değeri etkinin büyüklüğü değildir; $R^2$ değerine ve güven aralıklarına da bakmak gerekir.

## Şanzıman türleri arasında t testi

Şimdi otomatik (`am = 0`) ve manuel (`am = 1`) araçların ortalama `mpg` değerleri farklı mı sorusunu soralım. Önce anlaşılır etiketler oluşturalım, ardından Welch t testini çalıştıralım.

```r
# Grup etiketlerini faktöre dönüştür
mtcars$transmission <- factor(mtcars$am,
                               levels = c(0, 1),
                               labels = c("Otomatik", "Manuel"))

# Grup ortalamalarını incele
aggregate(mpg ~ transmission, data = mtcars, FUN = mean)

# İki grubun ortalamasını karşılaştır
sonuc_t <- t.test(mpg ~ transmission, data = mtcars)
sonuc_t
```

Bu testte hipotezler $H_0: \mu_{otomatik}=\mu_{manuel}$ ve $H_1: \mu_{otomatik}\ne\mu_{manuel}$ biçimindedir. Çıktıdaki güven aralığı sıfırı içermiyor ve p-değeri 0.05'ten küçükse, ortalamalar arasında anlamlı fark vardır. Ancak önemli bir uyarı: Manuel araçlar aynı zamanda daha hafif olabilir. Bu nedenle farkın yalnızca şanzımandan kaynaklandığını söylemek için `mpg ~ am + wt` gibi çoklu regresyon modelleri kurmak gerekir. İstatistikte en iyi model, en gösterişli çıktıyı değil, soruyu ve olası karıştırıcı değişkenleri en doğru temsil eden modeldir.
