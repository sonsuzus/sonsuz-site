---
layout: post
title: "Açık Kaynak Müşteri Destek Arenası: Chatwoot, Zammad ve FreeScout"
math: true
categories: 
  - Program
tags: 
  - müşteri desteği
  - chatwoot
  - zammad
  - freescout
  - açık kaynak
  - self-hosted
toc: true
image: /img/acik-kaynak-musteri-99.png
---

![acik-kaynak-musteri-99](/img/acik-kaynak-musteri-99.svg)


Müşteri desteği artık yalnızca e-posta yanıtlamaktan ibaret değil. Kullanıcılar canlı sohbetten yazıyor, sosyal medyadan sesleniyor ve bazen aynı soruyu üç farklı kanaldan gönderiyor. Bu iletişim trafiğini tek merkezde toplamak isteyen ekiplerin karşısına üç güçlü açık kaynak seçeneği çıkıyor: Chatwoot, Zammad ve FreeScout. Peki hangisi sizin destek üssünüz olmalı?
``

## Önce mantık: Destek sistemi neyi çözer?

Bir müşteri destek sistemi, farklı kanallardan gelen mesajları takip edilebilir **kayıtlara** dönüştürür. Her kayıt bir temsilciye atanabilir, etiketlenebilir, önceliklendirilebilir ve sonuçlanana kadar izlenebilir. Böylece kişisel posta kutularında kaybolan mesajların yerini ortak bir iş akışı alır.

Sistemin temel performansı kabaca şu oranla değerlendirilebilir:

$$\text{Çözüm Oranı} = \frac{\text{Çözülen Talep Sayısı}}{\text{Toplam Talep Sayısı}} \times 100$$

Ortalama ilk yanıt süresi ise müşteri deneyiminin önemli göstergelerindendir:

$$T_{yanıt} = \frac{\sum_{i=1}^{n}(t_{ilk\ yanıt,i}-t_{oluşturma,i})}{n}$$

Yazılım seçerken yalnızca özellik listesini değil; ekibin iletişim kanallarını, teknik kapasitesini ve beklenen talep hacmini de hesaba katmak gerekir.

## Üç adayın karakteri

**Chatwoot**, canlı sohbet ve çok kanallı iletişim merkezidir. Web sitesi sohbeti, e-posta, WhatsApp, Facebook ve benzeri kanalları ortak gelen kutusunda birleştirmesiyle öne çıkar. Modern arayüzü sayesinde satış ve destek ekipleri birlikte çalışabilir.

**Zammad**, klasik yardım masası disiplinine daha yakındır. Bilet yönetimi, roller, ayrıntılı yetkilendirme, SLA kuralları ve kurumsal iş akışları güçlüdür. Bir talebin kimde olduğunu ve ne zaman yanıtlanması gerektiğini sıkı biçimde takip etmek isteyen ekipleri hedefler.

**FreeScout** ise hafif ve tanıdık bir ortak posta kutusu deneyimi sunar. Help Scout benzeri arayüzü, düşük kaynak tüketimi ve modüler yapısıyla küçük ekiplerin hızlı başlangıç yapmasını sağlar.

| Ölçüt | Chatwoot | Zammad | FreeScout |
|---|---|---|---|
| Ana yaklaşım | Çok kanallı sohbet | Kurumsal bilet yönetimi | Ortak e-posta kutusu |
| Canlı sohbet | Çok güçlü | Mevcut | Eklenti gerekebilir |
| SLA ve süreçler | Orta | Çok güçlü | Temel/eklentili |
| Kaynak ihtiyacı | Orta-yüksek | Orta-yüksek | Düşük |
| Kurulum kolaylığı | Orta | Orta | Kolay |
| İdeal ekip | Dijital ürün ve satış | BT, kamu, büyük destek ekibi | Küçük işletme |

## Entegrasyon neden önemlidir?

Destek yazılımı tek başına yaşamaz; CRM, sipariş sistemi veya şirket içi uygulamalarla konuşmalıdır. Webhook yaklaşımında sistem, olay gerçekleştiğinde belirlediğiniz adrese HTTP isteği gönderir. Aşağıdaki Python örneği, gelen olaydan bilet kimliğini ve mesajı okuyarak basit bir otomasyon başlatır:

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.post("/support-webhook")
def support_webhook():
    event = request.get_json()
    ticket_id = event.get("conversation_id") or event.get("ticket_id")
    message = event.get("content", "")

    if "iade" in message.lower():
        print(f"{ticket_id}: Finans ekibine yönlendirildi")

    return jsonify({"received": True}), 200

app.run(port=5000)
```

Bu kod üretim ortamı için kimlik doğrulama, hata yönetimi ve imza doğrulaması gerektirir; ancak üç platformun da API veya webhook mekanizmalarıyla nasıl genişletilebileceğini gösterir.

## Hangisini seçmelisiniz?

Müşterileriniz ağırlıklı olarak canlı sohbet ve mesajlaşma kanallarındaysa **Chatwoot** doğal seçimdir. Ayrıntılı roller, SLA takibi ve denetlenebilir kurumsal süreçler gerekiyorsa **Zammad** daha sağlam bir omurga sunar. Temel ihtiyacınız birkaç kişinin aynı destek e-postasını düzenli biçimde yönetmesiyse **FreeScout**, gereksiz karmaşıklık oluşturmadan işi çözer.

Karar vermeden önce gerçek taleplerle küçük bir pilot kurulum yapın. Temsilcilerin tıklama sayısını, ilk yanıt süresini ve çözülemeyen kayıtları ölçün. En iyi destek sistemi en uzun özellik listesine sahip olan değil, ekibinizin her gün isteyerek kullandığı sistemdir.
