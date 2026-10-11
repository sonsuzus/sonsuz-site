---
layout: post
title: "Antik Dünyadan Rönesans’a: Caesar, Polybius ve Vigenère Şifreleri"
math: true
categories: 
  - Bilgi
tags: 
  - kriptografi
  - caesar
  - polybius
  - vigenère
  - şifreleme
  - siber güvenlik
toc: true
image: /img/antik-dunyadan-ronesansa-25.png
---

Günümüzde şifreleme denince akla devasa asal sayılar ve karmaşık algoritmalar geliyor. Oysa kriptografinin temelleri, harfleri kaydırmak veya bir tabloya yerleştirmek kadar basit fikirlerle atıldı. Caesar, Polybius ve Vigenère şifreleri yalnızca tarihî merak konusu değildir; modern şifrelemenin neden anahtar, anahtar uzayı ve istatistiksel direnç gibi kavramlara ihtiyaç duyduğunu gösteren harika laboratuvarlardır.

![antik-dunyadan-ronesansa-25](/img/antik-dunyadan-ronesansa-25.svg)

``
## Caesar şifresi: Alfabeyi biraz kaydıralım

Adını Roma lideri Julius Caesar’dan alan bu yöntemin askerî yazışmalarda kullanıldığı anlatılır. Her harf, alfabede sabit miktarda ileri kaydırılır. Harfleri $0$ ile $25$ arasında numaralandırırsak şifreleme işlemi şöyle gösterilir:

$$E_k(x) = (x + k) \bmod 26$$

Şifreyi çözmek için kaydırma geri alınır:

$$D_k(x) = (x - k) \bmod 26$$

Örneğin $k=3$ olduğunda `ABC`, `DEF` olur. Fikir zarif olsa da yalnızca 26 olası anahtar vardır. Saldırgan bütün kaydırmaları deneyerek anlamlı sonucu birkaç saniyede bulabilir. Buna **kaba kuvvet saldırısı** denir. Uzun metinlerde en sık görülen harfi dildeki yaygın harflerle karşılaştıran frekans analizi de kullanılabilir.

```python
def caesar(metin, kaydirma):
    sonuc = ""
    for karakter in metin.upper():
        if "A" <= karakter <= "Z":
            kod = (ord(karakter) - ord("A") + kaydirma) % 26
            sonuc += chr(kod + ord("A"))
        else:
            sonuc += karakter
    return sonuc

print(caesar("KRIPTOGRAFI", 3))
```

Bu kod, yalnızca Latin alfabesindeki harfleri kaydırır; boşluk ve noktalama işaretlerini korur. Negatif kaydırma verilerek şifre çözme işlemi de yapılabilir.

## Polybius karesi: Harfler koordinata dönüşüyor

MÖ 2. yüzyılda yaşamış Yunan tarihçi Polybius, karakterleri bir tablo üzerindeki koordinatlarla temsil etti. Klasik $5 \times 5$ karede I ve J aynı hücreyi paylaşır. Örneğin A `11`, B `12`, F ise `21` olarak yazılır.

Bu yaklaşımın önemli özelliği, harfleri sayısal çiftlere dönüştürmesidir. Böylece mesajlar meşale, ses veya işaret kombinasyonlarıyla iletilebilir. Ancak standart kare gizli değilse saldırgan koordinatları doğrudan geri çevirebilir. Karışık anahtarlı bir alfabe kullanılsa bile tek bir harf daima aynı çifte dönüştüğü için frekans analizi hâlâ etkilidir.

## Vigenère: Tek kaydırma yetmezse

16. yüzyılda Blaise de Vigenère ile özdeşleşen bu yöntem, tekrar eden bir anahtar kelime kullanarak her karaktere farklı Caesar kaydırması uygular. Matematiksel olarak:

$$C_i = (P_i + K_i) \bmod 26$$

`ANAHTAR` gibi bir anahtar, mesaj uzunluğunca tekrarlanır. Böylece aynı düz metin harfi farklı konumlarda farklı şifreli harflere dönüşebilir. Bu nedenle Vigenère uzun süre **çözülemez şifre** olarak ün kazandı.

```python
def vigenere_sifrele(metin, anahtar):
    metin = metin.upper()
    anahtar = anahtar.upper()
    sonuc, sira = "", 0

    for harf in metin:
        if harf.isalpha() and "A" <= harf <= "Z":
            kaydirma = ord(anahtar[sira % len(anahtar)]) - ord("A")
            sonuc += chr((ord(harf) - ord("A") + kaydirma) % 26 + ord("A"))
            sira += 1
        else:
            sonuc += harf
    return sonuc
```

Şifrenin zayıf noktası anahtarın tekrarlanmasıdır. **Kasiski incelemesi**, şifreli metindeki yinelenen diziler arasındaki uzaklıkları ölçerek muhtemel anahtar uzunluğunu bulur. Friedman testi ise harflerin çakışma olasılığından yararlanır. Uzunluk belirlendikten sonra metin sütunlara ayrılır ve her sütun ayrı bir Caesar şifresi gibi frekans analiziyle çözülür.

## Hızlı karşılaştırma

| Teknik | Temel fikir | Anahtar uzayı | Başlıca kırılma yöntemi |
|---|---|---:|---|
| Caesar | Sabit harf kaydırma | Çok küçük | Kaba kuvvet, frekans analizi |
| Polybius | Harfi koordinata çevirme | Kare düzenine bağlı | Eşleme ve frekans analizi |
| Vigenère | Tekrarlanan çoklu kaydırma | Anahtara bağlı | Kasiski, Friedman, frekans analizi |

Bu üç yöntem bize önemli bir ders verir: Bir algoritmanın karmaşık görünmesi güvenli olduğu anlamına gelmez. Küçük anahtar uzayı, tekrar eden desenler ve dilin istatistiksel yapısı saldırgana ipucu verir. Yine de bu klasikler, modern kriptografideki saldırı modelini anlamak ve kendi şifre analiz araçlarımızı geliştirmek için vazgeçilmez başlangıç noktalarıdır.
