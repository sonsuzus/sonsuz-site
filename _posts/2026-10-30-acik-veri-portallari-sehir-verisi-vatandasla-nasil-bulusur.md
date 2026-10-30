---
layout: post
title: "Açık Veri Portalları: Şehir Verisi Vatandaşla Nasıl Buluşur?"
math: true
categories: 
  - Bilgi
tags: 
  - açık veri
  - api
  - belediye
  - akıllı şehir
  - veri güvenliği
  - şehircilik
toc: true
image: /img/acik-veri-portallari-40.png
---

Bir şehir her gün devasa miktarda veri üretir: otobüslerin konumu, hava kalitesi, yol çalışmaları, bütçe harcamaları, park doluluk oranları ve hatta hangi mahallede kaç ağaç bulunduğu… Belediyeler bu verileri yalnızca kurum içinde saklamak yerine açık veri portalları ve API'ler aracılığıyla paylaşabilir. Böylece vatandaşlar, araştırmacılar ve yazılımcılar şehrin dijital hazinesinden yararlanarak yeni uygulamalar geliştirebilir.


![acik-veri-portallari-40](/img/acik-veri-portallari-40.svg)

``

## Açık veri nedir?

Açık veri; herkesin erişebildiği, kullanabildiği, değiştirebildiği ve uygun lisans koşullarıyla yeniden paylaşabildiği veridir. Bir Excel dosyasını belediyenin sitesine yüklemek başlangıç sayılabilir, ancak gerçek anlamda kullanılabilir veri için makine tarafından okunabilir formatlar gerekir.

Bir veri kümesinin faydasını basitçe şöyle düşünebiliriz:

$$F = E \times G \times A$$

Burada $E$ erişilebilirliği, $G$ güncelliği, $A$ ise anlaşılabilirliği temsil eder. Çarpanlardan biri sıfıra yaklaşırsa toplam fayda da düşer. Örneğin güncel olmayan otobüs konumları, teknik olarak erişilebilir olsa bile yolcuyu yanlış durağa koşturabilir!

| Paylaşım yöntemi | Güncellik | Yazılımla kullanım | Uygun senaryo |
|---|---:|---:|---|
| PDF raporu | Düşük | Zor | Yıllık faaliyet raporları |
| CSV dosyası | Orta | Kolay | Bütçe ve istatistik verileri |
| REST API | Yüksek | Çok kolay | Ulaşım ve sensör verileri |
| GeoJSON | Yüksek | Çok kolay | Harita ve konum uygulamaları |

## Belediye API'si nasıl çalışır?

API, belediyenin veri sistemleri ile dışarıdaki uygulamalar arasında kontrollü bir köprü kurar. İstemci belirli bir adrese HTTP isteği gönderir; sunucu çoğunlukla JSON biçiminde yanıt verir. Örneğin `/api/v1/otobusler` adresi araç listesini, `/api/v1/otobusler/34` adresi ise belirli bir aracı döndürebilir.

Arka planda tipik akış şu şekildedir:

1. Sensörler veya belediye birimleri ham veriyi üretir.
2. ETL süreci veriyi temizler, standartlaştırır ve doğrular.
3. Kişisel ya da hassas alanlar anonimleştirilir.
4. API katmanı yalnızca paylaşılması uygun alanları sunar.
5. Portal; açıklama, lisans, güncelleme tarihi ve örnek sorgular yayımlar.

Bir geliştirici, durak verisini Python ile şöyle kullanabilir:

```python
import requests

url = 'https://veri.ornek.bel.tr/api/v1/duraklar'
params = {'ilce': 'merkez', 'limit': 10}

response = requests.get(url, params=params, timeout=10)
response.raise_for_status()

for durak in response.json()['results']:
    print(durak['ad'], durak['konum'])
```

Bu kod API'ye filtreli bir GET isteği gönderir, bağlantı hatalarını denetler ve dönen ilk on durağın adını ve konumunu yazdırır. Gerçek projelerde sayfalama, önbellekleme ve istek sınırı bilgileri de dikkate alınmalıdır.

## Şeffaflık kadar mahremiyet de önemli

Her belediye verisi açılmamalıdır. Kişilerin adresleri, sağlık bilgileri, araç plakaları veya hareket geçmişleri doğrudan paylaşılırsa açık veri faydadan çok zarar üretebilir. Bu nedenle isim kaldırma tek başına yeterli değildir; farklı veri kümeleri birleştirildiğinde kişinin yeniden tanınması mümkün olabilir.

| Açılabilecek veri | Korunması gereken veri |
|---|---|
| Mahalle bazlı nüfus istatistiği | Kişi ve açık adres listesi |
| Anlık toplu taşıma konumu | Bireysel seyahat geçmişi |
| Toplam belediye harcaması | Personelin banka bilgileri |
| Ölçüm istasyonu hava kalitesi | Vatandaşa ait sağlık kaydı |

API anahtarları, hız sınırlama, anonimleştirme ve erişim kayıtları güvenliğin temel araçlarıdır. Ayrıca veri lisansı açıkça belirtilmelidir; “internette bulunuyor” ifadesi, verinin sınırsızca kullanılabileceği anlamına gelmez.

## Vatandaş için gerçek değer

İyi tasarlanmış bir portal yalnızca dosya deposu değildir. Veri sözlüğü, sürüm bilgisi, API dokümantasyonu, hata bildirim kanalı ve örnek projeler sunar. Bunun sonucunda erişilebilir rota uygulamaları, mahalle bütçesi panoları, hava kalitesi uyarıları veya boş otopark haritaları geliştirilebilir.

Kısacası şehir verisi paylaşıldığında belediye tek üretici olmaktan çıkar; vatandaşlar da çözüm ortağına dönüşür. Doğru standartlar, güncel API'ler ve güçlü mahremiyet kuralları sayesinde açık veri, dijital şehrin vitrini değil çalışan motoru olabilir.
