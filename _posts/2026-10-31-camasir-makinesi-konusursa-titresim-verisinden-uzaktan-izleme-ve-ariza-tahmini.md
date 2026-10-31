---
layout: post
title: "Çamaşır Makinesi Konuşursa: Titreşim Verisinden Uzaktan İzleme ve Arıza Tahmini"
math: true
categories: 
  - Bilgi
tags: 
  - iot
  - kestirimci bakım
  - titreşim analizi
  - python
  - akıllı beyaz eşya
  - uzaktan izleme
toc: true
image: /img/camasir-makinesi-konusursa-94.png
---

Çamaşır makineniz sıkma sırasında banyoda yürüyüşe çıkıyorsa, size bir şey anlatmaya çalışıyor olabilir. Akıllı beyaz eşyalarda titreşim sensörleri bu mekanik dili sayılara çevirir. Amaç yalnızca “makine sallanıyor” demek değil; normal davranıştan sapmayı yakalayarak bakım ihtiyacını, ciddi bir arıza oluşmadan önce görünür kılmaktır.

``

## Titreşim neden değerli bir ipucudur?

Dönen tambur, motor, rulmanlar ve amortisörler farklı titreşim bileşenleri üretir. Dengesiz yük, dönme frekansı çevresindeki hareketi artırabilir; rulman hasarı ise darbe benzeri bileşenler oluşturabilir. Ancak aynı belirti birden fazla nedenden kaynaklanır. Sensörümüz dedektiftir, kahin değil!

Dakikada 1200 devir yapan tamburun dönme frekansı $1200/60=20\,\text{Hz}$ olur. Frekans analizi, titreşim enerjisinin hangi bölgelerde yoğunlaştığını gösterir. Bu bilgi, toplam titreşim seviyesinden daha açıklayıcı olabilir.

| Gözlenen değişim | Olası açıklama | Kontrol edilmesi gereken |
|---|---|---|
| Dönme frekansında artış | Yük dengesizliği | Çamaşır dağılımı |
| Darbe benzeri sinyaller | Rulman veya mekanik temas | Tekrarlama ve çalışma koşulları |
| Genel titreşim artışı | Süspansiyon veya kurulum sorunu | Zemin ve ayak dengesi |

Bunlar kesin teşhis değildir. Aynı makine, aynı hızda bile farklı yüklerle farklı davranabilir.

## Önce doğru veriyi toplayalım

Bir ivmeölçer, üretici önerilerine uygun ve güvenli bir gövde noktasına sabitlenebilir. Sensörün konumu ve montajı değişirse referans da değişir. Elektrik veya hareketli parçalar çevresindeki müdahaleler uzmanlık gerektirir.

Örnekleme hızı, ilgilenilen en yüksek frekansın iki katından büyük olmalıdır: $f_s>2f_{\max}$. Pratikte uygun kenar payı ve örnekleme öncesi anti-aliasing filtresi gerekir. Örneğin 2 kHz örnekleme, aşağıdaki örnekte kullanılan 300–800 Hz bandını incelemeye uygundur; bu bant her makine için evrensel değildir.

İki saniyelik pencerelerde üç özellik çıkaralım: RMS, basıklık ve bant enerjisi oranı. RMS genel titreşim seviyesini özetler:

$$a_{RMS}=\sqrt{\frac{1}{N}\sum_{i=1}^{N}a_i^2}$$

Basıklık, darbe karakterine duyarlıdır. Bant enerjisi oranı ise seçilen frekans bölgesinin toplam güç içindeki payını gösterir. Öncesinde sinyal ortalamasını çıkararak sabit bileşeni azaltırız.

## Python ile küçük bir erken uyarı motoru

Aşağıdaki kod, tek eksenli ivme penceresinden özellik çıkarır. Sağlıklı çalışma pencerelerinden hazırlanmış `referans` matrisiyle karşılaştırarak bir anomali puanı üretir. Her referans satırı aynı üç özelliği içermelidir.

```python
import numpy as np
from scipy.signal import welch
from scipy.stats import kurtosis


def ozellikler(ivme, fs=2000):
    a = np.asarray(ivme, dtype=float)
    a = a - a.mean()
    f, p = welch(a, fs=fs, nperseg=min(len(a), 1024))
    bant = (f >= 300) & (f <= 800)
    return np.array([
        np.sqrt(np.mean(a ** 2)),
        kurtosis(a, fisher=False),
        p[bant].sum() / (p.sum() + 1e-12)
    ])


def alarm_puani(ivme, referans, fs=2000):
    ref = np.asarray(referans, dtype=float)
    medyan = np.median(ref, axis=0)
    mad = np.median(np.abs(ref - medyan), axis=0)
    z = (ozellikler(ivme, fs) - medyan) / (1.4826 * mad + 1e-6)
    return float(np.maximum(z, 0).max())
```

Medyan ve MAD, uç değerlerin referansı bozmasını azaltır. Puan yalnızca referansın üzerindeki sapmaları toplar; arıza olasılığı değildir. Sabit veya geçersiz sensör verileri ayrıca filtrelenmeli, çok küçük MAD değerleri için özellik bazında ölçek tabanları belirlenmelidir.

## Veriyi değil, anlamını gönderelim

Sensör verisi önce yerel işlemcide özetlenebilir. Özellikler, tambur hızı, program aşaması ve zaman damgasıyla MQTT üzerinden TLS kullanılarak sunucuya iletilir. Cihaz kimlik doğrulaması ve erişim yetkileri de şarttır.

| Yaklaşım | Avantaj | Bedel |
|---|---|---|
| Ham veriyi buluta gönderme | Ayrıntılı sonradan analiz | Yüksek trafik ve depolama |
| Yerelde özellik çıkarma | Düşük trafik, hızlı tepki | Bazı ayrıntıların kaybı |

Bağlantı kesilirse yerel tampon kullanılabilir. Böylece internetin molası, izleme sisteminin hafızasını silmez.

## Alarmdan gerçek tahmine geçiş

Referansları program, yük ve hız koşullarına göre ayırmak gerekir. Tek bir yüksek puan yerine birkaç karşılaştırılabilir pencerede kalıcı artış aranmalıdır. Eşikler gerçek saha verisiyle ayarlanır; yanlış alarm oranı ve bakım öncesi uyarı süresi birlikte ölçülür.

Gerçek kestirimci bakım için zaman içindeki eğilimler, servis kayıtları ve doğrulanmış arıza etiketleri gerekir. Bakım sonrası titreşimin normale dönmesi de değerli geri bildirimdir. Yalnızca titreşimden “rulman üç gün sonra bozulacak” demek güvenilir değildir. Başarılı sistem, gerektiğinde “alışılmadık bir değişim var, kontrol ettirelim” diyendir. Banyonun yeni dansçısını erken fark etmek bile iyi bir başlangıçtır!

![camasir-makinesi-konusursa-94](/img/camasir-makinesi-konusursa-94.svg)

