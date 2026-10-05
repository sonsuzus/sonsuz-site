---
layout: post
title: "Açık Kaynak Anket Sistemleri: LimeSurvey, Formbricks ve Nextcloud Forms Karşılaştırması"
math: true
categories: 
  - Program
tags: 
  - anket
  - limesurvey
  - formbricks
  - nextcloud
  - açık kaynak
  - veri gizliliği
toc: true
image: /img/acik-kaynak-anket-60.png
---

Bir anket hazırlamak kolay görünür: Soruyu yaz, seçenekleri ekle ve bağlantıyı paylaş. Ancak koşullu sorular, anonim yanıtlar, ekip çalışması ve veri güvenliği devreye girdiğinde işler küçük çaplı bir yazılım mimarisi problemine dönüşür. Bu noktada LimeSurvey, Formbricks ve Nextcloud Forms farklı ihtiyaçlara hitap eden üç güçlü açık kaynak seçenektir.
``
## Üç farklı yaklaşım

Bu araçların hepsi yanıt toplasa da temel amaçları aynı değildir. **LimeSurvey**, ayrıntılı araştırmalar ve akademik çalışmalar için geliştirilmiş kapsamlı bir anket motorudur. **Formbricks**, ürün deneyimi ve kullanıcı geri bildirimi odaklı modern bir platformdur. **Nextcloud Forms** ise Nextcloud kullanan ekiplerin hızlı ve sade formlar oluşturmasını sağlar.

| Özellik | LimeSurvey | Formbricks | Nextcloud Forms |
|---|---|---|---|
| Temel kullanım | Araştırma ve kapsamlı anket | Ürün içi geri bildirim | Basit ekip formları |
| Koşullu mantık | Çok gelişmiş | Deneyim akışına uygun | Daha sınırlı |
| Kurulum zorluğu | Orta | Orta | Nextcloud varsa kolay |
| Raporlama | Ayrıntılı | Ürün ve deneyim odaklı | Temel |
| Özelleştirme | Yüksek | Yüksek | Orta |
| İdeal kullanıcı | Araştırmacı, kurum | SaaS ve ürün ekibi | Nextcloud ekibi |

![acik-kaynak-anket-60](/img/acik-kaynak-anket-60.svg)


## Anket mantığının teorik temeli

İyi bir anket yalnızca sorulardan oluşmaz; bir **yönlendirilmiş grafik** gibi düşünülebilir. Her soru bir düğüm, verilen cevaba göre açılan sonraki soru ise bir kenardır. Örneğin kullanıcı “Ürünü kullanmadım” dediyse kullanım memnuniyetini sormak anlamsızdır. LimeSurvey bu tür dallanmış akışlarda özellikle güçlüdür.

Puanlama yapılan bir ankette toplam sonuç, ağırlıklı ortalama ile hesaplanabilir:

$$
S = \frac{\sum_{i=1}^{n} w_i x_i}{\sum_{i=1}^{n} w_i}
$$

Burada $x_i$ cevabın sayısal değeri, $w_i$ ise sorunun önem ağırlığıdır. Kritik bir güvenlik sorusuna 5, görsel tercihle ilgili bir soruya 1 ağırlık vermek sonuçların daha anlamlı olmasını sağlar.

Formbricks özellikle NPS gibi ürün metriklerinde avantajlıdır. NPS hesabı şu şekildedir:

$$
NPS = \%\text{Destekçiler} - \%\text{Kötüleyenler}
$$

9–10 puan verenler destekçi, 0–6 verenler kötüleyen kabul edilir. 7–8 puan veren pasif kullanıcılar hesaplamanın iki tarafına da eklenmez.

## Hangi aracı seçmelisiniz?

Üniversite araştırması, çalışan memnuniyeti veya çok dilli kamu anketi hazırlıyorsanız **LimeSurvey** mantıklı seçimdir. Soru grupları, kota yönetimi, gelişmiş koşullar ve dışa aktarma seçenekleri karmaşık projeleri destekler. Buna karşılık yönetim ekranı yeni başlayanlara biraz yoğun gelebilir.

Web veya mobil ürününüzün belirli ekranlarında geri bildirim toplamak istiyorsanız **Formbricks** daha doğal bir deneyim sunar. Kullanıcının uygulamadan ayrılmadan ankete katılması, yanıtların ürün bağlamıyla ilişkilendirilmesini kolaylaştırır.

Dosya paylaşımı, takvim ve ekip hesapları zaten Nextcloud üzerindeyse **Nextcloud Forms** en az sürtünmeli çözümdür. Etkinlik kaydı, öğle yemeği tercihi veya toplantı oylaması için ayrı bir platform işletmek zorunda kalmazsınız.

## Basit bir puan hesaplama örneği

Aşağıdaki JavaScript fonksiyonu, dışa aktarılan sayısal cevapların ağırlıklı puanını hesaplar:

```javascript
function weightedScore(answers) {
  const totals = answers.reduce(
    (acc, item) => {
      acc.score += item.value * item.weight;
      acc.weight += item.weight;
      return acc;
    },
    { score: 0, weight: 0 }
  );

  return totals.weight === 0 ? 0 : totals.score / totals.weight;
}

const result = weightedScore([
  { value: 5, weight: 3 },
  { value: 4, weight: 2 },
  { value: 2, weight: 1 }
]);

console.log(result.toFixed(2));
```

Bu kod, her cevabı önem katsayısıyla çarpar ve normalize edilmiş sonuç üretir. Böylece farklı öneme sahip sorular tek bir değerlendirme puanında birleştirilebilir.

## Gizlilik ve operasyon

Kendi sunucunuzda barındırmak kontrol sağlar ama otomatik olarak güvenlik sağlamaz. HTTPS, düzenli yedekleme, güncelleme, yetki sınırlandırması ve veri saklama politikası gereklidir. Anonimlik vaat ediyorsanız IP adresi, zaman damgası ve kullanıcı hesabı gibi dolaylı tanımlayıcıları da değerlendirmelisiniz.

Kısacası derinlik için LimeSurvey, ürün geri bildirimi için Formbricks, Nextcloud içinde hızlı sadelik için Nextcloud Forms öne çıkar. En iyi araç, en çok özelliğe sahip olan değil; anket akışınıza, ekibinizin teknik kapasitesine ve gizlilik gereksinimlerinize en iyi uyan araçtır.
