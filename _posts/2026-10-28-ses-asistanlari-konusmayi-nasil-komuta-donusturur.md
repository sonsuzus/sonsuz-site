---
layout: post
title: "Ses Asistanları Konuşmayı Nasıl Komuta Dönüştürür?"
math: true
categories: 
  - Bilgi
tags: 
  - doğal dil işleme
  - ses asistanları
  - yapay zeka
  - makine öğrenmesi
  - konuşma tanıma
toc: true
image: /img/ses-asistanlari-konusmayi-50.png
---

Alexa’ya ışıkları açmasını söylediğinizde birkaç saniye içinde odanın aydınlanması sihir gibi görünebilir. Oysa perde arkasında ses sinyalini metne, metni anlama ve nihayetinde çalıştırılabilir bir komuta dönüştüren çok katmanlı bir doğal dil işleme mimarisi vardır. Mikrofon dizilerinden derin öğrenme modellerine kadar uzanan bu zincir, küçük bir cümleyi dijital bir eyleme çevirir.
``
## Uyanma kelimesi ve sesin yakalanması

Ses asistanı çevresindeki sesi sürekli dinler; ancak genellikle tüm konuşmaları buluta göndermez. Cihaz üzerindeki hafif bir model, Alexa veya Hey Google gibi bir **uyandırma kelimesini** arar. Bu yaklaşım hem işlem maliyetini azaltır hem de mahremiyet açısından önemli bir filtre oluşturur.

Bir mikrofonun yakaladığı analog ses, örnekleme yoluyla sayısallaştırılır. Örnekleme frekansı $f_s$ ise Nyquist ilkesine göre algılanabilecek en yüksek frekans yaklaşık olarak şöyledir:

$$f_{max} = \frac{f_s}{2}$$

Örneğin $16\,kHz$ ile örneklenen bir kayıt, insan konuşmasının büyük bölümünü kapsayan $8\,kHz$ seviyesine kadar frekansları temsil edebilir. Birden fazla mikrofon kullanıldığında **beamforming**, konuşmacının yönüne odaklanırken televizyon veya klima gibi gürültü kaynaklarını bastırır.

## Sesten metne: Otomatik konuşma tanıma

Uyandırma kelimesinden sonraki ses, otomatik konuşma tanıma sistemine yani **ASR** katmanına aktarılır. Önce sinyal kısa parçalara ayrılır ve mel frekanslı spektrogram gibi özelliklere dönüştürülür. Modern sistemlerde Transformer veya Conformer tabanlı modeller, bu özelliklerden olası kelime dizilerini tahmin eder.

Modelin amacı en olası metni bulmaktır:

$$\hat{W} = \arg\max_W P(W \mid X)$$

Burada $X$ ses özelliklerini, $W$ ise kelime dizisini temsil eder. Dil modeli sayesinde Ben ışığı aç gibi anlamsız bir tahmin yerine Bir ışığı aç veya Salon ışığını aç gibi bağlama uygun sonuçlar öne çıkar.

| Katman | Girdi | Çıktı | Temel görev |
|---|---|---|---|
| Sinyal işleme | Ham ses | Temizlenmiş ses | Gürültüyü azaltmak |
| ASR | Ses özellikleri | Metin | Konuşmayı yazıya çevirmek |
| NLU | Metin | Niyet ve varlıklar | Kullanıcıyı anlamak |
| Diyalog yönetimi | Yapısal anlam | Eylem kararı | Sonraki adımı seçmek |
| TTS | Yanıt metni | Yapay ses | Kullanıcıya cevap vermek |

## Metinden niyete: Doğal dil anlama

ASR katmanı Salonun ışığını yüzde elliye getir metnini ürettiğinde iş henüz bitmez. **NLU** katmanı cümleyi iki temel parçaya ayırır:

- **Niyet:** Işık seviyesini değiştirme
- **Varlıklar:** Oda = salon, seviye = yüzde 50

Kural tabanlı sistemler belirli kalıpları ararken öğrenen modeller farklı söyleyişleri genelleyebilir.

| Yaklaşım | Avantaj | Dezavantaj |
|---|---|---|
| Kural tabanlı | Açıklanabilir ve hızlıdır | Yeni cümlelere karşı kırılgandır |
| Makine öğrenmesi | Farklı ifadeleri geneller | Etiketli veriye ihtiyaç duyar |
| Büyük dil modeli | Bağlamı güçlü yorumlar | Maliyet ve gecikme oluşturabilir |

Basitleştirilmiş bir komut ayrıştırıcı şöyle yazılabilir:

```python
def komutu_cozumle(metin):
    metin = metin.lower()

    if "ışık" in metin and "aç" in metin:
        return {
            "niyet": "isigi_ac",
            "oda": "salon" if "salon" in metin else "bilinmiyor"
        }

    return {"niyet": "anlasilmadi"}
```

Bu kod, metinde ışık ve aç sözcüklerini arayarak temel bir niyet üretir. Gerçek sistemler ise eş anlamlı ifadeleri, kelime sırasını, olumsuzluğu ve önceki konuşmaları da hesaba katar.

## Diyalog yönetimi ve eylem

Diyalog yöneticisi eksik bilgiyi belirler. Kullanıcı Işığı aç dediğinde hangi odanın kastedildiği bilinmiyorsa asistan Hangi odadaki ışığı açmalıyım? diye sorabilir. Yeterli bilgi varsa akıllı ev servisine yapılandırılmış bir istek gönderilir:

```json
{
  "action": "turn_on",
  "device": "light",
  "room": "living_room"
}
```

Servisten başarılı yanıt geldiğinde **TTS**, yani metinden konuşmaya sentez katmanı devreye girer ve Salonun ışığını açtım cümlesini doğal sese dönüştürür.

Kısacası ses asistanı tek bir dev model değil; sinyal işleme, ASR, NLU, diyalog yönetimi, servis entegrasyonu ve TTS bileşenlerinin uyumlu bir orkestrasıdır. Kullanıcı yalnızca birkaç kelime söyler, fakat sistem bu kelimeleri duyar, olasılıklarla çözümler, anlamlandırır, güvenli biçimde uygular ve sonucu konuşarak bildirir.

![ses-asistanlari-konusmayi-50](/img/ses-asistanlari-konusmayi-50.svg)

