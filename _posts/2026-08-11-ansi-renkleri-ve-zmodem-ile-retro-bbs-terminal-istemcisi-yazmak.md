---
layout: post
title: "ANSI Renkleri ve ZMODEM ile Retro BBS Terminal İstemcisi Yazmak"
math: true
categories: 
  - Proje
tags: 
  - bbs
  - ansı art
  - zmodem
  - terminal
  - python
image: /img/ansi-renkleri-ve-13.png
---

![ansi-renkleri-ve-13](/img/ansi-renkleri-ve-13.svg)


İnternetin modem sesleriyle bağlandığı günlere küçük bir selam vermek istiyorsanız, konsol tabanlı bir BBS terminal istemcisi harika bir projedir. Hedefimiz; seri port veya TCP üzerinden bir BBS’e bağlanmak, ANSI kaçış dizileriyle çizilen renkli ekranları doğru göstermek ve ZMODEM sayesinde dosya indirip gönderebilmektir. Bu proje yalnızca nostaljik değildir: akış kontrolü, terminal emülasyonu, ikili protokoller ve olay tabanlı G/Ç gibi bugün de değerli olan kavramları aynı potada buluşturur.

``

Bir terminal istemcisi temelde iki yönlü bir veri köprüsüdür. Klavyeden gelen karakterleri uzak sisteme iletir; uzak sistemden gelen baytları ise ekranda yorumlar. Ancak terminal ekranı düz metinden fazlasıdır. ANSI standardı, `ESC` karakteriyle başlayan kontrol dizileri kullanır. Örneğin `\x1b[31m` yazı rengini kırmızıya alırken `\x1b[2J` ekranı temizler. Buradaki temel fikir, görünür metin ile ekranı değiştiren komutların aynı bayt akışında bulunmasıdır.

| Bileşen | Görevi | Kritik ayrıntı |
|---|---|---|
| Taşıma katmanı | TCP veya seri port bağlantısı | Baytların sırası korunmalıdır |
| Terminal emülatörü | ANSI komutlarını yorumlar | İmleç ve renk durumunu tutar |
| Girdi yöneticisi | Tuşları uzak uca yollar | Özel tuşlar kaçış dizisine dönüşür |
| ZMODEM motoru | Dosya transferini yürütür | Terminal verisinden protokolü ayırır |

ANSI işleme için ilk sürümde her standardı desteklemeye çalışmayın. SGR renk kodları, imleç hareketi, satır silme ve ekran temizleme çoğu BBS için güçlü bir başlangıçtır. Terminalin durumu bir sonlu durum makinesi gibi düşünülebilir. Normal metin modunda karakter ekrana basılır; `ESC` görülünce ayrıştırıcı kontrol dizisi moduna geçer. Genel maliyet yaklaşık olarak $O(n)$’dir; çünkü gelen $n$ baytın her biri ideal olarak bir kez işlenir.

Python tarafında `asyncio`, ağdan veri okurken klavyenin donmaması için pratik bir omurga sağlar. Aşağıdaki iskelet, TCP bağlantısından gelen ham veriyi terminal ayrıştırıcısına aktarır:

```python
import asyncio

async def bbs_oturumu(host, port):
    reader, writer = await asyncio.open_connection(host, port)
    print(f"{host}:{port} bağlantısı kuruldu")

    while True:
        veri = await reader.read(1024)
        if not veri:
            break
        # Gerçek projede burada ANSI ayrıştırıcısı çağrılır.
        metin = veri.decode("cp437", errors="replace")
        print(metin, end="", flush=True)

    writer.close()
    await writer.wait_closed()

asyncio.run(bbs_oturumu("bbs.ornek.net", 23))
```

Kodda `cp437` seçimi tesadüf değildir. Eski DOS/BBS dünyasında kutu çizim karakterleri ve ikonik ANSI art eserleri sıklıkla IBM Code Page 437 kullanır. UTF-8 ile doğrudan çözmek, çerçeveleri anlamsız sembollere dönüştürebilir. Yine de sunucunun karakter setini yapılandırılabilir yapmak en sağlıklı yaklaşımdır.

ZMODEM işin daha heyecanlı, fakat daha hassas bölümüdür. Protokol; paket numaraları, CRC kontrolleri, yeniden deneme ve bağlantı kopunca devam edebilme özellikleri sağlar. Bir paketin güvenilirliği kabaca şu fikre dayanır: alıcı, hesapladığı denetim değerini göndereninkiyle karşılaştırır. Uyuşmazlık olasılığı kullanılan CRC genişliği arttıkça azalır; ideal modelde yaklaşık $P \approx 2^{-k}$ olarak düşünülebilir. Burada $k$, CRC bit sayısıdır.

| Özellik | Basit metin aktarımı | ZMODEM |
|---|---|---|
| Hata denetimi | Genellikle yok | CRC ile doğrulama |
| Kaldığı yerden sürdürme | Yok | Desteklenir |
| Etkileşim | Manuel | Otomatik anlaşma |
| İkili dosya güvenliği | Riskli | Yüksek |

Pratikte ZMODEM’i sıfırdan yazmak yerine olgun bir araç veya kütüphaneyle entegre edin. Terminal akışında `rz`/`sz` anlaşma imzaları algılandığında normal ANSI ayrıştırmasını geçici olarak durdurup baytları ZMODEM motoruna yönlendirin. Transfer bittiğinde terminal moduna geri dönün. En önemli kural şudur: Dosya aktarımı sırasında hiçbir katman gelen baytları metne dönüştürmemeli, değiştirmemeli veya ekrana “yardımcı olmak” adına ek karakter basmamalıdır.

Son dokunuş olarak bağlantı profilleri, otomatik giriş betikleri, kayıt dosyası ve 80x25 ekran boyutu ekleyin. Böylece yalnızca çalışan bir istemci değil, yeşil fosfor ekran hissini modern bilgisayara taşıyan küçük bir zaman makinesi üretmiş olursunuz.
