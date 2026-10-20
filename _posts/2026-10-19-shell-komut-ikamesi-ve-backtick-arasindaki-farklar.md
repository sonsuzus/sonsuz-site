---
layout: post
title: "Shell Komut İkamesi: $(...) ve Backtick Arasındaki Farklar"
math: true
categories: 
  - Bilgi
tags: 
  - shell
  - bash
  - linux
  - komut ikamesi
  - güvenilirlik
  - betik yazımı
toc: true
image: /img/shell-komut-ikamesi-95.png
---

Shell betiklerinde bir komutun çıktısını başka bir komutun argümanı yapmak oldukça yaygındır. Bunun için modern `$(...)` söz dizimini veya eski backtick biçimini kullanabiliriz. İkisi basit örneklerde aynı sonucu üretse de iç içe komutlar, kaçış karakterleri ve bakım kolaylığı devreye girdiğinde aralarında ciddi farklar ortaya çıkar.

![shell-komut-ikamesi-95](/img/shell-komut-ikamesi-95.svg)

``
## Komut ikamesi nedir?

Komut ikamesi, shell'in bir komutu çalıştırıp standart çıktısını ilgili ifadenin yerine yerleştirmesidir. Örneğin geçerli tarihi bir değişkene atayabiliriz:

```bash
bugun=$(date +%F)
echo "Bugünün tarihi: $bugun"
```

Aynı işlem eski söz dizimiyle şöyle yazılır:

```bash
bugun=`date +%F`
echo "Bugünün tarihi: $bugun"
```

Shell, önce içteki `date` komutunu çalıştırır ve çıktının sonundaki satır sonlarını kaldırır. Sonuç daha sonra dış komuta aktarılır. Bu davranışı basitçe

$$S = \operatorname{trimTrailingNewlines}(\operatorname{stdout}(C))$$

şeklinde düşünebiliriz. Burada $C$ çalıştırılan komut, $S$ ise ikame edilen metindir.

## Temel farklar

\vert  Özellik \vert  `$(...)` | Backtick |
|---|---|---|
| Okunabilirlik | Başlangıç ve bitiş belirgindir | Tek karakterler kolayca gözden kaçar |
| İç içe kullanım | Doğrudan yazılabilir | İç backtick'ler kaçırılmalıdır |
| Modern kullanım | Tavsiye edilir | Eski betiklerde görülür |
| POSIX uyumluluğu | Desteklenir | Desteklenir |
| Hata ayıklama | Yapı görsel olarak nettir | Karmaşık ifadeler zor takip edilir |

En önemli avantaj, parantezlerin doğal biçimde eşleşmesidir. Örneğin bir dosyanın bulunduğu dizinin adını almak için şu yapı kullanılabilir:

```bash
dizin=$(dirname "$(find /tmp -name '*.log' -print -quit)")
printf 'Dizin: %s\n' "$dizin"
```

Önce `find` ilk günlük dosyasını bulur, ardından `dirname` dosyanın dizinini çıkarır. Okuyucu işlemleri içeriden dışarıya rahatça takip edebilir.

Backtick ile aynı ifade kaçış karakterleri ister:

```bash
dizin=`dirname "\`find /tmp -name '*.log' -print -quit\`"`
printf 'Dizin: %s\n' "$dizin"
```

Her yeni seviye, hangi backtick'in kaçırılması gerektiğini anlamayı zorlaştırır. Kabaca okunabilirlik maliyetini iç içe geçme derinliği $n$ ile ilişkilendirirsek, `$(...)` için maliyet daha düzenli büyürken backtick biçiminde kaçış yükü çok daha hızlı artar. Üç katmanlı bir komut, kısa sürede noktalama işareti bulmacasına dönüşebilir.

## Tırnak kullanımı neden kritik?

`$(...)` tek başına güvenlik kalkanı değildir. Sonucu tırnaksız kullanmak, sözcük bölme ve dosya adı genişletmesine yol açabilir:

```bash
dosya=$(cat secim.txt)
cat $dosya       # Riskli
cat "$dosya"     # Daha güvenilir
```

İlk kullanımda `secim.txt` içeriğinde boşluk veya `*` bulunuyorsa shell bunu birden fazla argümana ya da eşleşen dosyalara dönüştürebilir. İkinci kullanım çıktıyı tek argüman olarak korur. Bununla birlikte değişken içeriğini `eval` ile çalıştırmak veya güvenilmeyen girdiyi komut metnine dönüştürmek ayrıca komut enjeksiyonu riski yaratır.

## Hata durumlarını unutmayın

Komut ikamesi, iç komutun başarısızlığını her zaman dış işlem üzerinden görünür kılmaz:

```bash
if sonuc=$(grep 'READY' durum.txt); then
    printf 'Bulundu: %s\n' "$sonuc"
else
    printf 'Kayıt bulunamadı veya dosya okunamadı.\n' >&2
fi
```

Bu örnek hem çıktıyı yakalar hem de `grep` komutunun durum kodunu denetler. Uzun betiklerde yalnızca güzel söz dizimi değil, çıkış kodlarının bilinçli yönetilmesi de güvenilirliği artırır.

Sonuç olarak backtick tarihsel uyumluluk için tanınması gereken bir biçimdir; fakat yeni kodlarda `$(...)` tercih edilmelidir. Parantezli yapı iç içe komutları sadeleştirir, kaçış hatalarını azaltır ve kod incelemesini kolaylaştırır. Tırnaklama ve hata denetimiyle birleştiğinde shell betikleri daha öngörülebilir, bakımı daha kolay ve daha az sürprizli hâle gelir.
