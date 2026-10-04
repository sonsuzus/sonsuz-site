---
layout: post
title: "Geleceğin Yazılımcısı: Kod Ustası mı, Yapay Zekâ Orkestra Şefi mi?"
math: true
categories: 
  - Bilgi
tags: 
  - yapay zeka
  - yazılım geliştirme
  - ai ajanları
  - prompt mühendisliği
  - sistem entegrasyonu
  - geleceğin meslekleri
toc: true
image: /img/gelecegin-yazilimcisi-kod-28.png
---

Yazılımcılık uzun süre doğru sözdizimini bilmek, algoritma kurmak ve hatasız kod yazmakla özdeşleştirildi. Ancak üretken yapay zekâ ve otonom ajanlar sahneye çıktıkça klavyenin başındaki kahramanın görevi değişiyor. Geleceğin yazılımcısı her enstrümanı tek başına çalan kişi değil; hangi ajanın ne zaman devreye gireceğini belirleyen, sonuçları denetleyen ve bütün sistemi uyum içinde çalıştıran bir orkestra şefi olabilir.
``
## Kod üretmekten niyet tanımlamaya

Geleneksel programlamada geliştirici, bilgisayara çözümün adımlarını açıkça anlatır. Ajan tabanlı yaklaşımda ise hedefi, sınırları ve başarı ölçütlerini tanımlar. Yapay zekâ bu hedefe ulaşmak için plan oluşturabilir, araç çağırabilir, kod yazabilir ve sonuçları değerlendirebilir.

Bu değişimi basit bir soyutlamayla ifade edebiliriz. Klasik modelde çıktı yaklaşık olarak şöyledir:

$$Çıktı = Program(Kod, Veri)$$

Ajan tabanlı sistemdeyse denklem genişler:

$$Çıktı = Ajan(Hedef, Bağlam, Araçlar, Geri\ Bildirim)$$

Burada geliştiricinin değeri yalnızca `Kod` üretmesinden değil; bağlamı düzenlemesinden, doğru araçları seçmesinden ve geri bildirim döngüsünü güvenilir hâle getirmesinden doğar.

| Geleneksel geliştirici | Ajan orkestra şefi |
|---|---|
| Fonksiyonları elle yazar | Görevleri ajanlara böler |
| Sözdizimi hatalarını düzeltir | Belirsiz hedefleri netleştirir |
| Tek uygulamaya odaklanır | Birden fazla servis ve modeli bağlar |
| Test senaryosu üretir | Otomatik değerlendirme döngüsü kurar |
| Kodu çalıştırır | Yetki, maliyet ve risk sınırlarını yönetir |

## Prompt mühendisliği tek başına yeterli mi?

Prompt yazmak önemli olsa da geleceğin işi yalnızca etkileyici cümleler kurmak değildir. İyi bir sistem; rol, bağlam, veri şeması, araç izinleri ve hata durumlarıyla birlikte tasarlanır. Başka bir deyişle prompt, sistem mimarisinin yalnızca bir bileşenidir.

Örneğin müşteri taleplerini yöneten basitleştirilmiş bir Python akışı şöyle kurulabilir:

```python
def handle_request(message, classifier, support_agent, billing_agent):
    category = classifier.run(message)

    agents = {
        "support": support_agent,
        "billing": billing_agent,
    }

    selected_agent = agents.get(category)
    if selected_agent is None:
        return {"status": "manual_review", "message": message}

    result = selected_agent.run(message)
    return {"status": "completed", "result": result}
```

Bu kodun ilginç tarafı algoritmik karmaşıklığı değil, sorumlulukları ayırmasıdır. Sınıflandırıcı yönlendirme yapar, uzman ajan görevi tamamlar, tanınmayan durumlar ise insana aktarılır. Gerçek sistemde bunlara erişim kontrolü, kayıt tutma, zaman aşımı ve çıktı doğrulama katmanları da eklenir.

## Yeni temel beceriler

Geleceğin geliştiricisi API tasarımı, olay tabanlı mimari, veri akışları ve gözlemlenebilirlik konularında daha güçlü olmalıdır. Çünkü beş ajanın ürettiği yüzlerce adımı izleyemiyorsanız sistemin çalışması, güvenilir olduğu anlamına gelmez.

Başarıyı yalnızca doğrulukla ölçmek de eksiktir. Pratik bir kalite fonksiyonu şöyle düşünülebilir:

$$Q = \alpha D - \beta M - \gamma R$$

Burada $D$ doğruluk, $M$ maliyet ve $R$ risk değeridir. Katsayılar ürünün önceliklerini temsil eder. Sağlık uygulamasında risk katsayısı büyürken, basit bir içerik aracında hız ve maliyet öne çıkabilir.

## Kod yazmak bitecek mi?

Hayır; fakat kodun rolü değişecek. Geliştirici daha az standart kod yazıp daha çok üretilen kodu inceleyecek, kritik bileşenleri tasarlayacak ve ajanların hareket alanını sınırlayacak. Temel programlama bilgisi de önemini kaybetmeyecek; aksine yapay zekânın ikna edici fakat hatalı çıktısını fark etmek için daha gerekli olacak.

Sonuçta geleceğin yazılımcısı, kod yazmayı bırakan biri değil; kodu, modelleri, servisleri ve insan kararlarını tek bir güvenilir sistemde buluşturan kişidir. Klavye hâlâ masada duracak, ancak en değerli araç artık yalnızca parmaklar değil; mimari düşünme, eleştirel denetim ve iyi yönetilmiş bir ajan orkestrası olacaktır.

![gelecegin-yazilimcisi-kod-28](/img/gelecegin-yazilimcisi-kod-28.svg)

