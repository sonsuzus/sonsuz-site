---
layout: post
title: "Yan Kanal Saldırıları: Bir Şifreyi Zamanlamadan Tahmin Etmek"
math: true
categories: 
  - Bilgi
tags: 
  - siber güvenlik
  - yan kanal
  - zamanlama saldırısı
  - kriptografi
  - python
  - güvenli kodlama
toc: true
image: /img/yan-kanal-saldirilari-85.png
---

Bir parola denetimi yalnızca “doğru” veya “yanlış” cevabı veriyor gibi görünebilir. Fakat işlem süresi de istemeden bilgi taşıyorsa saldırgan, kapının anahtarını görmeden kilidin sesini dinleyebilir. Zamanlama saldırıları, yazılımın ne söylediğinden çok cevabı ne kadar sürede verdiğini inceleyen yan kanal saldırılarıdır.
``
## Zaman neden bilgi sızdırır?

Bazı programlar iki metni soldan sağa karşılaştırır ve ilk farklı karakterde işlemi bitirir. Girilen adayın ilk üç karakteri doğruysa karşılaştırma, ilk karakteri yanlış olan bir adaya göre biraz daha uzun sürebilir. Tek ölçümde fark çoğunlukla fark edilmez; ancak çok sayıda ölçüm istatistiksel bir sinyale dönüşebilir.

Basitleştirilmiş süre modeli şöyledir:

$$T(k)=T_0+k\Delta+\epsilon$$

Burada $T_0$ sabit işlem maliyeti, $k$ doğru eşleşen karakter sayısı, $\Delta$ her ek karşılaştırmanın maliyeti ve $\epsilon$ ağ gecikmesi, işletim sistemi zamanlaması veya işlemci yükü gibi gürültüdür. Saldırganın amacı tek bir hızlı ölçüm yapmak değil, tekrarlı örneklerle $\epsilon$ etkisini azaltmaktır.

| Karşılaştırma türü | Davranış | Zamanlama riski |
|---|---|---|
| Erken çıkan döngü | İlk farkta durur | Yüksek |
| Normal eşitlik operatörü | Uygulamaya göre değişir | Belirsiz |
| Sabit zamanlı karşılaştırma | Tüm baytları işler | Daha düşük |

![yan-kanal-saldirilari-85](/img/yan-kanal-saldirilari-85.svg)


## Savunmasız yaklaşım

Aşağıdaki eğitim örneği, problemin kaynağını gösterir. Gerçek sistemlerde kullanılmamalıdır:

```python
import time

def insecure_compare(secret: bytes, candidate: bytes) -> bool:
    if len(secret) != len(candidate):
        return False

    for expected, received in zip(secret, candidate):
        if expected != received:
            return False
        # Yalnızca laboratuvar ortamında farkı görünür yapar.
        time.sleep(0.002)

    return True
```

`candidate` doğru bir önek içerdiğinde döngü daha fazla adım çalışır. `sleep` gerçek uygulamaların doğal bir parçası değildir; burada nanosaniyelik farkı gözle görülebilir hâle getiren bir büyüteçtir. Üretim ortamındaki sızıntılar önbellek erişimleri, dallanma tahmini veya değişken süreli algoritmalardan doğabilir.

Örneğin kontrollü bir laboratuvarda aynı uzunluktaki iki adayın ortalama süresi ölçülebilir:

```python
from statistics import mean
from time import perf_counter_ns

def average_duration(secret, candidate, repeats=30):
    samples = []
    for _ in range(repeats):
        start = perf_counter_ns()
        insecure_compare(secret, candidate)
        samples.append(perf_counter_ns() - start)
    return mean(samples)

secret = b"KEDI"
print(average_duration(secret, b"XAAA"))
print(average_duration(secret, b"KAAA"))
```

Bu kod bir parola çıkarma aracı değil, yalnızca yerel ve yapay bir fonksiyondaki süre farkını gözlemleme deneyidir. Yetkisiz sistemlerde deneme yapmak hukuka ve etik kurallara aykırıdır.

## Sabit zamanlı karşılaştırma

Python’da hassas değerleri elle yazılmış döngülerle karşılaştırmak yerine standart kütüphanedeki `hmac.compare_digest` kullanılmalıdır:

```python
import hmac

def secure_compare(secret: bytes, candidate: bytes) -> bool:
    return hmac.compare_digest(secret, candidate)
```

Bu fonksiyon, aynı türdeki girdilerin içeriğine bağlı erken çıkışları önlemek için tasarlanmıştır. Yine de “sabit zamanlı” ifadesi bütün sistemin süresinin matematiksel olarak aynı olduğu anlamına gelmez. Girdi uzunluğu, veri tabanı sorguları, hata mesajları ve oran sınırlaması gibi çevresel davranışlar ayrıca değerlendirilmelidir.

## Parolalarda doğru mimari

Parolalar genellikle doğrudan karşılaştırılmamalı; Argon2id, scrypt veya bcrypt gibi yavaş ve tuzlu parola özetleme algoritmalarıyla doğrulanmalıdır. API anahtarları, MAC değerleri ve oturum belirteçleri için sabit zamanlı karşılaştırma özellikle önemlidir.

Savunma kontrol listesi:

- Standart kriptografi kütüphanelerini kullanın.
- Başarısızlık mesajlarını ve işlem yollarını mümkün olduğunca birleştirin.
- Hız sınırlaması ve izleme uygulayın.
- Ölçümleri farklı yük ve ağ koşullarında test edin.
- Rastgele gecikmeyi ana çözüm sanmayın; gürültü, yeterli örnekle filtrelenebilir.

Kısacası yazılım yalnızca çıktı üretmez; süre, güç tüketimi ve bellek erişimi gibi izler de bırakır. Güvenli programlama, doğru cevabı saklamanın yanında cevaba giden yolun ne kadar bilgi anlattığını da sorgulamaktır.
