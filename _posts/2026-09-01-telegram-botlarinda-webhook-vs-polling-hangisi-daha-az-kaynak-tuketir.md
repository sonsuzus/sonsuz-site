---
layout: post
title: "Telegram Botlarında Webhook vs Polling: Hangisi Daha Az Kaynak Tüketir?"
math: true
categories: 
  - Bilgi
tags: 
  - telegram-bot
  - webhook
  - polling
toc: true
---

Bir Telegram botu geliştirdiğinizde mesajları nasıl alacağınız konusunda iki temel seçeneğiniz vardır: polling ve webhook. İkisi de aynı güncellemeleri teslim eder; ancak bunu yaparken ağ trafiği, işlemci kullanımı, gecikme ve altyapı gereksinimleri bakımından farklı davranır. Kısacası polling kapıyı sürekli çalıp “Yeni mesaj var mı?” diye sorarken webhook, mesaj geldiğinde kapı zilinin çalmasını bekler.
``
## Polling nasıl çalışır?

Polling yönteminde botunuz Telegram API’sindeki `getUpdates` metoduna düzenli olarak istek gönderir. Telegram, bekleyen mesajları döndürür; mesaj yoksa yanıt boş gelir. En basit polling yaklaşımında istekler kısa aralıklarla tekrarlanır.

Bir bot saniyede $r$ kez sorgu gönderiyorsa günlük yaklaşık istek sayısı şöyle hesaplanabilir:

$$
I = r \times 60 \times 60 \times 24
$$

Örneğin saniyede bir sorgu yapan bot, mesaj gelmese bile günde $86.400$ istek oluşturur. Bu durum ağ ve işlemci açısından gereksiz çalışma anlamına gelir.

Neyse ki **long polling** daha verimlidir. İstek, yeni bir mesaj gelene veya belirlenen zaman aşımı süresi dolana kadar Telegram tarafında açık tutulur. Böylece sürekli bağlantı kurma maliyeti azalır.

```python
import requests

TOKEN = "BOT_TOKEN"
url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
offset = 0

while True:
    response = requests.get(url, params={
        "offset": offset,
        "timeout": 30
    })

    for update in response.json()["result"]:
        offset = update["update_id"] + 1
        print(update)
```

Buradaki `timeout=30`, Telegram’ın bağlantıyı 30 saniyeye kadar açık tutmasını sağlar. `offset` ise aynı mesajın tekrar işlenmesini önler. Kod basittir ve yerel geliştirmede ekstra sunucu yapılandırması gerektirmez.

## Webhook nasıl çalışır?

Webhook kullanımında botunuz Telegram’a erişilebilir bir HTTPS adresi verir. Yeni bir güncelleme geldiğinde Telegram, bu adrese HTTP POST isteği gönderir. Botun sürekli Telegram’ı kontrol etmesine gerek kalmaz.

```python
from flask import Flask, request

app = Flask(__name__)

@app.post("/telegram-webhook")
def telegram_webhook():
    update = request.get_json()
    print(update)
    return "OK", 200

app.run(port=8000)
```

Bu örnekte Flask, Telegram’dan gelen güncellemeleri karşılayan bir uç nokta oluşturur. Gerçek ortamda adresin HTTPS üzerinden internete açık olması, webhook URL’sinin `setWebhook` metoduyla kaydedilmesi ve isteğin hızlıca `200 OK` yanıtı alması gerekir.

## Kaynak tüketimi karşılaştırması

| Ölçüt | Polling | Webhook |
|---|---|---|
| Boşta ağ trafiği | Vardır | Neredeyse yoktur |
| Mesaj gecikmesi | Sorgu aralığına bağlıdır | Genellikle çok düşüktür |
| Kurulum | Kolay | HTTPS ve açık sunucu gerekir |
| CPU kullanımı | Döngü nedeniyle daha yüksek olabilir | Mesaj geldiğinde yükselir |
| Yerel geliştirme | Çok uygundur | Tünel servisi gerekebilir |
| Ölçeklenebilirlik | Orta | Genellikle daha iyi |

Kaynak maliyetini basitleştirerek şu şekilde düşünebiliriz:

$$
C_{polling} = I \times C_{request}
$$

$$
C_{webhook} = M \times C_{request}
$$

Burada $I$ yapılan sorgu sayısını, $M$ ise gelen mesaj sayısını temsil eder. Çoğu botta $I \gg M$ olduğundan webhook daha az ağ isteği ve işlemci zamanı tüketir. Long polling kullanıldığında fark küçülür; çünkü bağlantı sürekli yeniden kurulmaz.

## Hangisini seçmelisiniz?

Botu bilgisayarınızda geliştiriyor, hızlıca deneme yapıyor veya HTTPS sunucusuyla uğraşmak istemiyorsanız long polling oldukça mantıklıdır. Küçük ve düşük trafikli botlarda kaynak tüketimi çoğu zaman sorun yaratmaz.

Üretim ortamında çalışan, yoğun mesaj alan veya sunucusuz platformlarda barındırılan botlarda ise webhook öne çıkar. Olay geldiğinde çalıştığı için boşta kaynak tüketmez ve daha hızlı tepki verir. Ancak webhook uç noktasının güvenliğini doğrulamak, başarısız istekleri izlemek ve işlemleri mümkün olduğunca hızlı tamamlamak gerekir.

Sonuç olarak teorik verimlilik kazananı **webhook** yöntemidir. Pratik kolaylık kupası ise **long polling** seçeneğine gider. Yani yarışın galibi yalnızca hız değil, projenizin altyapısıdır: geliştirmede polling, ölçeklenen üretim sistemlerinde webhook genellikle en dengeli tercihtir.
