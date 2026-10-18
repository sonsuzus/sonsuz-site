---
layout: post
title: "Tek Bir Beyin Yok: Sürü Robotları Nasıl Birlikte Düşünüyor?"
math: true
categories: 
  - Bilgi
tags: 
  - robotik
  - sürü-robotiği
  - yapay-zeka
  - dağıtık-sistemler
  - otonom-robotlar
  - algoritma
toc: true
image: /img/tek-bir-beyin-30.png
---

![tek-bir-beyin-30](/img/tek-bir-beyin-30.svg)


Bir robotun odadaki nesneleri toplaması etkileyicidir; yüzlerce küçük robotun lider olmadan alan taraması, yük taşıması veya kayıp bir kişiyi araması ise bilim kurgu gibi görünür. Sürü robotiği, tam olarak bu kolektif davranışı inceler. Karıncaların yiyecek bulması ve kuşların çarpışmadan uçması gibi doğadaki örneklerden esinlenen yaklaşımda karmaşık görevler, basit yerel kurallara uyan çok sayıda robot tarafından çözülür.

``

## Merkezi olmayan koordinasyon nedir?

Geleneksel bir robot filosunda merkezi bilgisayar, her robota nereye gideceğini söyleyebilir. Sürü robotiğinde ise çoğunlukla böyle bir komutan bulunmaz. Her robot yalnızca sensörlerinden, yakın komşularından ve çevrede bırakılan dolaylı işaretlerden yararlanarak karar verir. Başka bir deyişle hiçbir robot büyük resmin tamamını görmez; ancak sürü, yerel etkileşimlerden küresel bir düzen üretir.

Bu olgu **belirme** veya *emergence* olarak adlandırılır. Bir robotun davranışını basitçe şöyle modelleyebiliriz:

$$u_i(t)=f(x_i(t),\,N_i(t),\,E_i(t))$$

Burada $u_i(t)$ robotun hareket komutunu, $x_i(t)$ kendi durumunu, $N_i(t)$ algıladığı komşuları ve $E_i(t)$ çevresel bilgiyi temsil eder. Fonksiyon basit olsa bile bütün robotların tekrar eden etkileşimi karmaşık sonuçlar doğurabilir.

| Özellik | Merkezi sistem | Merkezi olmayan sürü |
|---|---|---|
| Karar noktası | Tek sunucu veya lider | Her robot |
| Arıza etkisi | Merkez bozulursa sistem durabilir | Birkaç robot kaybedilse de görev sürebilir |
| Ölçeklenme | İletişim yükü hızla artar | Yerel iletişimle daha kolaydır |
| Küresel plan | Genellikle güçlüdür | Dolaylı biçimde ortaya çıkar |
| Robot gereksinimi | Daha karmaşık olabilir | Basit ve düşük maliyetli olabilir |

## Basit kurallar, şaşırtıcı sonuçlar

Sürülerde sık kullanılan üç hareket kuralı vardır: komşularla çarpışmayı önleyen **ayrılma**, aynı yönde ilerlemeyi sağlayan **hizalanma** ve grubun yakınında kalmayı sağlayan **uyum**. Robot $i$ için birleşik hız komutu şu şekilde yazılabilir:

$$v_i=\alpha v_{ayrılma}+\beta v_{hizalanma}+\gamma v_{uyum}$$

$[1m$

$[0m$\alpha$, $\beta$ ve $\gamma$ katsayıları sürünün karakterini değiştirir. Ayrılma ağırlığı düşükse robotlar birbirine girebilir; uyum aşırı yüksekse sürü hedef yerine kendi merkezine takıntılı hâle gelebilir. Robotların bile ayar tutturması gerekiyor!

Aşağıdaki Python benzeri kod, bir robotun komşularına göre yönünü güncelleyen sadeleştirilmiş bir kontrol döngüsüdür:

```python
def yeni_hiz(robot, komsular, hedef):
    ayrilma = carpismadan_kac(robot, komsular)
    hizalanma = ortalama_hiz(komsular)
    uyum = komsu_merkezine_git(robot, komsular)
    gorev = hedefe_yonel(robot, hedef)

    return (1.5 * ayrilma
            + 0.8 * hizalanma
            + 0.6 * uyum
            + 1.2 * gorev)
```

Bu fonksiyon merkezi bir plan istemez. Her robot aynı döngüyü kendi ölçümleriyle çalıştırır. Katsayılar simülasyonda denenebilir veya pekiştirmeli öğrenmeyle optimize edilebilir.

## Sürü görevleri nasıl bölüşür?

Koordinasyon yalnızca birlikte hareket etmek değildir. Robotlar keşif, taşıma ve iletişim rölesi gibi rolleri de paylaşabilir. Örneğin bir robot hedef bulduğunda dijital bir “feromon” bırakabilir. Diğerleri bu işaretin yoğunluğunu takip ederken işaret zamanla buharlaşır. Böylece eski bilgiler unutulur, güncel ve kısa rotalar güçlenir.

Bir görevin robot tarafından seçilme olasılığı eşik modeliyle ifade edilebilir:

$$P(task)=\frac{s^n}{s^n+\theta^n}$$

Burada $s$ görevin uyarı gücü, $\theta$ robotun uzmanlık eşiğidir. Farklı eşikler, önceden lider atamadan doğal bir iş bölümü oluşturur.

## Güçlü ama kusursuz değil

Sürü robotiği arama-kurtarma, hassas tarım, depo otomasyonu, uzay keşfi ve çevresel izleme için dayanıklı çözümler sunar. Ancak zayıf iletişim, sensör gürültüsü, enerji sınırları ve yerel kuralların beklenmeyen davranışlar üretmesi ciddi sorunlardır. Ayrıca yüzlerce robotun güvenli olduğunu matematiksel olarak doğrulamak, tek robotu doğrulamaktan çok daha zordur.

Yine de yaklaşımın temel fikri son derece güçlüdür: Karmaşıklık her zaman karmaşık bir yöneticiden gelmek zorunda değildir. Doğru yerel kurallar, sürekli geri bildirim ve yeterli sayıda katılımcı birleştiğinde, sürü tek tek üyelerinden çok daha yetenekli bir sisteme dönüşebilir.
