---
layout: post
title: "Python Context Manager: İstisnalara Rağmen Kaynaklar Nasıl Güvenle Temizlenir?"
math: true
categories: 
  - Bilgi
tags: 
  - python
  - context-manager
  - with
  - istisna-yönetimi
  - kaynak-yönetimi
toc: true
image: /img/python-context-manager-66.png
---

Bir dosyayı açtınız, veritabanına bağlandınız veya bir kilidi ele geçirdiniz. Tam işinizi bitirecekken kod bir istisna fırlattı! Kaynağı serbest bırakmayı unuttuysanız dosya tanıtıcıları tükenebilir, bağlantılar açık kalabilir ya da uygulamanız kilitlenebilir. Python’ın `with` ifadesi, işler yolunda gitse de gitmese de temizlik adımının çalışmasını sağlayarak bu problemi zarifçe çözer.
``

## Temel fikir: edin, kullan, mutlaka bırak

Kaynak yönetimini üç aşamalı bir süreç olarak düşünebiliriz:

1. Kaynağı edin.
2. Kaynağı kullan.
3. Kaynağı serbest bırak.

Bir kaynağın edinilme olasılığı $P(E)$ ve kullanım sırasında istisna oluşma olasılığı $P(H)$ olsun. Elle yazılmış dikkatsiz bir kodda temizliğin atlanma riski yaklaşık olarak $P(E) \times P(H)$ ile ilişkilendirilebilir. Context manager ise kontrol akışını merkezileştirerek istisna yolunda da temizliği devreye sokar.

```python
with open("veriler.txt", "r", encoding="utf-8") as dosya:
    icerik = dosya.read()
    sayi = int(icerik)  # ValueError oluşabilir
```

`int()` başarısız olsa bile dosya kapatılır. Buradaki garanti, `with` ifadesinin sihrinden değil, context manager protokolünden gelir.

## Perde arkasında ne oluyor?

Bir context manager iki özel metot uygular:

- `__enter__()`: Blok başlamadan önce çalışır ve `as` değişkenine verilecek değeri döndürür.
- `__exit__()`: Blok normal veya hatalı biçimde tamamlandığında çalışır.

Yukarıdaki kod, kavramsal olarak şu yapıya benzer:

```python
manager = open("veriler.txt", "r", encoding="utf-8")
dosya = manager.__enter__()

try:
    icerik = dosya.read()
    sayi = int(icerik)
except BaseException as hata:
    bastirildi = manager.__exit__(
        type(hata), hata, hata.__traceback__
    )
    if not bastirildi:
        raise
else:
    manager.__exit__(None, None, None)
```

Gerçek Python uygulamasının ayrıntıları farklı olabilir; ancak mantık budur. İstisna oluşursa türü, nesnesi ve traceback bilgisi `__exit__()` metoduna aktarılır. Metot `True` döndürürse istisna bastırılır; `False` veya `None` döndürürse dışarı yayılmaya devam eder.

| Durum | `__exit__()` argümanları | Sonuç |
|---|---|---|
| Blok normal biter | `None, None, None` | Temizlik yapılır |
| İstisna oluşur | Tür, nesne, traceback | Temizlik yapılır, hata genellikle yayılır |
| `__exit__()` `True` döndürür | İstisna bilgileri | Hata bastırılır |
| `__exit__()` hata fırlatır | Değişebilir | Yeni hata dışarı yayılır |

## Kendi context manager’ımızı yazalım

Aşağıdaki sınıf, hayali bir bağlantının yaşam döngüsünü yönetir:

```python
class Baglanti:
    def __enter__(self):
        print("Bağlantı açıldı")
        self.aktif = True
        return self

    def sorgula(self):
        if not self.aktif:
            raise RuntimeError("Bağlantı kapalı")
        raise ValueError("Sorgu başarısız oldu")

    def __exit__(self, hata_turu, hata, traceback):
        self.aktif = False
        print("Bağlantı kapatıldı")
        return False


with Baglanti() as baglanti:
    baglanti.sorgula()
```

`ValueError` oluşmasına rağmen `__exit__()` çağrılır ve bağlantı kapatılır. `False` döndürüldüğü için hata gizlenmez. Bu genellikle en güvenli davranıştır; çünkü hataları sessizce yutmak, böcekleri görünmez yapan dijital bir halı altı süpürgesidir.

## `try/finally` ile farkı nedir?

| Yaklaşım | Avantaj | Dezavantaj |
|---|---|---|
| `try/finally` | Açık ve temel kontrol sağlar | Her kullanımda tekrar gerekir |
| `with` | Kısa, okunabilir ve yeniden kullanılabilir | Context manager tanımlanmalıdır |
| `try/except` | Hataları işlemek için uygundur | Tek başına temizliği garanti etmez |

Aslında `with`, `try/finally` düşüncesinin yeniden kullanılabilir bir nesne protokolüne dönüştürülmüş hâlidir. `contextlib.contextmanager` dekoratörüyle aynı yapı bir generator kullanılarak da kurulabilir; `yield` öncesi edinme, `yield` sonrası ise temizlik bölümüdür.

Sonuç olarak `with`, yalnızca dosya açmanın kısa yolu değildir. Dosyalar, ağ bağlantıları, kilitler, geçici dizinler ve transaction’lar gibi kaynaklarda yaşam döngüsünü tek noktadan yönetir. En önemli güvence şudur: Bloktan normal çıkışta, `return` sırasında veya bir istisna nedeniyle ayrılırken `__exit__()` çalıştırılır. Böylece kaynak temizliği, geliştiricinin hafızasına değil dilin kontrol akışına emanet edilir.

![python-context-manager-66](/img/python-context-manager-66.svg)

