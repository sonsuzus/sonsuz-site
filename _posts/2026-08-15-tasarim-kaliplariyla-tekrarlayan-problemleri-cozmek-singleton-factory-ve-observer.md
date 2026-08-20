---
layout: post
title: "Tasarım Kalıplarıyla Tekrarlayan Problemleri Çözmek: Singleton, Factory ve Observer"
math: true
categories: 
  - Bilgi
tags: 
  - tasarım kalıpları
  - singleton
  - factory
  - observer
toc: true
---

Yazılım geliştirmede bazı problemler, proje değişse bile inatla geri gelir: Uygulama genelinde tek bir ayar yöneticisi nasıl tutulur? Nesne üretimini hangi sınıfın yapacağı nasıl saklanır? Bir veri değiştiğinde onu dinleyen ekranlar nasıl haberdar edilir? Tasarım kalıpları, bu sorulara kopyala-yapıştır tarifler değil; test edilmiş iletişim ve sorumluluk dağıtma stratejileri sunar.

``

Bir tasarım kalıbını ezberlemekten çok, arkasındaki **bağımlılık yönetimi** fikrini anlamak önemlidir. Kod kalitesi kabaca bakım maliyetiyle ters orantılıdır: $Kalite \propto \frac{1}{Bağımlılık + Karmaşıklık}$. Kalıplar bu maliyetleri sihirli biçimde sıfırlamaz; ancak değişimin etkilediği alanı daraltırlar. Bununla birlikte, her sınıfa kalıp uygulamak da "altın çekiç" hatasına dönüşebilir: Elinizde çekiç varsa her şey çivi gibi görünür.

## Singleton: Tek ve Kontrollü Örnek

**Singleton**, bir sınıftan uygulama boyunca yalnızca bir örnek üretilmesini ve bu örneğe ortak bir erişim noktası sağlanmasını hedefler. Yapılandırma, günlükleme veya bellek içi önbellek gibi paylaşımlı kaynaklarda faydalı olabilir. Ancak global değişken hissi yarattığı için testleri zorlaştırabilir; bu nedenle bağımlılık enjeksiyonu ile kullanmak daha sağlıklıdır.

```python
class AppConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.theme = "dark"
        return cls._instance

first = AppConfig()
second = AppConfig()
print(first is second)  # True
```

Bu örnekte `__new__`, yeni nesne oluşturulmadan önce çalışır ve önceden oluşmuş örneği döndürür. Çok iş parçacıklı sistemlerde iki iş parçacığının aynı anda örnek üretmesini engellemek için kilit mekanizması da eklenmelidir.

## Factory: Nesne Üretimini Saklamak

**Factory** kalıbında istemci kodu, doğrudan `PDFRapor()` ya da `ExcelRapor()` demek yerine üretim işini bir fabrikaya bırakır. Böylece nesne seçme kuralı merkezi hâle gelir. Yeni bir rapor türü eklemek, uygulamanın her köşesinde `if` aramaktan çok daha az yorucudur.

```python
class Rapor:
    def olustur(self):
        raise NotImplementedError

class PDFRapor(Rapor):
    def olustur(self):
        return "PDF raporu hazır"

class ExcelRapor(Rapor):
    def olustur(self):
        return "Excel raporu hazır"

class RaporFabrikasi:
    @staticmethod
    def getir(tur):
        raporlar = {"pdf": PDFRapor, "excel": ExcelRapor}
        return raporlar[tur]()

rapor = RaporFabrikasi.getir("pdf")
print(rapor.olustur())
```

Buradaki kritik kazanç, istemcinin somut sınıflara değil `Rapor` soyutlamasına bağımlı olmasıdır. Bu, Açık/Kapalı İlkesini destekler: Sistem genişlemeye açık, mevcut davranışı değiştirmeye daha kapalı olur.

## Observer: Değişikliği Dinleyenler

**Observer**, bir nesnedeki değişikliği ona bağlı birçok nesneye duyurur. E-ticaret stok değiştiğinde bildirim göndermek, arayüzdeki sayaçları güncellemek veya olay tabanlı mimari kurmak için idealdir. Yayıncı, abonelerinin detaylarını bilmez; yalnızca `guncelle` sözleşmesini çağırır.

| Kalıp | Temel problem | Güçlü tarafı | Dikkat edilmesi gereken |
|---|---|---|---|
| Singleton | Tek ortak kaynak | Kontrollü erişim | Gizli global durum |
| Factory | Nesne seçimi/üretimi | Gevşek bağlılık | Fazla sınıf üretimi |
| Observer | Olay yayını | Dinamik abonelik | Karmaşık bildirim akışı |

```python
class Stok:
    def __init__(self):
        self.aboneler = []

    def abone_ekle(self, abone):
        self.aboneler.append(abone)

    def guncelle(self, adet):
        for abone in self.aboneler:
            abone(adet)

stok = Stok()
stok.abone_ekle(lambda adet: print(f"Yeni stok: {adet}"))
stok.guncelle(12)
```

Observer ilişkisini $1 \rightarrow N$ olarak düşünebilirsiniz: bir yayıncı, $N$ adet aboneyi tetikler. Abone sayısı arttıkça bildirim maliyeti yaklaşık $O(N)$ olur; bu yüzden gereksiz aboneleri kaldırmak önemlidir.

Sonuçta doğru kalıp, en popüler olan değil sorunun basıncını azaltandır. Tekil bir kaynağı yönetiyorsanız Singleton'ı, üretim kararlarını gizlemek istiyorsanız Factory'yi, olayları yaymak istiyorsanız Observer'ı değerlendirin. Önce basit çözümü kurun; tekrar eden ağrı ortaya çıktığında kalıbı bilinçli biçimde devreye alın.
