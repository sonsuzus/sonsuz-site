---
layout: post
title: "Oyunlarda Erişilebilirlik Tasarımı: Her Oyuncuya Açık Bir Dünya"
math: true
categories: 
  - Bilgi
tags: 
  - oyun geliştirme
  - erişilebilirlik
  - renk körlüğü
  - işitme engeli
  - oyun tasarımı
  - kullanıcı deneyimi
toc: true
image: /img/oyunlarda-erisilebilirlik-tasarimi-80.png
---

![oyunlarda-erisilebilirlik-tasarimi-80](/img/oyunlarda-erisilebilirlik-tasarimi-80.svg)


Bir oyunun zorlu olması başka, bazı oyuncular için gereksiz yere oynanamaz olması başkadır. Küçük yazılar, yalnızca renkle aktarılan bilgiler veya altyazısız diyaloglar; geliştiricinin fark etmeden koyduğu engellere dönüşebilir. Erişilebilirlik tasarımı, oyunu basitleştirmek değil, oyuncuların bilgiye farklı yollarla ulaşmasını sağlayarak gerçek oyun deneyimine katılmalarını mümkün kılmaktır.
``
## Erişilebilirlik neden temel bir tasarım kararıdır?

Erişilebilirlik, geliştirme bittikten sonra ayarlar menüsüne eklenen birkaç kutucuktan ibaret değildir. Oyunun görsel dili, ses sistemi, kontrolleri ve geri bildirim mekanizmaları tasarlanırken ele alınmalıdır. Bunun temelinde **eşdeğer bilgi** ilkesi bulunur: Önemli bir bilgi yalnızca tek duyusal kanalla aktarılmamalıdır.

Örneğin yaklaşan bir düşman sadece ayak sesiyle haber veriliyorsa işitme engelli oyuncu dezavantaj yaşar. Aynı bilgi ekrandaki yön göstergesi, titreşim veya görsel efekt ile de sunulabilir. Benzer biçimde, takım üyelerini yalnızca kırmızı ve yeşil renkle ayırmak bazı renk körlüğü türlerinde sistemi kullanışsız hâle getirir.

| Sorun | Riskli tasarım | Erişilebilir alternatif |
|---|---|---|
| Renk körlüğü | Yalnızca kırmızı-yeşil ayrımı | Renk, simge ve desen birlikte kullanılır |
| İşitme engeli | Sadece sesli tehlike uyarısı | Altyazı, yön göstergesi ve titreşim eklenir |
| Görme güçlüğü | Küçük, sabit arayüz metni | Ölçeklenebilir yazı ve yüksek kontrast sunulur |
| Motor kısıtlılık | Hızlı ve karmaşık tuş kombinasyonları | Tuş atama ve basılı tutma seçenekleri sağlanır |

## Renk tek başına konuşmamalı

Renk körlüğü tek bir durum değildir. Deuteranopi yeşil, protanopi kırmızı, tritanopi ise mavi tonlarının algılanmasını etkileyebilir. Bu nedenle hazır bir “renk körü filtresi” her zaman yeterli olmaz. Bilgiyi renk dışında şekil, ikon, metin ve desenle desteklemek daha güvenlidir.

Metin ve arka plan okunabilirliğinde kontrast oranı önemli bir ölçüdür:

$$
C = \frac{L_{açık} + 0.05}{L_{koyu} + 0.05}
$$

Burada $L$, rengin göreli parlaklığıdır. $C$ yükseldikçe öğeleri ayırt etmek kolaylaşır. Ancak matematiksel olarak yeterli kontrast, hareketli ve karmaşık bir sahnede otomatik olarak iyi okunabilirlik anlamına gelmez. Tasarım gerçek oyun görüntüleri üzerinde test edilmelidir.

## Sesleri görünür hâle getirmek

Altyazı yalnızca konuşma metni değildir. Konuşmacının kimliği, sesin yönü ve önemli çevresel sesler de aktarılabilir:

- **[Sol taraftan metal sürtünmesi]**
- **Komutan:** Kapıyı kapat!
- **[Müzik hızlanır]**

Oyuncuya yazı boyutu, arka plan opaklığı ve konuşmacı rengi seçenekleri vermek altyazıları çok daha kullanışlı yapar. Rekabetçi oyunlarda görsel ses göstergeleri dikkatle dengelenmeli; erişilebilirlik seçeneği, sesi kullanan oyunculardan daha fazla taktik bilgi vermemelidir.

## Ayarları veri odaklı tasarlamak

Aşağıdaki Unity C# örneği, altyazı tercihlerini tek bir yapı içinde tutar ve arayüzün bu ayarlara göre güncellenmesini sağlar:

```csharp
using UnityEngine;

[System.Serializable]
public class AccessibilitySettings
{
    public bool subtitlesEnabled = true;
    [Range(18, 48)] public int subtitleSize = 28;
    [Range(0f, 1f)] public float backgroundOpacity = 0.75f;
    public bool showSoundDirection = true;
}

public class AccessibilityManager : MonoBehaviour
{
    public AccessibilitySettings settings;
    public SubtitleView subtitleView;

    public void ApplySettings()
    {
        subtitleView.gameObject.SetActive(settings.subtitlesEnabled);
        subtitleView.SetFontSize(settings.subtitleSize);
        subtitleView.SetBackgroundOpacity(settings.backgroundOpacity);
        subtitleView.ShowDirection(settings.showSoundDirection);
    }
}
```

Bu yaklaşım, değerleri oyun koduna gömmek yerine merkezi ve kaydedilebilir hâle getirir. Aynı model renk paletleri, titreşim yoğunluğu ve kontrol şemaları için genişletilebilir.

## Son kontrol: Oyuncuyla test

Simülasyon araçları yararlıdır fakat gerçek kullanıcı testlerinin yerini tutmaz. Farklı ihtiyaçlara sahip oyuncular geliştirme sürecine erken katılmalı, ayarlar ilk açılışta bulunabilir olmalı ve seçeneklerin etkisi anında önizlenebilmelidir. Sonuçta erişilebilir tasarım yalnızca belirli gruplara yardım etmez; gürültülü ortamda altyazı kullanan, küçük ekranda oynayan veya geçici sakatlık yaşayan herkese daha esnek bir deneyim sunar. İyi erişilebilirlik görünmez bir yardımcı gibidir: İhtiyaç duyulduğunda oradadır ve oyuncuyla oyun arasındaki gereksiz duvarları kaldırır.
