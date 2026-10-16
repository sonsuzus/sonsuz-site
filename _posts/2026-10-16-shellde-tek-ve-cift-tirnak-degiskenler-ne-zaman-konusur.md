---
layout: post
title: "Shell’de Tek ve Çift Tırnak: Değişkenler Ne Zaman Konuşur?"
math: true
categories: 
  - Bilgi
tags: 
  - shell
  - bash
  - linux
  - değişken
  - tırnak
  - komut-satırı
toc: true
image: /img/shellde-tek-ve-81.png
---

Shell dünyasında tırnak işaretleri yalnızca boşluk içeren metinleri bir arada tutmaz; değişken genişletmesinin, komut çalıştırmanın ve özel karakterlerin yorumlanmasının kaderini belirler. Tek tırnak her şeyi olduğu gibi saklayan ciddi bir güvenlik görevlisiyken, çift tırnak bazı genişletmelere izin veren daha esnek bir kapı görevlisi gibidir.

![shellde-tek-ve-81](/img/shellde-tek-ve-81.svg)

``

## Değişken genişletmesi nedir?

Shell bir komutu çalıştırmadan önce satır üzerinde çeşitli dönüşümler gerçekleştirir. `$HOME` veya `${USER}` gibi ifadelerin değerleriyle değiştirilmesine **parametre genişletmesi** denir.

Bu süreci basitçe şöyle gösterebiliriz:

$$
\text{yazılan ifade} \xrightarrow{\text{shell genişletmesi}} \text{komuta gönderilen argümanlar}
$$

Örneğin `USER=ada` ise `$USER` ifadesinin genişletilmiş sonucu `ada` olur. Ancak bunun gerçekleşip gerçekleşmeyeceğini kullanılan tırnak türü belirler.

\vert  Yazım \vert  Değişken genişler mi? \vert  Komut ikamesi çalışır mı? \vert  Boşluklar korunur mu? \vert 
\vert ---\vert ---:\vert ---:\vert ---:\vert 
\vert  `$USER` | Evet | Evet | Her zaman değil |
| `"$USER"` \vert  Evet \vert  Evet \vert  Evet \vert 
\vert  `'$USER'` | Hayır | Hayır | Evet |

## Tek tırnak: Her şey olduğu gibi

Tek tırnaklar arasındaki karakterler shell tarafından değişmez metin olarak değerlendirilir. `$`, ters eğik çizgi ve komut ikamesinde kullanılan karakterler özel anlamlarını kaybeder.

```bash
name="Deniz"

echo '$name'
echo 'Kullanıcı: $name'
echo 'Bugün: $(date)'
```

Çıktı şöyledir:

```text
$name
Kullanıcı: $name
Bugün: $(date)
```

Shell burada değişkeni genişletmez ve `date` komutunu çalıştırmaz. Bu davranış düzenli ifadeler, SQL parçaları veya dolar işareti içeren sabit metinler yazarken oldukça kullanışlıdır.

Tek tırnağın küçük bir huysuzluğu vardır: Tek tırnak içinde başka bir tek tırnak doğrudan kullanılamaz. Parçaları birleştirmek gerekir:

```bash
echo 'Bugün hava güzel, değil mi?'
echo 'Ali'"'"'nin dosyası'
```

İkinci komut; tek tırnaklı `Ali`, çift tırnaklı tek tırnak karakteri ve yeniden tek tırnaklı metin olmak üzere üç bitişik parçayı birleştirir.

## Çift tırnak: Kontrollü genişletme

Çift tırnaklar metni tek argüman olarak korurken değişken genişletmesine, komut ikamesine ve bazı kaçışlara izin verir.

```bash
name="Ada Lovelace"
project_count=3

echo "Merhaba, $name"
echo "Proje sayısı: ${project_count}"
echo "Tarih: $(date +%F)"
```

Burada `$name` genişler, fakat içindeki boşluk nedeniyle iki ayrı argümana bölünmez. `${project_count}` yazımı ise değişken adının sınırlarını açıkça gösterir.

```bash
file="rapor final.txt"

rm $file      # İki ayrı dosya adı gibi yorumlanabilir
rm "$file"    # Tek bir dosya adı olarak gönderilir
```

Genel kural şudur: Özellikle dosya adlarında değişkenleri çift tırnakla kullanın. Bir değişkenin ürettiği sözcük sayısını kabaca şöyle düşünebiliriz:

$$
N_{\text{tırnaksız}} \ge 1, \qquad N_{\text{çift tırnaklı}} = 1
$$

Boş veya özel durumlar dışında çift tırnak, genişletilmiş değerin tek argüman kalmasını sağlar.

## Tırnaksız kullanım neden riskli?

Tırnaksız değişkenler **word splitting** ve dosya adı genişletmesine maruz kalabilir:

```bash
pattern="*.log"
printf '<%s>\n' $pattern
printf '<%s>\n' "$pattern"
```

İlk komut mevcut `.log` dosyalarını listeleyebilir. İkincisi ise kelimesi kelimesine `*.log` yazdırır. Yani çift tırnak yalnızca estetik değil, davranışı öngörülebilir kılan bir güvenlik kemeridir.

## Hızlı seçim rehberi

| İhtiyaç | Tercih |
|---|---|
| Tamamen sabit metin | Tek tırnak |
| Değişken içeren metin | Çift tırnak |
| Dosya yolu veya kullanıcı girdisi | Çift tırnak |
| Bilerek kelime bölme veya glob kullanma | Tırnaksız, dikkatle |

Özetle tek tırnak shell’e “hiçbir şeye dokunma”, çift tırnak ise “değişkenleri aç ama sonucu parçalama” der. Emin olmadığınızda `"$variable"` kullanmak çoğu shell betiğinde en güvenli ve en az sürprizli seçimdir.
