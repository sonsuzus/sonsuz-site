---
layout: post
title: "Steganografi: Mesajları Görsel ve Ses Dosyalarının İçinde Saklamak"
math: true
categories: 
  - Bilgi
tags: 
  - steganografi
  - siber güvenlik
  - python
  - veri gizleme
  - görsel işleme
  - kriptografi
toc: true
image: /img/steganografi-mesajlari-gorsel-32.png
---

![steganografi-mesajlari-gorsel-32](/img/steganografi-mesajlari-gorsel-32.svg)


Bir arkadaşınıza gizli bir mesaj göndereceğinizi düşünün. Mesajı şifrelemek onu okunamaz hâle getirir; ancak ortada şifreli bir iletişim bulunduğu yine de fark edilir. Steganografi ise farklı bir numara yapar: Mesajı sıradan görünen bir fotoğrafın, ses kaydının veya videonun içine yerleştirerek iletişimin varlığını saklar. Dijital dünyanın görünmez mürekkebi sayılan bu yöntem, matematikten insan algısının sınırlarına kadar uzanan oldukça eğlenceli bir konudur.
``

## Steganografi ve şifreleme aynı şey mi?

Kriptografi mesajın **içeriğini**, steganografi ise öncelikle mesajın **varlığını** gizler. İki teknik birlikte de kullanılabilir: Önce mesaj şifrelenir, ardından bir görsele gömülür. Böylece gizli veri keşfedilse bile anahtar olmadan okunamaz.

| Yöntem | Gizlenen unsur | Dışarıdan görünen | Temel risk |
|---|---|---|---|
| Kriptografi | Mesajın anlamı | Şifreli veri | Anahtarın ele geçirilmesi |
| Steganografi | Mesajın varlığı | Normal medya dosyası | Gizleme tekniğinin tespit edilmesi |
| İkisi birlikte | Varlık ve anlam | Normal medya dosyası | İstatistiksel analiz ve anahtar kaybı |

## Piksellerin en önemsiz bitleri

Dijital bir RGB görselde her piksel kırmızı, yeşil ve mavi olmak üzere üç kanal taşır. Her kanal çoğunlukla 0–255 arasında, yani 8 bitlik bir değerdir. **LSB** (Least Significant Bit) yönteminde bu değerlerin en sağdaki biti mesaj bitleriyle değiştirilir.

Örneğin `11001010` değeri 202 sayısını temsil eder. Son bit `1` yapılırsa değer `11001011`, yani 203 olur. Bir seviyelik renk değişimini insan gözünün fark etmesi genellikle zordur. Görselin teorik ham kapasitesi yaklaşık olarak

$$C = W \times H \times 3$$

bit olur. Burada $W$ genişliği, $H$ yüksekliği belirtir. Bir bayt 8 bit olduğundan saklanabilecek yaklaşık bayt miktarı $C/8$ ile hesaplanır. Dosya biçimi, başlık bilgisi ve mesaj sonlandırıcısı gerçek kapasiteyi azaltabilir.

## Python ile basit bir LSB deneyi

Aşağıdaki eğitim örneği, kısa bir metni kayıpsız PNG görselinin renk kanallarına yerleştirir. Sonlandırıcı işaret, çıkarma aşamasında mesajın nerede bittiğini bildirir.

```python
from PIL import Image

END = "0000000011111110"

def hide_message(source, target, message):
    image = Image.open(source).convert("RGB")
    pixels = list(image.getdata())

    payload = ''.join(f'{byte:08b}' for byte in message.encode("utf-8")) + END
    channels = [value for pixel in pixels for value in pixel]

    if len(payload) > len(channels):
        raise ValueError("Mesaj bu görsel için fazla uzun.")

    for index, bit in enumerate(payload):
        channels[index] = (channels[index] & 0b11111110) | int(bit)

    rebuilt = [tuple(channels[i:i + 3]) for i in range(0, len(channels), 3)]
    image.putdata(rebuilt)
    image.save(target, "PNG")

hide_message("kaynak.png", "gizli.png", "Merhaba görünmez dünya!")
```

`& 0b11111110` işlemi kanalın son bitini sıfırlar; `| int(bit)` ise mesaj bitini bu konuma yazar. JPEG gibi kayıplı sıkıştırma kullanan biçimler piksel değerlerini değiştirebildiği için basit LSB verisini bozabilir. Bu nedenle örnekte PNG tercih edilir.

## Ses dosyalarında gizleme

Ses steganografisinde benzer işlem PCM örneklerinin düşük anlamlı bitlerinde uygulanabilir. İnsan kulağının daha az hassas olduğu frekanslara veri ekleyen gelişmiş yöntemler de vardır.

| Taşıyıcı | Avantaj | Dezavantaj |
|---|---|---|
| PNG görsel | Piksel değerlerini korur | Yeniden boyutlandırma veriyi bozabilir |
| WAV ses | Ham örneklere erişim kolaydır | Dosya boyutu büyüktür |
| JPEG/MP3 | Yaygın ve küçüktür | Kayıplı sıkıştırma uygulanır |

## Görünmez olmak, tespit edilemez olmak değildir

Steganaliz araçları renk dağılımlarındaki düzensizlikleri, dosya boyutunu ve bit örüntülerini inceleyerek gizli veri arar. Mesaj büyüdükçe istatistiksel iz de artar. Sağlam sistemler kapasite, algılanabilirlik ve dayanıklılık arasında denge kurar. Teknik; filigranlama, telif takibi ve bütünlük doğrulama gibi meşru amaçlara hizmet edebilir. Ancak izinsiz veri saklamak etik ve hukuki sorunlar doğurabileceğinden deneyler yalnızca size ait dosyalarda ve kontrollü ortamlarda yapılmalıdır.
