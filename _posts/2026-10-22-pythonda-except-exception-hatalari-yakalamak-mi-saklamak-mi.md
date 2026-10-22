---
layout: post
title: "Python’da except Exception: Hataları Yakalamak mı, Saklamak mı?"
math: true
categories: 
  - Bilgi
tags: 
  - python
  - exception
  - hata yönetimi
  - debugging
  - temiz kod
toc: true
image: /img/pythonda-except-exception-81.png
---

Python’da hata yakalamak, uygulamanın ilk tökezlemede yere kapaklanmasını önler. Ancak `except Exception` ifadesini her yere serpiştirmek, zemini güvenli hâle getirmek yerine çukurların üzerini halıyla kapatmaya benzeyebilir. Program çalışıyor görünürken veri kaybı, yanlış sonuçlar ve bulunması zor hatalar sessizce büyüyebilir.

![pythonda-except-exception-81](/img/pythonda-except-exception-81.svg)

``
## `except Exception` tam olarak ne yakalar?

Python’daki istisnalar sınıf hiyerarşisine sahiptir. `Exception`; `ValueError`, `TypeError`, `KeyError`, `OSError` ve pek çok uygulama hatasının ortak üst sınıfıdır. Dolayısıyla aşağıdaki blok çok geniş bir alanı kapsar:

```python
try:
    sonucu_hesapla()
except Exception:
    pass
```

Buradaki asıl tehlike yalnızca geniş yakalama değildir; hatanın ardından `pass` kullanılarak hiçbir kayıt bırakılmamasıdır. `sonucu_hesapla()` içindeki bir yazım hatası, bozuk veri veya beklenmeyen ağ problemi aynı sessizlikle yutulur.

Bir sistemin gözlemlenebilirliğini basitçe şöyle düşünebiliriz:

$$G = \frac{K}{T}$$

Burada $G$ gözlemlenebilirlik, $K$ kaydedilen anlamlı hata sayısı, $T$ ise gerçekleşen toplam hata sayısıdır. Hatalar sessizce geçiştirildikçe $K$ azalır ve sistemin gerçekte ne yaptığı karanlıkta kalır.

## Geniş ve hedefli yakalama karşılaştırması

| Yaklaşım | Avantaj | Risk | Uygun kullanım |
|---|---|---|---|
| `except Exception` | Beklenmeyen uygulama hatalarını topluca yakalar | Programlama kusurlarını gizleyebilir | En üst uygulama sınırı |
| `except ValueError` | Beklenen veri sorununu açıkça belirtir | Diğer hatalar yukarı taşınır | Girdi dönüştürme |
| `except OSError` | Dosya ve işletim sistemi sorunlarını yönetir | Alt türlere göre ayrıntı gerekebilir | Dosya işlemleri |
| Çıplak `except:` | `BaseException` türlerini de yakalar | Çıkış sinyallerini engelleyebilir | Neredeyse hiçbir zaman |

Çıplak `except:`, `KeyboardInterrupt` ve `SystemExit` gibi `BaseException` alt sınıflarını da yakalayabilir. Kullanıcı `Ctrl+C` ile programı durdurmaya çalışırken uygulamanın inatla devam etmesi pek eğlenceli değildir.

## Beklediğin hatayı yakala

Bir kullanıcıdan sayı alırken beklenen sorun, değerin sayıya çevrilememesidir. Bu nedenle yalnızca `ValueError` yakalanmalıdır:

```python
def yas_oku(metin):
    try:
        yas = int(metin)
    except ValueError:
        return None
    else:
        return yas
```

Bu kod, geçersiz girdiyi kontrollü biçimde yönetir. Buna karşılık fonksiyon içindeki beklenmeyen bir `TypeError` gizlenmez; hata üst katmana ulaşır ve geliştirici tarafından görülebilir.

## Geniş yakalama gerekiyorsa iz bırak

Web sunucusu, görev işleyicisi veya komut satırı aracının ana döngüsü gibi sınır katmanlarında `Exception` yakalamak mantıklı olabilir. Amaç süreci ayakta tutmak olsa bile hata günlüklenmeli, bağlam korunmalı ve gerekiyorsa yeniden fırlatılmalıdır:

```python
import logging

logger = logging.getLogger(__name__)

def gorevi_calistir(gorev):
    try:
        return gorev.calistir()
    except Exception:
        logger.exception("Görev çalıştırılırken beklenmeyen hata oluştu")
        raise
```

`logger.exception`, aktif istisnanın traceback bilgisini otomatik olarak kaydeder. Tek başına `logger.error("Hata oldu")` demek ise dedektife yalnızca “bir suç işlendi” notu bırakıp olay yerini temizlemeye benzer. `raise` ifadesi aynı istisnayı ve traceback zincirini koruyarak üst katmana iletir.

## Dar bir `try` bloğu kullan

`try` bloğu büyüdükçe hangi satırın hataya yol açtığını anlamak zorlaşır. Yalnızca hata vermesi beklenen işlemi kapsamak daha güvenlidir:

```python
try:
    veri = dosyadan_oku("ayarlar.json")
except FileNotFoundError:
    veri = varsayilan_ayarlar()

ayarlari_dogrula(veri)
uygulamayi_baslat(veri)
```

Böylece doğrulama veya başlatma aşamasındaki gerçek hatalar yanlışlıkla “dosya bulunamadı” senaryosu gibi ele alınmaz.

Kısacası iyi hata yönetiminin amacı programı ne pahasına olursa olsun çalıştırmak değildir. Beklenen sorunları hedefli biçimde karşılamak, beklenmeyenleri görünür kılmak ve teşhis için yeterli bağlam bırakmaktır. `except Exception` bir emniyet ağı olabilir; fakat kodun tamamını örten görünmezlik pelerini olmamalıdır.
