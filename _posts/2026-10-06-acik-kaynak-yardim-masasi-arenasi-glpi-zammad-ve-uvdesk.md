---
layout: post
title: "Açık Kaynak Yardım Masası Arenası: GLPI, Zammad ve UVdesk"
math: true
categories: 
  - Program
tags: 
  - yardım masası
  - glpi
  - zammad
  - uvdesk
  - açık kaynak
  - itil
  - destek sistemi
toc: true
image: /img/acik-kaynak-yardim-33.png
---

E-postalar, telefon notları ve “Abi yazıcı yine çalışmıyor” mesajları arasında kaybolan destek taleplerini düzenlemenin yolu, iyi bir yardım masası sisteminden geçer. GLPI, Zammad ve UVdesk bu iş için öne çıkan açık kaynaklı seçeneklerdir. Üçü de talepleri bilete dönüştürür; ancak varlık yönetimi, müşteri iletişimi ve e-ticaret desteği gibi konularda farklı karakterlere sahiptir.

``

## Yardım masası sisteminin mantığı

Yardım masası yazılımı, dağınık destek isteklerini izlenebilir **biletlere** dönüştürür. Bir bilet; talep sahibi, sorumlu personel, öncelik, durum, kategori ve çözüm süresi gibi alanlardan oluşur. Temel yaşam döngüsü genellikle şöyledir:

1. Kullanıcı talep oluşturur.
2. Sistem talebi uygun kuyruğa yönlendirir.
3. Bir temsilci bileti üstlenir.
4. Sorun araştırılır ve yanıtlanır.
5. Çözüm doğrulanarak bilet kapatılır.

Bu süreçte SLA, yani hizmet seviyesi anlaşması önemlidir. Örneğin izin verilen çözüm süresi $T_{SLA}$, gerçek çözüm süresi $T_{çözüm}$ ise uyumluluk şöyle ifade edilebilir:

$$
SLA\ Uyumu = \frac{T_{SLA}\ içinde\ çözülen\ biletler}{Toplam\ biletler} \times 100
$$

Sistem yalnızca kayıt tutmamalı; önceliklendirme, otomasyon, raporlama ve bilgi tabanı özellikleriyle ekibin hafızası hâline gelmelidir.

## Üç rakibin kısa karşılaştırması

| Özellik | GLPI | Zammad | UVdesk |
|---|---|---|---|
| Ana odak | BT hizmet ve varlık yönetimi | Çok kanallı müşteri desteği | Müşteri ve e-ticaret desteği |
| Varlık envanteri | Çok güçlü | Sınırlı | Sınırlı |
| E-posta yönetimi | Var | Çok güçlü | Güçlü |
| Bilgi tabanı | Eklenti veya yerleşik seçenekler | Yerleşik | Yerleşik |
| Arayüz | İşlevsel, yoğun | Modern ve akıcı | Sade, müşteri odaklı |
| Kurulum zorluğu | Orta | Orta | Orta |
| Uygun ekip | Sistem ve BT ekipleri | Destek merkezleri | KOBİ ve e-ticaret ekipleri |

## GLPI: Envanter ustası

GLPI, klasik bir bilet sisteminden fazlasıdır. Bilgisayarları, monitörleri, yazıcıları, lisansları, sözleşmeleri ve kullanıcıları merkezi biçimde yönetebilir. “Bu dizüstü bilgisayar kimde?” sorusuna saniyeler içinde yanıt vermek isteyen BT ekipleri için güçlüdür.

ITIL yaklaşımına yakın olay, talep, problem ve değişiklik yönetimi sunar. Buna karşılık çok sayıda menü ve alan, küçük ekipler için başlangıçta karmaşık görünebilir. Envanter ile destek süreçlerini aynı çatı altında toplamak istiyorsanız GLPI öne çıkar.

## Zammad: İletişim merkezinin yıldızı

Zammad; e-posta, web formu, sohbet ve çeşitli sosyal kanal entegrasyonlarından gelen mesajları tek ekranda toplar. Temsilciler bilet geçmişini rahatça izleyebilir, etiketler ekleyebilir ve otomatik tetikleyiciler tanımlayabilir.

REST API desteği sayesinde başka uygulamalardan bilet oluşturmak da mümkündür:

```python
import requests

payload = {
    "title": "Ödeme ekranında hata",
    "group": "Destek",
    "customer": "musteri@example.com",
    "article": {
        "subject": "Ödeme sorunu",
        "body": "Kullanıcı ödeme adımını tamamlayamıyor.",
        "type": "note",
        "internal": False
    }
}

response = requests.post(
    "https://destek.example.com/api/v1/tickets",
    json=payload,
    headers={"Authorization": "Token token=API_TOKEN"}
)
print(response.status_code)
```

Bu kod, başka bir uygulamada oluşan hatayı otomatik olarak Zammad bileti hâline getirir. Böylece kullanıcı ayrıca destek formu doldurmak zorunda kalmaz.

## UVdesk: E-ticaret dostu

Symfony tabanlı UVdesk, özellikle çevrim içi mağazalara destek veren ekipleri hedefler. WooCommerce ve çeşitli e-ticaret platformlarıyla kurulabilen bağlantılar sayesinde temsilci, müşterinin sipariş bağlamını destek ekranında görebilir.

UVdesk’in arayüzü görece sadedir ve bilgi tabanı oluşturmayı kolaylaştırır. Ancak kapsamlı donanım envanteri veya ileri seviye kurumsal BT süreçleri gerektiğinde GLPI kadar derin değildir.

## Hangisini seçmeli?

Seçimi basit bir ağırlıklı puanla yapabilirsiniz:

$$
Puan = 0.4E + 0.3K + 0.2A + 0.1M
$$

Burada $E$ envanter, $K$ kanal yönetimi, $A$ API ve otomasyon, $M$ ise kullanım kolaylığı puanıdır. Donanım ve lisans yönetimi öncelikliyse **GLPI**, modern çok kanallı destek gerekiyorsa **Zammad**, e-ticaret müşterilerine hızlı hizmet verilecekse **UVdesk** daha mantıklıdır. En doğru karar için üç sistemi de örnek biletler, gerçek kullanıcı rolleri ve ölçülebilir SLA senaryolarıyla test etmek gerekir.

![acik-kaynak-yardim-33](/img/acik-kaynak-yardim-33.svg)

