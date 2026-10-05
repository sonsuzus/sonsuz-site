---
layout: post
title: "Online Deneme Sınavı Sistemi Seçimi: Moodle mı, ClassMarker mı?"
math: true
categories: 
  - Bilgi
tags: 
  - moodle
  - classmarker
  - online-sınav
  - e-öğrenme
  - ölçme-değerlendirme
  - lms
toc: true
image: /img/online-deneme-sinavi-59.png
---

Online deneme sınavı hazırlamak, soruları bir forma yerleştirip “Gönder” düğmesine basmaktan ibaret değildir. İyi bir sistem; soru havuzu, rastgeleleştirme, süre yönetimi, otomatik değerlendirme, güvenlik ve ayrıntılı raporlama gibi parçaları birlikte çalıştırır. Bu noktada açık kaynaklı bir öğrenme yönetim sistemi olan Moodle ile sınav odaklı bulut hizmeti ClassMarker öne çıkar.

``

## Önce sistemin mantığını anlayalım

Bir deneme sınavının temel veri modeli kullanıcı, sınav, soru, seçenek, cevap ve sonuç varlıklarından oluşur. Öğrenci sınava başladığında sistem soru havuzundan belirlenen kurallara göre bir sınav oturumu üretir. Örneğin 100 soruluk havuzdan rastgele 20 soru seçilmesi kombinatoryal olarak

$$
\binom{100}{20} = \frac{100!}{20!\,80!}
$$

farklı soru kümesi oluşturabilir. Seçeneklerin sırası da karıştırıldığında öğrencilerin tamamen aynı sınavla karşılaşma ihtimali ciddi ölçüde azalır.

Puanlama ise basit bir ağırlıklı toplamla modellenebilir:

$$
P = \sum_{i=1}^{n} w_i c_i - \sum_{i=1}^{n} q_i h_i
$$

Burada $w_i$ doğru cevabın puanını, $c_i$ doğruluk durumunu, $q_i$ yanlış cevap cezasını ve $h_i$ yanlışlık durumunu gösterir. Moodle farklı soru davranışları ve esnek notlandırma konusunda oldukça ayrıntılıdır. ClassMarker ise benzer ihtiyaçları daha sade bir yönetim paneliyle çözmeyi hedefler.

## Moodle ve ClassMarker karşılaştırması

| Özellik | Moodle | ClassMarker |
|---|---|---|
| Kurulum | Sunucuya kurulabilir veya hizmet olarak alınabilir | Bulut tabanlı, kurulum gerektirmez |
| Özelleştirme | Eklentiler ve tema sistemiyle çok yüksek | Hazır seçeneklerle sınırlı |
| Soru havuzu | Kategori, etiket ve ayrıntılı rastgele seçim | Kolay yönetilen soru bankası |
| Raporlama | Geniş, ancak öğrenmesi zaman alabilir | Sade ve hızlı sonuç ekranları |
| Entegrasyon | API, LTI ve çok sayıda eklenti | API ve bağlantı seçenekleri |
| Bakım | Kurumu veya yöneticiyi ilgilendirir | Hizmet sağlayıcı tarafından yapılır |
| Kullanım amacı | Ders, içerik ve sınavların tamamı | Hızlı biçimde çevrim içi sınav yapmak |

![online-deneme-sinavi-59](/img/online-deneme-sinavi-59.svg)


## Moodle ne zaman mantıklı?

Ders materyalleri, ödevler, forumlar, canlı ders bağlantıları ve deneme sınavları tek merkezde yönetilecekse Moodle güçlü bir tercihtir. Matematik, kısa cevap, eşleştirme ve gömülü cevap gibi birçok soru türünü destekler. Ayrıca öğrencinin her denemesinde farklı sorular görebilmesi için kategori tabanlı rastgele soru seçimi yapılabilir.

Bunun bedeli teknik sorumluluktur. Güncelleme, yedekleme, performans, e-posta ayarları ve güvenlik düzenli olarak takip edilmelidir. Yüzlerce öğrencinin aynı anda sınava girmesi bekleniyorsa sunucu kapasitesi yük testiyle doğrulanmalıdır.

## ClassMarker ne zaman avantajlı?

“Sunucu yönetmeyeyim, sınavımı bugün yayımlayayım” diyorsanız ClassMarker daha pratik olabilir. Sınav bağlantıları, erişim kodları, zaman sınırları, sertifikalar ve otomatik sonuçlandırma hızlı biçimde ayarlanabilir. Özellikle şirket içi eğitimler, işe alım testleri ve bağımsız eğitmenler için öğrenme eğrisi düşüktür.

Buna karşılık platformun sunduğu tasarım ve iş akışlarıyla sınırlı kalırsınız. Çok özel bir soru tipi veya kuruma özgü rapor gerekiyorsa Moodle’ın eklenti mimarisi daha fazla hareket alanı sağlar.

## Basit bir puan hesaplama örneği

Aşağıdaki Python fonksiyonu doğru cevaplara 5 puan verirken yanlışlardan 1,25 puan düşürür. Boş cevaplar puanı değiştirmez:

```python
def puan_hesapla(cevaplar, anahtar):
    puan = 0

    for cevap, dogru in zip(cevaplar, anahtar):
        if cevap is None:
            continue
        if cevap == dogru:
            puan += 5
        else:
            puan -= 1.25

    return max(0, puan)
```

Gerçek bir sistemde bu işlem sunucu tarafında yapılmalı; cevap anahtarı tarayıcıya gönderilmemelidir. Ayrıca sınav başlangıç ve bitiş zamanları sunucu saatiyle denetlenmeli, her işlem kayda alınmalı ve kişisel veriler gereğinden uzun tutulmamalıdır.

## Kısa karar reçetesi

Tam kapsamlı bir eğitim portalı, yüksek özelleştirme ve veri kontrolü istiyorsanız Moodle seçin. Teknik bakım olmadan hızlı, anlaşılır ve sınav merkezli bir çözüm arıyorsanız ClassMarker kullanın. En iyi platform en fazla özelliğe sahip olan değil; sınav güvenliği, bütçe, teknik ekip ve öğrenci deneyimi arasında doğru dengeyi kurandır.
