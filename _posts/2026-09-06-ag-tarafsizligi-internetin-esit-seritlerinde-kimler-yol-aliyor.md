---
layout: post
title: "Ağ Tarafsızlığı: İnternetin Eşit Şeritlerinde Kimler Yol Alıyor?"
math: true
categories: 
  - Bilgi
tags: 
  - ağ tarafsızlığı
  - bilgisayar ağları
  - internet politikaları
toc: true
---

Bir video izlerken görüntünün donduğunu, aynı anda servis sağlayıcınızın kendi video platformunun kusursuz çalıştığını düşünün. Bu durum teknik bir arızadan çok daha fazlası olabilir: Ağ tarafsızlığı tartışmasının tam merkezindesiniz. Ağ tarafsızlığı, internet servis sağlayıcılarının paketleri kaynağına, hedefine, içeriğine veya uygulamasına göre haksız biçimde engellememesi, yavaşlatmaması ya da ücretli “hızlı şeritlere” ayırmaması ilkesidir.
``

## İnternet Paketleri Neden “Tarafsız” Olmalı?

İnternette gönderilen bir e-posta, oyun komutu veya video parçası küçük veri paketlerine bölünür. IP katmanındaki yönlendiriciler, ideal olarak paketin taşıdığı fikre değil hedef adresine bakar. Bu yaklaşım **uçtan uca ilkesi** ile ilişkilidir: Ağın çekirdeği genel amaçlı ve sade kalırken yenilikler uç cihazlarda geliştirilir.

Bir bağlantının yaklaşık aktarım süresi şöyle modellenebilir:

$$T_{toplam} = T_{iletim} + T_{yayılım} + T_{işleme} + T_{kuyruk}$$

Burada özellikle $T_{kuyruk}$, yoğunluk veya bilinçli trafik yönetimi nedeniyle büyüyebilir. Servis sağlayıcı belirli bir uygulamanın paketlerini düşük öncelikli kuyruğa yerleştirirse kullanıcı bunu gecikme, donma veya düşük görüntü kalitesi olarak hisseder.

| Uygulama | Temel ağ ihtiyacı | Ayrımcılığın olası sonucu |
|---|---|---|
| Web gezintisi | Orta bant genişliği | Sayfaların geç açılması |
| Görüntülü görüşme | Düşük gecikme, düşük jitter | Ses kesilmesi ve donma |
| Video akışı | Yüksek ve kararlı bant genişliği | Çözünürlüğün düşmesi |
| Çevrim içi oyun | Çok düşük gecikme | Komutların geç işlenmesi |

## Ayrım Teknik Olarak Nasıl Yapılabilir?

Yönlendiriciler **QoS (Quality of Service)** mekanizmalarıyla paketleri sınıflandırabilir. Port numarası, IP adresi, protokol veya DPI adı verilen derin paket inceleme yöntemi kullanılabilir. Ardından öncelikli kuyruklama, bant genişliği sınırlama ve trafik şekillendirme uygulanabilir.

QoS özünde kötü değildir. Acil durum çağrısına öncelik vermek veya ağ saldırısını bastırmak mantıklıdır. Sorun, aynı araçların ticari rakipleri yavaşlatmak için kullanılmasıdır.

Aşağıdaki basitleştirilmiş Python örneği, paketlerin uygulama adına göre farklı gecikmelere maruz bırakılmasını simgeler:

```python
import time

gecikmeler = {
    "saglayici_video": 0.01,
    "rakip_video": 0.20,
    "web": 0.05
}

def paketi_isle(uygulama, veri):
    gecikme = gecikmeler.get(uygulama, 0.05)
    time.sleep(gecikme)
    return f"{uygulama}: {len(veri)} bayt iletildi"

print(paketi_isle("rakip_video", b"video-paketi"))
```

Gerçek ağ cihazları elbette milyonlarca paketi donanım hızında işler. Ancak örnekteki sözlük, politika tablosunu; `sleep` ise yapay kuyruk gecikmesini temsil eder.

## Makul Yönetim ile Ayrımcılık Arasındaki Çizgi

| Makul trafik yönetimi | Tarafsızlığa aykırı davranış |
|---|---|
| Yoğunluk sırasında geçici önlem | Rakip servisi sürekli yavaşlatma |
| Zararlı trafiği engelleme | Yasal içeriği siyasi nedenle engelleme |
| Uygulamadan bağımsız kota | Belirli uygulamaya ayrıcalıklı kota |
| Şeffaf QoS politikası | Gizli ücretli önceliklendirme |

Bir kuyruğun kapasitesi $C$, toplam trafik talebi ise $R$ olsun. $R > C$ olduğunda tüm paketlerin aynı anda iletilmesi mümkün değildir. Bu nedenle teknik önceliklendirme bazen kaçınılmazdır. Kritik soru şudur: Karar performans gereksinimine göre mi, yoksa ödeme gücü ve kurumsal çıkara göre mi veriliyor?

## Sosyopolitik Önemi

Ağ tarafsızlığı yalnızca mühendislerin yönlendirici ayarlarından ibaret değildir. Yeni kurulmuş küçük bir girişimin, dev bir platformla kullanıcının ekranına ulaşma konusunda eşit şansa sahip olmasını etkiler. Ücretli hızlı şeritler yaygınlaşırsa sermayesi yüksek şirketler daha kaliteli erişim satın alabilir; küçük geliştiriciler ise teknik olarak çevrim içi olsalar bile pratikte görünmezleşebilir.

Konu ifade özgürlüğüyle de bağlantılıdır. Servis sağlayıcının haber sitelerini, toplumsal hareketleri veya belirli görüşleri yavaşlatabilmesi, altyapı sahibine editoryal güce benzeyen bir yetki verir. Öte yandan sağlayıcılar, kapasite yatırımlarını finanse edebilmek için fiyatlandırma esnekliği gerektiğini savunur.

Sağlıklı bir yaklaşım; şeffaflık, bağımsız denetim, kullanıcıya gerçek seçim hakkı ve teknik olarak gerekçelendirilebilir trafik yönetimini birlikte gerektirir. İnternetin eşitliği, her paketin fiziksel olarak aynı hızda gitmesi değil, dijital yolların kurallarının adil, açık ve kötüye kullanıma kapalı olmasıdır.
