---
layout: post
title: "Shell Değişkenlerinde Tırnak: Bir Boşluk Nasıl Dosya Adını Parçalar?"
math: true
categories: 
  - Bilgi
tags: 
  - shell
  - bash
  - word-splitting
  - linux
  - komut-satırı
  - güvenli-kodlama
toc: true
image: /img/shell-degiskenlerinde-tirnak-75.png
---

![shell-degiskenlerinde-tirnak-75](/img/shell-degiskenlerinde-tirnak-75.svg)


Shell betiklerinde `$var` ile `"$var"` arasındaki iki küçük tırnak, çalışan bir komutla gizemli hatalar üreten bir komut arasındaki fark olabilir. Özellikle dosya adları boşluk içerdiğinde tırnaksız değişken kullanımı, değerin birden fazla argümana bölünmesine neden olur. Shell bu davranışı kötü niyetinden değil, tarihsel kurallarından dolayı sergiler!
``
## Temel sorun: Değer başka, argüman başka

Bir değişkenin içinde tek bir dosya adı bulunması, komutun onu mutlaka tek argüman olarak göreceği anlamına gelmez:

```bash
file="Yıllık Rapor.txt"
rm $file
```

İlk bakışta bu kodun `Yıllık Rapor.txt` dosyasını sileceği düşünülebilir. Fakat değişken tırnaksız genişletildiği için shell, ortaya çıkan metne **word splitting** uygular. Komut kabaca şuna dönüşür:

```bash
rm Yıllık Rapor.txt
```

Burada `rm`, `Yıllık` ve `Rapor.txt` adında iki ayrı dosya argümanı alır. Doğru kullanım şöyledir:

```bash
rm "$file"
```

Çift tırnak, değişken genişletmesine izin verirken sonucun tek argüman olarak korunmasını sağlar.

## Word splitting nasıl çalışır?

Shell, tırnaksız parametre genişletmesinden çıkan metni `$IFS` değişkenindeki ayırıcılara göre parçalar. Varsayılan olarak bunlar boşluk, sekme ve satır sonudur. Basitleştirilmiş biçimde süreç şöyle gösterilebilir:

$$
\text{argümanlar} = \operatorname{split}(\text{expand}(\$var), IFS)
$$

Değer `Proje Dosyaları/plan 2026.md` ise boşluklara göre üç kelime oluşabilir:

$$
1\ \text{dosya yolu} \longrightarrow 3\ \text{komut argümanı}
$$

| Yazım | Değişken genişler mi? | Kelime bölünmesi | Sonuç |
|---|---:|---:|---|
| `$var` \vert  Evet \vert  Evet \vert  Riskli; birden çok argüman oluşabilir \vert 
\vert  `"$var"` | Evet | Hayır | Değer tek argüman kalır |
| `'$var'` \vert  Hayır \vert  Hayır \vert  Komuta kelimesi kelimesine `$var` gider |

Tek tırnak ile çift tırnağı karıştırmamak önemlidir. `'$var'`, değişkenin değerini değil, doğrudan `$var` metnini temsil eder.

## Sorunu görünür hâle getirelim

Bir komutun gerçekte kaç argüman aldığını küçük bir fonksiyonla inceleyebiliriz:

```bash
show_args() {
    printf 'Argüman sayısı: %s\n' "$#"
    printf '<%s>\n' "$@"
}

name="tatil fotoğrafı.jpg"
show_args $name
show_args "$name"
```

İlk çağrı iki argüman, ikinci çağrı ise tek argüman üretir. `"$@"` yazımı da özeldir: Fonksiyona gelen her argümanı ayrı ayrı ve içeriğini bozmadan aktarır.

## Tehlike yalnızca boşluk değildir

Tırnaksız genişletmeden sonra **pathname expansion**, yani glob genişletmesi de gerçekleşebilir:

```bash
pattern="*"
printf '%s\n' $pattern
```

Bu kod yıldız karakterini yazdırmak yerine mevcut dizindeki dosyaları listeleyebilir. Dolayısıyla tırnaksız kullanım yalnızca yanlış sonuçlara değil, beklenmeyen dosyaların taşınmasına veya silinmesine de yol açabilir.

| Girdi içeriği | Tırnaksız risk | Tırnaklı davranış |
|---|---|---|
| Boşluk | Birden fazla kelimeye ayrılır | Tek argüman kalır |
| `*`, `?`, `[...]` | Dosya adlarına genişleyebilir | Karakterler korunur |
| Boş değer | Argüman tamamen kaybolabilir | Boş bir argüman gönderilir |
| Satır sonu | Yeni kelimeler oluşturabilir | Değer içinde korunur |

## Sağlam kullanım alışkanlıkları

Değişken genişletmelerini varsayılan olarak çift tırnak içine alın:

```bash
cp -- "$source" "$destination"
mkdir -p -- "$directory"
printf '%s\n' "$message"
```

Buradaki `--`, sonraki değerin `-` ile başlasa bile seçenek olarak yorumlanmasını önler. Birden fazla öğe saklamak gerektiğinde boşluklarla birleştirilmiş metin yerine Bash dizisi kullanın:

```bash
files=("Yıllık Rapor.txt" "tatil fotoğrafı.jpg")
cp -- "${files[@]}" backup/
```

Özet kural oldukça basittir: **Tırnaksız değişken kullanmak için özel bir nedeniniz yoksa değişkeni çift tırnakla çevreleyin.** Shell dünyasında tırnaklar süs değil, argümanların emniyet kemeridir.
