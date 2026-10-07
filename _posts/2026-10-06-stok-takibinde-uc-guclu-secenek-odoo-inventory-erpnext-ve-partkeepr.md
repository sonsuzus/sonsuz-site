---
layout: post
title: "Stok Takibinde Üç Güçlü Seçenek: Odoo Inventory, ERPNext ve PartKeepr"
math: true
categories: 
  - Program
tags: 
  - stok takibi
  - odoo
  - erpnext
  - partkeepr
  - erp
  - envanter yönetimi
toc: true
image: /img/stok-takibinde-uc-80.png
---

Depodaki son rulmanın nerede olduğunu bulmak bazen polisiye roman çözmekten zor olabilir. İyi bir stok takip sistemi; hangi üründen kaç adet bulunduğunu, ürünün nerede durduğunu ve ne zaman yeniden sipariş verilmesi gerektiğini gösterir. Açık kaynak dünyasında bu iş için öne çıkan Odoo Inventory, ERPNext ve PartKeepr ise benzer ihtiyaçlara farklı ölçeklerden yaklaşır.
``

## Stok takibinin temel mantığı

Bir stok sisteminin kalbinde **stok hareketi** bulunur. Satın alma stoğu artırırken satış, üretim veya fire azaltır. Belirli bir andaki stok miktarı basitçe şöyle hesaplanabilir:

$$S_{son} = S_{ilk} + Girişler - Çıkışlar$$

Ancak gerçek hayatta yalnızca toplam miktarı bilmek yetmez. Ürünün deposu, rafı, lot numarası, seri numarası ve ayrılmış miktarı da önemlidir. Kullanılabilir stok için şu ifade kullanılabilir:

$$S_{kullanılabilir} = S_{fiziksel} - S_{rezerve}$$

Yeniden sipariş noktası ise ortalama talep ve tedarik süresiyle ilişkilidir:

$$ROP = d \times L + SS$$

Burada $d$ günlük ortalama talebi, $L$ tedarik süresini, $SS$ ise güvenlik stoğunu temsil eder. Yazılım seçerken bu kavramları otomatik yönetebilmesine dikkat edilmelidir.

## Üç sistemin karşılaştırması

| Özellik | Odoo Inventory | ERPNext | PartKeepr |
|---|---|---|---|
| Temel yaklaşım | Modüler ERP ve depo yönetimi | Bütünleşik açık kaynak ERP | Elektronik parça envanteri |
| Uygun ölçek | Orta ve büyük işletmeler | Küçük ve orta işletmeler | Atölye ve laboratuvarlar |
| Lot/seri takibi | Güçlü | Güçlü | Parça odaklı |
| Üretim entegrasyonu | Gelişmiş | Dahili ve erişilebilir | Sınırlı |
| Öğrenme eğrisi | Orta-yüksek | Orta | Düşük-orta |
| Özelleştirme | Python modülleri | DocType ve sunucu betikleri | Daha dar kapsamlı |

![stok-takibinde-uc-80](/img/stok-takibinde-uc-80.svg)


## Odoo Inventory

Odoo, stoğu bağımsız bir ada olarak değil; satış, satın alma, muhasebe ve üretim zincirinin parçası olarak ele alır. Çoklu depo, raf konumları, barkod, rotalar ve otomatik ikmal kuralları konusunda oldukça yeteneklidir. Bir ürün tükendiğinde satın alma emri oluşturmak veya başka depodan transfer başlatmak mümkündür.

Bunun karşılığında kurulum ve yapılandırma daha fazla uzmanlık ister. Ayrıca bazı gelişmiş özelliklerin sürüme veya lisansa bağlı olması, toplam maliyet hesabına katılmalıdır.

## ERPNext

ERPNext, sade arayüz ile kapsamlı ERP özellikleri arasında başarılı bir denge kurar. Depolar, stok girişleri, teslimat notları, satın alma fişleri ve üretim reçeteleri aynı veri modeli üzerinde çalışır. Özellikle açık kaynak bir çözümü hızla devreye almak isteyen ekipler için güçlü bir adaydır.

ERPNext REST API üzerinden otomasyona da uygundur. Örneğin bir ürünün verisini almak için Python ile şu istek gönderilebilir:

```python
import requests

url = "https://erp.example.com/api/resource/Item/URUN-001"
headers = {
    "Authorization": "token API_KEY:API_SECRET"
}

response = requests.get(url, headers=headers, timeout=10)
response.raise_for_status()
item = response.json()["data"]
print(item["item_name"])
```

Bu kod, belirli bir ürün kartını API üzerinden okuyarak harici uygulamalarla entegrasyonun temelini oluşturur. Gerçek projelerde anahtarlar kaynak koda yazılmamalı, ortam değişkenlerinde saklanmalıdır.

## PartKeepr

PartKeepr daha özel bir probleme odaklanır: elektronik bileşenler. Direnç, kondansatör, mikrodenetleyici ve sensör gibi parçaları konum, üretici, teknik parametre ve dosyalarla kataloglamak için kullanışlıdır. “O 10 kΩ direnç hangi çekmecedeydi?” sorusunu saniyeler içinde yanıtlayabilir.

Buna karşın kapsamlı satış, muhasebe veya insan kaynakları bekleniyorsa doğru araç değildir. PartKeepr bir ERP’den çok, teknik atölyeler için düzenli bir dijital parça dolabıdır.

## Hangisini seçmeli?

| İhtiyaç | Öneri |
|---|---|
| Karmaşık lojistik ve çoklu şirket | Odoo Inventory |
| Dengeli, açık kaynak ERP | ERPNext |
| Elektronik parça arşivi | PartKeepr |

Seçimden önce ürün sayısı, günlük hareket hacmi, kullanıcı rolleri ve entegrasyon ihtiyacı belirlenmelidir. En iyi sistem en fazla özelliğe sahip olan değil, ekibin düzenli kullanabildiği sistemdir. Çünkü güncellenmeyen stok kaydı, dijital ortamda saklanan şık bir tahminden ibarettir.
