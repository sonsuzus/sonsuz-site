---
layout: post
title: "Kendi Dosya Dönüştürme Siteni Kur: ConvertX, Stirling PDF ve CloudConvert Alternatifleri"
math: true
categories: 
  - Proje
tags: 
  - dosya dönüştürme
  - self-hosted
  - docker
  - python
  - pdf
  - açık kaynak
toc: true
image: /img/kendi-dosya-donusturme-80.png
---

Bir DOCX dosyasını PDF’ye, PNG görselini WebP’ye veya videoyu MP3’e çevirmek basit görünür. Ancak perde arkasında farklı araçların yönetilmesi, dosya güvenliği, kuyruk sistemi ve kaynak sınırlandırması bulunur. ConvertX, Stirling PDF ve CloudConvert gibi servisler bu karmaşayı kullanıcıdan gizler. Peki gizliliği önceleyen, kendi sunucumuzda çalışan benzer bir sistem kurmak istersek hangi yaklaşımı seçmeliyiz?

``

## Dönüştürme işleminin temel mantığı

Dosya dönüştürme, yalnızca uzantıyı değiştirmek değildir. Kaynak dosya önce ayrıştırılır, içindeki veri uygun bir ara modele aktarılır ve hedef biçimin kurallarına göre yeniden kodlanır. Örneğin bir görsel dönüştürülürken piksel verisi korunabilir fakat sıkıştırma algoritması değişir.

Kayıplı dönüşümlerde kalite ile dosya boyutu arasında denge kurulur. Basitleştirilmiş biçimde bu ilişkiyi şöyle gösterebiliriz:

$$Q \propto \frac{1}{C}$$

Burada $Q$ algılanan kaliteyi, $C$ ise sıkıştırma miktarını temsil eder. Sıkıştırma yükseldikçe dosya küçülür; ancak özellikle JPEG, MP3 ve video biçimlerinde kalite kaybı artabilir.

## Hangi çözüm ne sunuyor?

| Çözüm | Çalışma modeli | Güçlü tarafı | Uygun kullanım |
|---|---|---|---|
| ConvertX | Self-hosted | Sade arayüz ve çoklu format | Kişisel veya ekip içi dönüşümler |
| Stirling PDF | Self-hosted | Kapsamlı PDF araçları | Birleştirme, OCR, bölme ve imzalama |
| CloudConvert | Bulut/SaaS | Geniş format ve API desteği | Ölçeklenebilir ticari uygulamalar |
| Özel servis | Self-hosted | Tam kontrol ve özelleştirme | Ürüne özel iş akışları |

![kendi-dosya-donusturme-80](/img/kendi-dosya-donusturme-80.svg)


Yalnızca PDF işlemleri gerekiyorsa Stirling PDF oldukça güçlüdür. Çok sayıda dosya türü için ConvertX daha genel bir başlangıç sunar. Bakım yapmak istemeyen ekipler CloudConvert’i değerlendirebilir. Hassas belgeler söz konusuysa self-hosted yaklaşım öne çıkar.

## Küçük bir dönüştürme mimarisi

Pratik bir sistem dört parçadan oluşabilir: dosyayı alan web API’si, işleri sıraya koyan Redis, dönüşümü gerçekleştiren worker ve sonuçları geçici olarak saklayan depolama alanı. Worker tarafında LibreOffice, FFmpeg, ImageMagick ve Pandoc gibi kanıtlanmış araçlardan yararlanılabilir.

Ortalama işlem süresi $t$, worker sayısı $w$ ve bekleyen iş sayısı $n$ ise yaklaşık tamamlanma süresi şöyle tahmin edilebilir:

$$T \approx \frac{n \times t}{w}$$

Dolayısıyla worker sayısını artırmak kuyruğu hızlandırır; fakat CPU ve bellek tüketimini de büyütür. Sunucunun bir tost makinesine dönüşmesini istemiyorsak kaynak limitleri şarttır.

## FastAPI ile DOCX → PDF örneği

Aşağıdaki uç nokta yüklenen DOCX dosyasını geçici bir dizine kaydeder ve LibreOffice’i arayüzsüz modda çalıştırır:

```python
from pathlib import Path
from tempfile import TemporaryDirectory
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse
import subprocess

app = FastAPI()

@app.post("/convert/docx-to-pdf")
async def convert(file: UploadFile):
    if not file.filename.lower().endswith(".docx"):
        raise HTTPException(400, "Yalnızca DOCX kabul edilir")

    temp = TemporaryDirectory()
    workdir = Path(temp.name)
    source = workdir / "input.docx"
    source.write_bytes(await file.read())

    subprocess.run(
        ["libreoffice", "--headless", "--convert-to", "pdf",
         "--outdir", str(workdir), str(source)],
        check=True,
        timeout=60
    )

    result = workdir / "input.pdf"
    return FileResponse(result, filename="converted.pdf")
```

Kod öğretici bir iskelettir. Gerçek projede geçici dizinin yanıt tamamlanmadan silinmemesi, dosya boyutu sınırı, benzersiz adlandırma ve hata kayıtları ayrıca ele alınmalıdır.

## Güvenlik, projenin görünmez kahramanıdır

Kullanıcı dosyaları güvenilir kabul edilmemelidir. Dönüştürücüleri ayrı Docker konteynerlerinde, yetkisiz kullanıcıyla ve sınırlı CPU/bellek altında çalıştırın. Dosya uzantısına değil MIME türüne bakın; makroları engelleyin, işlem zaman aşımı belirleyin ve sonuçları otomatik silin. Komut oluştururken kullanıcı girdisini kabuk metnine eklemek yerine argüman listesi kullanmak komut enjeksiyonunu önler.

Sonuç olarak hızlı kurulum için ConvertX, PDF odaklı kullanım için Stirling PDF, yönetilen API için CloudConvert mantıklıdır. Öğrenmek ve tam kontrol kazanmak istiyorsanız FastAPI, Redis ve konteyner tabanlı worker’lardan oluşan özel çözüm en eğlenceli rotadır.
