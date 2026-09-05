---
layout: post
title: "Kod İnceleme Kültürü: Egodan Uzak, Kaliteye Yakın"
math: true
categories: 
  - Bilgi
tags: 
  - code-review
  - takım-kültürü
  - yazılım-kalitesi
toc: true
---

Kod inceleme, yalnızca hataları yakalamak için açılan teknik bir kontrol kapısı değildir; bilginin ekip içinde dolaşmasını, ortak standartların oluşmasını ve geliştiricilerin birbirinden öğrenmesini sağlayan sosyal bir sistemdir. Ancak yanlış kurulduğunda “Bu kod kötü” cümlesi kolayca “Sen kötü bir geliştiricisin” şeklinde algılanabilir. Sağlıklı bir kültürün temel amacı, insanları yargılamak değil ürünü birlikte iyileştirmektir.
``
## Kod İncelemenin Görünmeyen Katmanı

Bir pull request içinde görünen şey kod olsa da tartışmanın arkasında güven, statü, aidiyet ve uzmanlık algısı bulunur. İnsan beyni eleştiriyi bazen sosyal tehdit olarak yorumlar. Özellikle yazılı iletişimde ses tonu kaybolduğu için kısa bir “Yanlış olmuş” yorumu, yazanın niyetinden çok daha sert duyulabilir.

İnceleme kalitesini basitçe şöyle modelleyebiliriz:

$$Q = T \times G \times A$$

Burada $Q$ inceleme kalitesini, $T$ teknik doğruluğu, $G$ psikolojik güveni, $A$ ise açıklık düzeyini temsil eder. Çarpım kullanılması önemlidir: Teknik bilgi çok yüksek olsa bile güven sıfıra yaklaşırsa toplam fayda da çöker. Kimse soru sormuyor, itiraz etmiyor veya hatasını kabul edemiyorsa süreç yalnızca törensel bir onaya dönüşür.

## Koda Karşı Ol, Kişiye Değil

Yorumların öznesi geliştirici değil, kod ve beklenen davranış olmalıdır. “Bunu neden böyle yaptın?” sorgulayıcı duyulabilirken “Bu yaklaşım yüksek trafikte nasıl davranır?” merak ve iş birliği daveti taşır.

| Çatışma üreten ifade | Kalite odaklı alternatif | Etkisi |
|---|---|---|
| “Bu çok kötü.” | “Bu bölüm okunabilirliği zorlaştırabilir.” | Kişiden probleme yönelir |
| “Yanlış yapmışsın.” | “Şu kenar durumda hata oluşabilir.” | Somut risk gösterir |
| “Böyle yazılmaz.” | “Ekip standardımız burada X yaklaşımını öneriyor.” | Kişisel zevki ortak kurala bağlar |
| “Bunu değiştir.” | “Şu çözümü değerlendirebilir miyiz?” | Diyaloğa alan açar |

Yorumları önem seviyesine göre etiketlemek de gereksiz gerilimi azaltır: `blocking` birleştirmeyi engelleyen problemi, `suggestion` iyileştirme önerisini, `nit` ise küçük bir stil tercihini belirtebilir. Böylece yazar her yorumun acil ve zorunlu olduğunu düşünmez.

## Somutluk: Egonun Panzehiri

İyi yorum; problemi, etkisini ve mümkünse alternatifi açıklar. Örneğin aşağıdaki kod küçük listelerde çalışsa da eleman sayısı büyüdüğünde gereksiz karşılaştırmalar yapar:

```python
def ortak_elemanlar(a, b):
    # Her elemanı diğer listedeki tüm elemanlarla karşılaştırır.
    return [x for x in a if x in b]
```

Yorum “Verimsiz yazılmış” olmamalıdır. Daha öğretici bir inceleme şöyle yapılabilir: “`b` bir liste olduğu için üyelik kontrolü $O(n)$ sürüyor; toplam karmaşıklık yaklaşık $O(n \times m)$. `b` değerini kümeye dönüştürerek ortalama üyelik maliyetini $O(1)$ seviyesine indirebiliriz.”

```python
def ortak_elemanlar(a, b):
    # Küme, tekrar eden üyelik kontrollerini hızlandırır.
    b_kumesi = set(b)
    return [x for x in a if x in b_kumesi]
```

Bu yaklaşım yalnızca düzeltme istemez; gerekçeyi aktararak ekip bilgisini büyütür.

## Süreci Güvenli Hâle Getiren Alışkanlıklar

- Pull request’leri küçük tutun; küçük değişiklik daha hızlı ve dikkatli incelenir.
- Eleştiriden önce bağlamı sorun; farklı görünen kararın bilinmeyen bir nedeni olabilir.
- İyi tercihleri de belirtin. İnceleme sadece kusur avcılığı değildir.
- Üslup tartışmalarını otomatik biçimlendiricilere ve linter araçlarına bırakın.
- Uzayan yazılı tartışmayı kısa bir görüşmeyle çözün, sonucu yeniden kayda geçirin.
- Kıdemi mutlak doğruluk saymayın; junior geliştiriciler de değerli sorular sorabilir.

Son olarak inceleme başarısını “kaç hata bulduk?” ile ölçmek eksiktir. İnceleme süresi, tekrar açılan hatalar, yorumların çözülme biçimi ve ekipteki psikolojik güven birlikte değerlendirilmelidir. Güçlü code review kültüründe amaç kazanan bir tartışmacı bulmak değil, daha iyi bir kod tabanına birlikte ulaşmaktır. Kod geçicidir; ekip içinde kurulan güven ise sonraki bütün projelerin altyapısıdır.
