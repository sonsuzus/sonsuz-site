---
layout: post
title: "Blokzinciri Kriptodan İbaret Değil: Finans Dışı Kullanım Senaryoları"
math: true
categories: 
  - Bilgi
tags: 
  - blokzinciri
  - dağıtık defter
  - veri güvenliği
toc: true
---

Blokzinciri denildiğinde akla ilk olarak Bitcoin gelse de teknoloji, dijital para üretmekten çok daha genel bir probleme çözüm sunar: Birbirine tam olarak güvenmeyen tarafların, ortak bir veri geçmişi üzerinde anlaşabilmesi. Bu özellik; domatesin tarladan markete yolculuğunu izlemekten sağlık kayıtlarının değişmediğini kanıtlamaya kadar şaşırtıcı derecede geniş bir kullanım alanı oluşturur.

``

## Temel fikir: Veriyi saklamak değil, geçmişi kanıtlamak

Blokzinciri, kayıtların zaman sırasıyla bloklara yerleştirildiği ve her bloğun önceki bloğa kriptografik olarak bağlandığı dağıtık bir defterdir. Bir kaydın özeti, yani hash değeri, kabaca şu fonksiyonla gösterilebilir:

$$h = H(veri)$$

Veride tek bir karakter değişirse $h$ değeri de tamamen değişir. Bloklar önceki bloğun hash değerini taşıdığı için eski bir kaydı değiştirmek, kendisinden sonraki bağlantıları da bozar. Ağdaki düğümler farklı kopyaları karşılaştırarak tutarsızlığı fark edebilir.

Buradaki kritik ayrım şudur: Blokzinciri, girilen bilginin gerçek olduğunu kendiliğinden garanti etmez; bilginin sonradan değiştirilmediğini kanıtlamayı kolaylaştırır. Yanlış veri zincire yazılırsa elimizde yalnızca değiştirilemeyen bir yanlış bulunur. Bu probleme bazen “çöp girer, çöp çıkar” ilkesi denir.

| Yaklaşım | Yönetim | Değişiklik tespiti | Uygun olduğu durum |
|---|---|---|---|
| Merkezi veritabanı | Tek kurum | Yetkilere ve loglara bağlı | Taraflar aynı kuruma güveniyorsa |
| İzinli blokzinciri | Seçilmiş kurumlar | Dağıtık doğrulama ile güçlü | Şirketler ortak kayıt tutuyorsa |
| Açık blokzinciri | Herkese açık ağ | Konsensüs ile güçlü | Kamusal doğrulanabilirlik gerekiyorsa |

## Tedarik zincirinde dijital ürün pasaportu

Bir ürünün üretim, taşıma, depolama ve satış adımları farklı şirketlerin sistemlerinde tutulur. Sorun çıktığında hangi kaydın doğru olduğu tartışmaya dönüşebilir. İzinli bir blokzincirinde üretici parti numarasını, lojistik firması sıcaklık ölçümlerinin özetini, mağaza ise teslim zamanını kaydedebilir.

Örneğin soğuk zincirde sıcaklık sınırı $8\,^{\circ}\mathrm{C}$ olsun. Sensör ölçümlerinin tamamını zincire yazmak pahalı ve mahremiyet açısından sakıncalıdır. Bunun yerine büyük veri dosyası harici depoda tutulur, yalnızca hash değeri zincire eklenir. Böylece dosyanın sonradan değiştirilip değiştirilmediği doğrulanabilir.

## Sağlık kayıtlarını güvenli biçimde mühürlemek

Hasta dosyalarının herkese açık bir zincire yazılması ciddi bir hata olur. Sağlık verileri silinme, erişim kontrolü ve mahremiyet gerektirir. Daha uygun tasarımda gerçek kayıt hastanenin güvenli sisteminde kalır; blokzincirine kaydın özeti, zaman damgası ve yetkilendirme olayı yazılır.

Aşağıdaki Python örneği, bir sağlık kaydının dijital parmak izini üretir:

```python
import hashlib
import json

def kaydi_muhurle(kayit):
    # Anahtarları sıralamak, aynı veri için tutarlı çıktı sağlar.
    metin = json.dumps(kayit, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(metin.encode('utf-8')).hexdigest()

kayit = {
    'hasta_kodu': 'P-1042',
    'islem': 'Laboratuvar sonucu oluşturuldu',
    'tarih': '2026-08-19'
}

print(kaydi_muhurle(kayit))
```

Aylar sonra dosyadan yeniden hash üretilir. Yeni değer zincirdeki mühürle eşleşiyorsa kayıt değişmemiştir. Ancak hash, veriyi şifrelemez; tahmin edilebilir hassas bilgiler ek koruma olmadan hashlenmemelidir.

## Başka hangi sektörler dönüşebilir?

Eğitim kurumları diplomaların hash değerlerini yayımlayarak sahte belge kontrolünü hızlandırabilir. Belediyeler ruhsat süreçlerinin zaman damgalı geçmişini paylaşabilir. Enerji ağlarında üreticiler yenilenebilir kaynak sertifikalarını izleyebilir. Telif sistemlerinde ise bir eserin belirli tarihte var olduğu kanıtlanabilir; fakat zincire kayıt yaptırmak tek başına hukuki sahiplik oluşturmaz.

## Her probleme blokzinciri eklemeyin

Taraflar tek bir güvenilir kurumun veritabanını kabul ediyorsa blokzinciri gereksiz maliyet, gecikme ve yönetim karmaşası yaratabilir. İyi bir kullanım senaryosunda birden fazla bağımsız taraf, ortak geçmiş, denetlenebilirlik ve kayıt değişikliklerine karşı direnç birlikte bulunur. Teknolojinin gerçek gücü “veriyi zincire atalım” yaklaşımında değil, güvenin kurumlar arasında nasıl dağıtılacağını dikkatle tasarlamaktadır.
