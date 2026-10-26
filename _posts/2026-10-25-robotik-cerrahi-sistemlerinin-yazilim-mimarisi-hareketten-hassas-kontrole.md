---
layout: post
title: "Robotik Cerrahi Sistemlerinin Yazılım Mimarisi: Hareketten Hassas Kontrole"
math: true
categories: 
  - Bilgi
tags: 
  - robotik cerrahi
  - gömülü sistemler
  - gerçek zamanlı yazılım
  - robotik
  - kontrol teorisi
  - yazılım mimarisi
toc: true
image: /img/robotik-cerrahi-sistemlerinin-13.png
---

Bir cerrahın konsoldaki kumandayı birkaç milimetre oynatmasıyla robot kolunun hastanın içinde son derece hassas biçimde hareket etmesi neredeyse bilim kurgu gibi görünür. Oysa perde arkasında sensörler, gerçek zamanlı işletim sistemleri, kontrol algoritmaları ve güvenlik katmanları birlikte çalışır. Bu zincirin en kritik hedefi yalnızca hızlı olmak değil; öngörülebilir, kararlı ve hataya dayanıklı biçimde milisaniyeler içinde tepki vermektir.

![robotik-cerrahi-sistemlerinin-13](/img/robotik-cerrahi-sistemlerinin-13.svg)

``

## Hareket komutu nasıl yolculuk eder?

Cerrahın kullandığı ana kontrol birimindeki konum, açı ve kuvvet sensörleri saniyede yüzlerce, hatta binlerce ölçüm üretir. Ham ölçümler doğrudan robot koluna gönderilmez. Sensör gürültüsü filtrelenir, el titremesi bastırılır ve hareket cerrahi ölçeğe dönüştürülür.

Tipik veri hattı şöyledir:

1. **Örnekleme:** Kumandaların konumu ve yönelimi okunur.
2. **Filtreleme:** İstenmeyen titreşimler ve ölçüm gürültüsü azaltılır.
3. **Ölçekleme:** Büyük el hareketi, küçük alet hareketine çevrilir.
4. **Kinematik çözüm:** Robot eklemlerinin hedef açıları hesaplanır.
5. **Motor kontrolü:** Her eklem için tork veya hız komutu üretilir.
6. **Geri besleme:** Enkoderler gerçek hareketi ölçerek döngüyü kapatır.

Örneğin cerrahın hareketi $\Delta x_h$, cerrahi aletin hareketi ise $\Delta x_r$ olsun. Ölçekleme ilişkisi basitçe

$$\Delta x_r = s \cdot \Delta x_h$$

şeklinde ifade edilebilir. $s=0.2$ seçildiğinde, eldeki 10 milimetrelik hareket robot ucunda 2 milimetreye dönüşür.

## Katmanlı yazılım mimarisi

| Katman | Görevi | Tipik zaman ölçeği |
|---|---|---:|
| Kullanıcı arayüzü | Görüntü, ayarlar ve uyarılar | 10–100 ms |
| Hareket işleme | Filtreleme ve ölçekleme | 1–5 ms |
| Kinematik planlama | Eklem hedeflerini hesaplama | 1–10 ms |
| Servo kontrol | Motorları geri beslemeyle yönetme | 0.1–1 ms |
| Güvenlik sistemi | Sınır ve hata denetimi | Sürekli |

Bu görevlerin hepsi aynı öncelikte değildir. Grafik arayüzündeki küçük bir gecikme tolere edilebilirken motor kontrol döngüsünün zamanında çalışmaması risklidir. Bu nedenle kritik bileşenlerde gerçek zamanlı işletim sistemleri kullanılır. Buradaki “gerçek zamanlı” ifadesi yalnızca hızlı çalışmayı değil, işlemin belirlenmiş süre sınırı içinde tamamlanmasını anlatır.

Toplam gecikme yaklaşık olarak

$$T_{toplam}=T_{sensör}+T_{işleme}+T_{iletişim}+T_{motor}$$

biçiminde modellenebilir. Ortalama değerin düşük olması kadar gecikmedeki değişim, yani **jitter**, de önemlidir. Robotun bazen 2, bazen 30 milisaniyede tepki vermesi cerrahın hareket algısını bozabilir.

## Kontrol döngüsünün kalbi

Basitleştirilmiş bir servo denetleyici aşağıdaki gibi düşünülebilir:

```python
def kontrol_adimi(hedef, gercek, onceki_hata, dt):
    hata = hedef - gercek
    turev = (hata - onceki_hata) / dt
    komut = KP * hata + KD * turev
    komut = sinirla(komut, -MAKS_TORK, MAKS_TORK)
    return komut, hata
```

Bu örnek, hedef açı ile enkoderden okunan gerçek açı arasındaki hatayı kullanarak motor torku üretir. Oransal terim hatayı kapatmaya çalışırken türev terimi ani değişimleri sönümler. Gerçek sistemlerde sürtünme telafisi, yerçekimi modeli ve gelişmiş durum kestiricileri de bulunabilir.

## Güvenlik neden ayrı bir mimaridir?

Robotik cerrahide tek bir algoritmaya güvenilmez. Eklem sınırları, hız, tork, iletişim bütünlüğü ve sensör tutarlılığı bağımsız gözetleyiciler tarafından denetlenir. İki sensör çelişirse veya zamanında veri gelmezse sistem hareketi durdurabilir. Acil durdurma mekanizması mümkün olduğunca yazılımdan bağımsız tasarlanır.

Sonuç olarak robot, cerrahın yerine karar veren sihirli bir makine değildir. Cerrah komutu üretir; yazılım ise bu komutu filtreler, küçültür, kinematik olarak çözer ve kapalı çevrim kontrolle güvenli harekete dönüştürür. Milisaniyelik aktarımın sırrı ham hızdan çok, doğru önceliklendirilmiş katmanlar ve deterministik mühendisliktir.
