---
layout: post
title: "Python’da *args ve **kwargs: Esneklik Okunabilirliğe Karşı"
math: true
categories: 
  - Bilgi
tags: 
  - python
  - args
  - kwargs
  - fonksiyonlar
  - okunabilirlik
  - temiz-kod
toc: true
image: /img/pythonda-args-ve-31.png
---

![pythonda-args-ve-31](/img/pythonda-args-ve-31.svg)


Python’daki `*args` ve `**kwargs`, fonksiyonlara değişken sayıda argüman gönderme özgürlüğü sağlar. Ancak bu özgürlük kontrolsüz kullanıldığında fonksiyon imzası, ne beklediğini söylemeyen gizemli bir kapıya dönüşebilir. Fonksiyon çalışır, testler geçer; fakat onu ilk kez gören geliştirici kendini “Buraya ne göndermem gerekiyor?” diye sorarken bulur.

``

## `*args` ve `**kwargs` aslında ne yapar?

`*args`, fazladan konumsal argümanları bir `tuple` içerisinde toplar. `**kwargs` ise fazladan anahtar kelimeli argümanları bir `dict` olarak saklar. Buradaki `args` ve `kwargs` isimleri zorunlu değildir; özel davranışı oluşturan yıldızlardır.

```python
def rapor_olustur(baslik, *satirlar, **ayarlar):
    print(f"Rapor: {baslik}")
    print(f"Satır sayısı: {len(satirlar)}")
    print(f"Ayarlar: {ayarlar}")

rapor_olustur(
    "Aylık Satış",
    "Ocak: 120",
    "Şubat: 145",
    renk="mavi",
    pdf=True
)
```

Bu örnekte `satirlar`, iki elemanlı bir tuple; `ayarlar` ise `renk` ve `pdf` anahtarlarını taşıyan bir sözlüktür. Teknik olarak oldukça kullanışlıdır. Sorun, fonksiyon imzasının hangi ayarların geçerli olduğunu açıklamamasıdır.

Bir fonksiyonun anlaşılabilirliğini kabaca şu ilişkiyle düşünebiliriz:

$$
O \approx \frac{B}{1 + G}
$$

Burada $O$ okunabilirliği, $B$ imzada açıkça belirtilen bilgiyi, $G$ ise gizli veya belirsiz parametre sayısını temsil eder. Bu gerçek bir yazılım metriği değildir; fakat önemli fikri gösterir: Beklentiler imzadan sözlük içine taşındıkça okunabilirlik azalır.

## Açık imza ile karşılaştırma

| Yaklaşım | Avantaj | Dezavantaj |
|---|---|---|
| Açık parametreler | IDE desteği ve anlaşılır hata mesajları | Çok sayıda parametrede imza uzar |
| `*args` | Değişken sayıda değer kabul eder | Değerlerin anlamı sıraya bağımlıdır |
| `**kwargs` | Yeni seçenek eklemek kolaydır | Geçerli anahtarlar görünmez kalabilir |
| Yapılandırma nesnesi | Tip güvenliği ve düzen sağlar | Ek bir sınıf tanımlamak gerekir |

Şu fonksiyon kısa görünür, ancak kullanıcı açısından yeterince açıklayıcı değildir:

```python
def kullanici_olustur(**kwargs):
    # Parametreleri doğrudan veri katmanına iletiyor.
    return veritabani.ekle(kwargs)
```

Fonksiyon `ad`, `eposta`, `yas` veya bambaşka alanlar mı bekliyor? Yanlışlıkla `eposta` yerine `epost` yazılırsa hata hemen mi alınacak, yoksa problem veritabanına kadar mı ilerleyecek? Kısa imza her zaman sade tasarım anlamına gelmez.

Açık parametreler çoğu durumda daha güvenlidir:

```python
def kullanici_olustur(
    ad: str,
    eposta: str,
    *,
    aktif: bool = True
) -> dict:
    return {
        "ad": ad,
        "eposta": eposta,
        "aktif": aktif,
    }
```

Tek başına kullanılan `*`, sonraki parametrelerin yalnızca isimleriyle gönderilmesini zorunlu kılar. Böylece `aktif` değerinin yanlışlıkla üçüncü konumsal argüman olarak verilmesi engellenir. Ayrıca IDE otomatik tamamlama sunabilir ve statik tip denetleyicileri hataları daha erken yakalayabilir.

## Yapılandırma nesnesi ne zaman kullanılmalı?

Seçenek sayısı arttığında bütün bilgileri `**kwargs` içine saklamak yerine `dataclass` tercih edilebilir:

```python
from dataclasses import dataclass

@dataclass
class RaporAyarlari:
    renk: str = "mavi"
    pdf: bool = False
    sayfa_boyutu: str = "A4"


def rapor_olustur(baslik: str, ayarlar: RaporAyarlari) -> None:
    print(baslik, ayarlar)
```

Bu yapı geçerli seçenekleri görünür kılar, varsayılan değerleri tek yerde toplar ve yanlış alan adlarının sessizce dolaşmasını önler.

Elbette `*args` ve `**kwargs` kötü değildir. Dekoratörlerde, başka bir fonksiyona çağrı aktarırken veya gerçekten değişken sayıda değer kabul eden toplama benzeri işlemlerde son derece uygundurlar. Temel ölçüt şudur: Esnekliğin kendisi fonksiyonun amacıysa yıldızlı parametreler mantıklıdır; yalnızca uzun bir imzayı saklamak için kullanılıyorsa okunabilirlik borcu oluştururlar. Python bize yıldızları verir, fakat her fonksiyonu galaksiye çevirmek zorunda değiliz.
