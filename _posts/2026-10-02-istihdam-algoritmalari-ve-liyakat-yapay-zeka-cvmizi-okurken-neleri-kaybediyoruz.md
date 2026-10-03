---
layout: post
title: "İstihdam Algoritmaları ve Liyakat: Yapay Zeka CV’mizi Okurken Neleri Kaybediyoruz?"
math: true
categories: 
  - Bilgi
tags: 
  - yapay zeka
  - istihdam
  - algoritmik önyargı
  - insan kaynakları
  - makine öğrenmesi
  - etik
toc: true
image: /img/istihdam-algoritmalari-ve-62.png
---

Bir pozisyona yüzlerce kişi başvurduğunda bütün CV’leri insanların incelemesi zorlaşıyor. Şirketler bu sorunu ATS adı verilen aday takip sistemleri ve yapay zeka destekli sıralama algoritmalarıyla çözmeye çalışıyor. Ne var ki hız kazandıran bu dijital kapıcılar, liyakati ölçmek yerine CV’de doğru sihirli kelimelerin bulunup bulunmadığını kontrol edebiliyor. Sonuçta güçlü bir aday, yalnızca deneyimini algoritmanın beklediği lehçeyle anlatmadığı için daha kapıyı çalamadan elenebiliyor.
``

## Dijital eleme nasıl çalışıyor?

Klasik bir ATS, iş ilanındaki terimleri CV metniyle karşılaştırır. İlanda “Python”, “Docker” ve “mikroservis” geçiyorsa sistem bu kelimelerin aday belgesinde bulunmasına puan verebilir. Basitleştirilmiş bir uygunluk skoru şöyle düşünülebilir:

$$
S = w_k K + w_d D + w_e E - w_g G
$$

Burada $K$ anahtar kelime eşleşmesini, $D$ deneyim süresini, $E$ eğitim uyumunu, $G$ ise açıklanamayan boşluklar gibi algoritmanın risk saydığı özellikleri temsil eder. $w$ değerleri her ölçütün ağırlığıdır. Sorun, anahtar kelime ağırlığı $w_k$ gereğinden yüksek olduğunda başlar.

Modern sistemler yalnızca birebir kelime aramaz; metin gömmeleriyle anlam benzerliği de hesaplayabilir. Kosinüs benzerliği kullanılan bir modelde aday ile ilan vektörleri arasındaki yakınlık şöyledir:

$$
\operatorname{sim}(a,j)=\frac{a\cdot j}{\lVert a\rVert\lVert j\rVert}
$$

Bu yöntem “yazılım geliştirici” ile “programcı” ifadelerinin ilişkisini yakalayabilir. Ancak geçmiş işe alım verileri önyargılıysa daha akıllı model, daha adil değil; yalnızca geçmiş tercihleri daha ustaca taklit eden bir model olur.

## Anahtar kelime saplantısının kaybettirdikleri

| Algoritmanın kolayca gördüğü | Görmekte zorlandığı |
|---|---|
| Sertifika ve teknoloji adları | Hızlı öğrenme kapasitesi |
| Çalışılan yıl sayısı | Deneyimin niteliği |
| Standart unvanlar | Sıra dışı kariyer geçişleri |
| Kesintisiz iş geçmişi | Bakım emeği ve kişisel koşullar |
| Diploma bilgisi | Açık kaynak katkısı ve merak |

Örneğin küçük bir işletmede tek başına ödeme sistemi kuran biri “Site Reliability Engineer” unvanını hiç kullanmamış olabilir. Buna karşılık ilan metnindeki bütün terimleri CV’sine serpiştiren başka bir aday yüksek puan alabilir. Sistem potansiyeli değil, çoğu zaman metinsel itaati ödüllendirir.

## Küçük bir sıralayıcı, büyük bir ders

Aşağıdaki Python örneği, kelime eşleşmesine dayalı kaba bir filtreyi gösterir:

```python
ilan = {"python", "docker", "api", "postgresql"}

adaylar = {
    "Ada": {"python", "flask", "sql", "linux"},
    "Deniz": {"python", "docker", "api", "postgresql"},
    "Ece": {"backend", "konteyner", "web servisi", "veritabanı"}
}

def puanla(yetenekler):
    return len(ilan & yetenekler) / len(ilan)

sirali = sorted(adaylar.items(),
                key=lambda aday: puanla(aday[1]),
                reverse=True)

for isim, yetenekler in sirali:
    print(isim, puanla(yetenekler))
```

Kod, ilan kümesiyle adayın yetenek kümesinin kesişimini ölçer. Deniz tam puan alırken Ece, aynı kavramları farklı sözcüklerle ifade ettiği için sıfıra yaklaşır. Eş anlamlı sözlüğü veya anlamsal model eklemek bu problemi azaltabilir; fakat iletişim, yaratıcılık ve gelişim hızı hâlâ birkaç etikete indirgenemez.

## Daha adil bir sistem mümkün mü?

İlk adım, algoritmayı nihai karar verici değil karar destek aracı yapmaktır. Şirketler rastgele seçilmiş düşük puanlı CV’leri insanlar aracılığıyla yeniden inceleyerek yanlış negatif oranını ölçmelidir. Bu oran şu şekilde ifade edilir:

$$
FNR = \frac{FN}{FN + TP}
$$

Buradaki $FN$, sistemin elediği hâlde gerçekte uygun olan adaylardır. Ayrıca isim, yaş, fotoğraf ve adres gibi ilgisiz bilgiler mümkün olduğunca maskelenmeli; kullanılan ölçütler pozisyon başarısıyla düzenli olarak doğrulanmalıdır.

Adaylara da neden elendiklerini açıklama ve karara itiraz etme kanalı sunulmalıdır. Liyakat, en fazla anahtar kelimeyi yazmak değil işi yapabilme ve gelişebilme kapasitesidir. İyi bir istihdam algoritması insan yargısını ortadan kaldırmaz; onun kör noktalarını görünür kılar. Aksi hâlde yapay zeka yetenek keşfeden bir teleskop değil, yalnızca geçmişe çevrilmiş pahalı bir ayna olur.

![istihdam-algoritmalari-ve-62](/img/istihdam-algoritmalari-ve-62.svg)

