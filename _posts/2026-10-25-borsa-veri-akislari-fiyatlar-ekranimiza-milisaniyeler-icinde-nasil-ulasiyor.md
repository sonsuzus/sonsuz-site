---
layout: post
title: "Borsa Veri Akışları: Fiyatlar Ekranımıza Milisaniyeler İçinde Nasıl Ulaşıyor?"
math: true
categories: 
  - Bilgi
tags: 
  - borsa
  - finans
  - veri akışı
  - websocket
  - algoritmik ticaret
  - düşük gecikme
toc: true
image: /img/borsa-veri-akislari-31.png
---

Bir hisse fiyatının ekranda yanıp sönmesi basit görünür: Yeşil olduysa yükseldi, kırmızı olduysa düştü. Oysa bu küçük değişikliğin arkasında borsalar, veri dağıtıcıları, özel ağlar, mesaj protokolleri ve milisaniyelerle yarışan yazılımlar bulunur. Gelin, bir emrin borsaya ulaşmasından fiyatın bilgisayarımızda görünmesine kadar geçen dijital yolculuğu inceleyelim.


![borsa-veri-akislari-31](/img/borsa-veri-akislari-31.svg)

``

## Her şey emir defterinde başlar

Borsa, alıcılarla satıcıları eşleştiren merkezi bir pazar gibi çalışır. Yatırımcıların gönderdiği alış ve satış emirleri **emir defterinde** tutulur. Örneğin en yüksek alış emri 99,90 TL, en düşük satış emri 100 TL ise alış-satış farkı, yani *spread*, şöyledir:

$$
\text{Spread} = \text{En iyi satış} - \text{En iyi alış} = 100 - 99{,}90 = 0{,}10\text{ TL}
$$

Bir alış emri mevcut satış emriyle eşleştiğinde işlem gerçekleşir. Borsanın eşleştirme motoru bu işlemi kaydeder ve yeni fiyat, hacim ya da emir defteri değişikliği hakkında bir piyasa verisi mesajı üretir.

## Veri hangi duraklardan geçer?

Tipik akış şu şekildedir:

1. Aracı kurum, yatırımcının emrini borsaya gönderir.
2. Borsanın eşleştirme motoru uygun karşı emri bulur.
3. İşlem veya defter güncellemesi oluşturulur.
4. Borsa, veriyi doğrudan bağlantılara ve veri dağıtıcılarına yayınlar.
5. Aracı kurumun sunucusu mesajı işler.
6. WebSocket gibi sürekli bir bağlantı üzerinden uygulamaya iletir.
7. Arayüz yeni fiyatı ekranda gösterir.

Burada görülen fiyat çoğu zaman tek başına gelmez. Mesaj; sembol, zaman damgası, fiyat, miktar, işlem kimliği ve mesaj sıra numarası gibi alanlar taşır.

| Veri türü | İçerik | Yaygın kullanım |
|---|---|---|
| Son işlem | Gerçekleşen fiyat ve miktar | Fiyat ekranları |
| Seviye 1 | En iyi alış ve satış | Temel alım satım |
| Seviye 2 | Birden fazla fiyat kademesi | Derinlik analizi |
| Tick verisi | Her değişiklik veya işlem | Algoritmik ticaret |
| Gecikmeli veri | Genellikle 15 dakika geriden | Ücretsiz uygulamalar |

## Gerçek zamanlı demek sıfır gecikme değildir

Verinin yolculuğu mutlaka zaman alır. Toplam gecikme yaklaşık olarak bileşenlerine ayrılabilir:

$$
L_{toplam} = L_{borsa} + L_{ağ} + L_{işleme} + L_{istemci}
$$

Borsaya fiziksel olarak yakın veri merkezlerinde çalışan profesyonel sistemler mikrosaniyeleri önemser. Evdeki yatırımcı içinse internet rotası, aracı kurum altyapısı ve tarayıcının çizim süresi nedeniyle gecikme daha yüksek olabilir. Bu nedenle iki uygulamada aynı sembolün fiyatı kısa süreliğine farklı görünebilir.

| Yöntem | Bağlantı modeli | Avantaj | Dezavantaj |
|---|---|---|---|
| REST API | İstek-cevap | Basit ve yaygın | Sürekli sorgulama gerekir |
| WebSocket | Sürekli çift yönlü | Düşük gecikmeli güncelleme | Bağlantı yönetimi ister |
| FIX | Finans odaklı oturum | Standart ve güvenilir | Daha karmaşık |
| Doğrudan veri akışı | Borsaya özel protokol | Çok hızlı | Pahalı ve teknik |

## Bilgisayarda akışı dinlemek

Aşağıdaki Python örneği, temsili bir WebSocket kanalından mesajları alır. Gerçek kullanımda adres, kimlik doğrulama ve mesaj biçimi veri sağlayıcısına göre değişir.

```python
import asyncio
import json
import websockets

async def fiyatlari_dinle():
    adres = "wss://ornek-veri-saglayici.test/stream"

    async with websockets.connect(adres) as baglanti:
        abonelik = {"type": "subscribe", "symbol": "XYZ"}
        await baglanti.send(json.dumps(abonelik))

        async for mesaj in baglanti:
            veri = json.loads(mesaj)
            fiyat = veri.get("price")
            zaman = veri.get("timestamp")
            print(f"{zaman} | XYZ: {fiyat}")

asyncio.run(fiyatlari_dinle())
```

Kod bağlantıyı açık tutar, sembole abone olur ve sunucu yeni mesaj gönderdikçe fiyatı yazdırır. REST API ile her saniye “Yeni fiyat var mı?” diye sormak yerine WebSocket sunucusu değişikliği kendisi iletir.

## Paket kaybı ve sıra numaraları

Hız kadar doğruluk da önemlidir. Her mesaja artan bir sıra numarası eklenebilir. Sistem 105 numaralı mesajdan sonra 107’yi görürse 106’nın kaybolduğunu anlar. Ardından eksik veriyi yeniden ister veya güncel emir defteri görüntüsünü indirir. Aksi hâlde uygulama hızlı ama yanlış bir piyasa resmi gösterebilir.

Kısacası gerçek zamanlı borsa verisi, yalnızca internetten gelen bir sayı değildir. Eşleştirme motorundan başlayan; protokoller, ağlar, sıra kontrolleri ve kullanıcı arayüzüyle tamamlanan hassas bir veri zinciridir. Ekrandaki minicik fiyat hareketinin arkasında oldukça hareketli bir mühendislik piyasası vardır.
