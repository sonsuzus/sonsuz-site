---
layout: post
title: "Açık Kaynak Çeviri Üçlüsü: LibreTranslate, Argos Translate ve Apertium"
math: true
categories: 
  - Bilgi
tags: 
  - çeviri
  - libretranslate
  - argos-translate
  - apertium
  - doğal-dil-işleme
  - açık-kaynak
toc: true
image: /img/acik-kaynak-ceviri-19.png
---

![acik-kaynak-ceviri-19](/img/acik-kaynak-ceviri-19.svg)


Bir metni başka bir dile çevirmek kolay görünür: kelimeyi bul, karşılığını yaz, kahveni yudumla! Gerçekteyse dil; bağlam, sözcük sırası, çekim ve kültürel ifadelerle dolu karmaşık bir sistemdir. Açık kaynak dünyasında LibreTranslate, Argos Translate ve Apertium bu probleme farklı katmanlardan yaklaşır. Biri kullanışlı bir web API’si sunarken diğeri çevrimdışı sinir ağı modellerine, ötekiyse dilbilgisi kurallarına güvenir.

``

## Makine çevirisinin temel mantığı

Makine çevirisi sistemleri genel olarak **kural tabanlı**, **istatistiksel** veya **sinir ağı tabanlı** çalışır. Kural tabanlı yöntemde kaynak cümle sözcük ve biçimbirimlerine ayrılır; ardından sözlükler ile dilbilgisi kuralları uygulanır. Sinir ağı tabanlı yöntemdeyse model, bütün cümlenin bağlamını sayısal vektörlerle temsil ederek hedef cümleyi üretir.

Bir sinir ağı modelinde en olası çeviri basitleştirilmiş biçimde şöyle aranır:

$$
\hat{Y} = \arg\max_Y P(Y \mid X)
$$

Burada $X$ kaynak cümleyi, $Y$ olası hedef cümleyi ve $\hat{Y}$ modelin seçtiği çeviriyi ifade eder. Model yalnızca kelime karşılıklarını değil, hedef dilde doğal görünme olasılığını da hesaba katar.

## Üç araç arasındaki farklar

| Araç | Temel yaklaşım | Çevrimdışı kullanım | Güçlü yanı | Uygun senaryo |
|---|---|---:|---|---|
| LibreTranslate | Argos tabanlı sinirsel çeviri ve HTTP API | Evet | Web servislerine kolay entegrasyon | Uygulama ve mikroservisler |
| Argos Translate | OpenNMT tabanlı sinirsel modeller | Evet | Yerel ve gizlilik odaklı çalışma | Masaüstü araçları, otomasyon |
| Apertium | Kural tabanlı makine çevirisi | Evet | Dil yapısının denetlenebilmesi | Özellikle yakın akraba diller |

### LibreTranslate

LibreTranslate, kendi sunucunuza kurabileceğiniz açık kaynaklı bir çeviri API’sidir. Tarayıcı arayüzü bulunsa da asıl yıldızı REST API desteğidir. Verilerin üçüncü taraf bir servise gönderilmemesi; şirket içi belgeler, kişisel notlar ve eğitim projeleri için önemli bir avantajdır.

Aşağıdaki Python kodu, çalışan bir LibreTranslate sunucusuna istek gönderir:

```python
import requests

payload = {
    "q": "Açık kaynak yazılımlar özgürlük sağlar.",
    "source": "tr",
    "target": "en",
    "format": "text"
}

response = requests.post(
    "http://localhost:5000/translate",
    json=payload,
    timeout=30
)

response.raise_for_status()
print(response.json()["translatedText"])
```

Kod, kaynak metni ve dil kodlarını JSON olarak API’ye yollar; dönen sonuçtan çevrilmiş metni çıkarır. Üretim ortamında zaman aşımı, kimlik doğrulama ve hata yönetimi ayrıca planlanmalıdır.

### Argos Translate

Argos Translate, indirilebilir dil paketleriyle tamamen yerel çalışabilir. İnternet bağlantısı olmadan çeviri yapması hem gizlilik hem de taşınabilirlik sağlar. Ancak bir dil çiftinin desteklenmesi için uygun model paketinin kurulması gerekir. Ayrıca doğrudan bir model yoksa Türkçeden belirli bir dile çeviri, İngilizce gibi ara bir dil üzerinden gerçekleştirilebilir. Bu zincirleme yaklaşım erişimi artırırken hataları da biriktirebilir.

### Apertium

Apertium’un dünyası biraz daha “dilbilim laboratuvarı” gibidir. Sistem sözlükler, biçimbirimsel çözümleyiciler ve aktarım kuralları kullanır. Özellikle İspanyolca–Katalanca gibi yapısal olarak yakın dillerde güçlü sonuçlar verebilir. Kurallar incelenebilir ve düzeltilebilir; buna karşılık yeni bir dil çifti hazırlamak ciddi dilbilim emeği ister.

## Kaliteyi nasıl değerlendirmeli?

Çeviri kalitesi yalnızca “doğru görünüyor” hissiyle ölçülmez. BLEU gibi metrikler, üretilen çevirideki sözcük dizilerini referans çevirilerle karşılaştırır. Yine de yüksek puan her zaman doğal veya anlamca kusursuz sonuç demek değildir. Deyimler, teknik terimler ve alan bilgisi için insan değerlendirmesi gereklidir.

Hızlı bir API ve kolay entegrasyon istiyorsanız **LibreTranslate**, gömülü ya da çevrimdışı bir çözüm arıyorsanız **Argos Translate**, kuralları denetlemek ve yakın diller üzerinde çalışmak istiyorsanız **Apertium** mantıklı seçimdir. Kısacası en iyi araç mutlak değildir; dil çiftine, donanıma, gizlilik beklentisine ve “bu cümle neden böyle çevrildi?” sorusuna ne kadar ayrıntılı cevap istediğinize bağlıdır.
