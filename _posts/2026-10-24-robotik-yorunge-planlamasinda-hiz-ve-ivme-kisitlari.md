---
layout: post
title: "Robotik Yörünge Planlamasında Hız ve İvme Kısıtları"
math: true
categories: 
  - Bilgi
tags: 
  - robotik
  - yörünge planlama
  - hareket kontrolü
  - kinematik
  - hız
  - ivme
toc: true
image: /img/robotik-yorunge-planlamasinda-35.png
---

Bir robot kolunun hedefe ulaşması yeterli değildir; bunu sarsılmadan, motorları zorlamadan ve etrafındaki kahveyi dökmeden yapması gerekir. Yörünge planlamasında hız ve ivme kısıtları, geometrik olarak mümkün bir yolu fiziksel olarak uygulanabilir ve pürüzsüz bir harekete dönüştürür.

``

## Yol ve yörünge aynı şey değildir

**Yol (path)**, robotun uzayda izleyeceği geometrik rotayı tanımlar. **Yörünge (trajectory)** ise bu rotaya zaman bilgisini ekler. Başka bir ifadeyle yol, “Nereden geçeceğim?”; yörünge ise “Hangi noktadan ne zaman ve ne kadar hızlı geçeceğim?” sorularını yanıtlar.

Bir eklemin konumu $q(t)$ ile gösterilirse hareketin temel büyüklükleri şöyledir:

$$v(t) = dq(t)/dt$$

$$a(t) = d^2q(t)/dt^2$$

Burada $v(t)$ eklem hızını, $a(t)$ ise eklem ivmesini temsil eder. Gerçek bir robotta bu değerler sınırsız değildir:

$$\vert v(t)\vert  \leq v_{max}, \qquad \vert a(t)\vert  \leq a_{max}$$

Bu sınırlar motor kapasitesi, redüktör yapısı, taşınan yük, güvenlik gereksinimleri ve kontrol döngüsünün performansı gibi etkenlerden doğar.

## Hız kısıtı neden önemlidir?

Bir motorun ulaşabileceği maksimum dönüş hızı vardır. Planlayıcı bu değeri aşan bir komut üretirse robot istenen hareketi takip edemez. Sonuçta konum hatası büyüyebilir, kontrolcü doygunluğa girebilir veya koruma sistemi robotu durdurabilir.

Hız sınırı yalnızca donanımı korumaz. İnsanlarla aynı ortamda çalışan robotlarda düşük ve öngörülebilir hızlar güvenliği de artırır. Ayrıca yüksek hız, dar bir virajdan geçen mobil robotun savrulmasına benzer şekilde, mekanik sistem üzerinde daha büyük dinamik etkiler oluşturabilir.

## İvme: Pürüzsüzlüğün görünmez kahramanı

Hızın aniden değişmesi, teoride mümkün görünse bile pratikte sonsuz ivme gerektirir. Örneğin hızın sıfırdan aniden $2\,m/s$ değerine çıktığını düşünelim. Geçiş süresi $\Delta t$ küçüldükçe

$$a \approx \frac{\Delta v}{\Delta t}$$

ifadesine göre gerekli ivme hızla büyür. Bu durum titreşim, mekanik aşınma, yük kayması ve yüksek tork talebi oluşturur. Robot bir bardak taşıyorsa agresif ivmelenme, başarılı bir teslimattan çok küçük bir mutfak felaketine dönüşebilir.

| Özellik | Hız sınırı | İvme sınırı |
|---|---|---|
| Kontrol ettiği büyüklük | Konum değişim oranı | Hız değişim oranı |
| Donanımsal karşılığı | Motorun maksimum devri | Motor torku ve yük ataleti |
| Aşılması halinde | Takip hatası, güvenlik riski | Sarsıntı, titreşim, aşınma |
| Hareket hissi | Ne kadar hızlı? | Ne kadar yumuşak? |

![robotik-yorunge-planlamasinda-35](/img/robotik-yorunge-planlamasinda-35.svg)


## Trapez hız profili

Yaygın çözümlerden biri trapez hız profilidir. Robot önce sabit ivmeyle hızlanır, mümkünse sabit hızla ilerler ve hedefe yaklaşırken sabit negatif ivmeyle yavaşlar. Mesafe kısa olduğunda maksimum hıza ulaşılamaz ve profil üçgensel olur.

Aşağıdaki Python örneği, hız komutunu izin verilen ivme miktarıyla kademeli olarak hedef hıza yaklaştırır:

```python
def sinirli_hiz_guncelle(v, hedef_v, a_max, dt):
    # Bir kontrol adımında izin verilen en büyük hız değişimi
    dv_max = a_max * dt
    hata = hedef_v - v

    # İvme sınırını aşmadan hız değişimini sınırla
    dv = max(-dv_max, min(hata, dv_max))
    return v + dv

v = 0.0
for _ in range(100):
    v = sinirli_hiz_guncelle(v, 1.5, 0.8, 0.02)
```

Bu yaklaşım, hedef hızı doğrudan motora göndermek yerine her kontrol çevriminde uygulanabilecek değişimi sınırlar. Ancak yalnızca anlık hız üretir; eksiksiz bir yörünge planlayıcısının durma mesafesini ve hedef konumu da hesaba katması gerekir.

## Daha da pürüzsüz hareket: jerk

Çok hassas uygulamalarda ivmenin sürekliliği de yeterli olmayabilir. İvmenin değişim oranına **jerk** denir:

$$j(t) = da(t)/dt$$

Jerk sınırlandırılmış S-eğrisi profilleri, ivmeyi bir anda değiştirmek yerine kademeli biçimde artırır. Böylece kamera robotları, CNC makineleri ve hassas taşıma sistemleri daha az titreşimle çalışır.

Sonuç olarak iyi bir yörünge, yalnızca çarpışmasız değildir. Robotun hız, ivme ve gerektiğinde jerk sınırlarını gözetir; hedefe zamanında ulaşırken motorları, taşınan yükü ve çevredeki insanları da korur. Pürüzsüzlük estetik bir ayrıntı değil, uygulanabilir robot hareketinin temel şartıdır.
