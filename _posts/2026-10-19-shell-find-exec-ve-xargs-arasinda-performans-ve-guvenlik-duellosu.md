---
layout: post
title: "Shell find: -exec ve xargs Arasında Performans ve Güvenlik Düellosu"
math: true
categories: 
  - Bilgi
tags: 
  - shell
  - linux
  - find
  - xargs
  - performans
  - güvenlik
toc: true
image: /img/shell-find-exec-69.png
---

![shell-find-exec-69](/img/shell-find-exec-69.svg)


`find` ile binlerce dosyayı aradıktan sonra üzerlerinde işlem yapmak istediğimizde iki popüler seçenek karşımıza çıkar: `-exec` ve `xargs`. İkisi de bulunan yolları başka bir komuta aktarır; ancak süreç oluşturma maliyeti, özel karakter içeren dosya adları ve güvenilmeyen dizinlerle çalışma konusunda davranışları aynı değildir. Yanlış seçim betiği yalnızca yavaşlatmaz, beklenmedik dosyaların işlenmesine de yol açabilir.

``

## Temel çalışma mantığı

Klasik `-exec`, bulunan her dosya için komutu ayrı çalıştırabilir:

```bash
find logs -type f -name '*.log' -exec gzip '{}' \;
```

Buradaki `{}` bulunan dosyanın tam yolu ile değiştirilir, `\;` ise `-exec` ifadesini sonlandırır. Dosya adı komuta doğrudan bir argüman olarak verildiğinden boşluklar, satır sonları veya joker karakterler yeniden yorumlanmaz.

Buna karşılık `xargs`, standart girdiden aldığı yolları gruplandırarak komut satırları oluşturur:

```bash
find logs -type f -name '*.log' -print0 |
  xargs -0 gzip
```

`-print0` yolları NUL karakteriyle ayırır; `xargs -0` aynı biçimi okur. Unix dosya adlarında NUL bulunamayacağı için bu ikili, sıra dışı dosya adlarında güvenli bir protokol sağlar.

## Performans neden değişiyor?

Bir süreç başlatmanın maliyetini $C_p$, tek bir dosyayı işlemenin maliyetini $C_f$ ve dosya sayısını $n$ kabul edelim. Dosya başına çalışan klasik kullanımın yaklaşık maliyeti:

$$T_{exec} \approx n(C_p + C_f)$$

`xargs` dosyaları ortalama $b$ elemanlık gruplara ayırırsa maliyet yaklaşık olarak şöyledir:

$$T_{xargs} \approx \left\lceil\frac{n}{b}\right\rceil C_p + nC_f$$

Dolayısıyla kısa süren bir komut binlerce kez çağrıldığında süreç maliyeti belirginleşir. Fakat `find` modern ve daha güvenli bir toplu çalışma seçeneğine de sahiptir:

```bash
find logs -type f -name '*.log' -exec gzip '{}' +
```

Sondaki `+`, mümkün olduğunca çok yolu tek komut çağrısında toplar. Böylece `xargs` benzeri performans elde edilirken ayrı bir boru hattına ihtiyaç kalmaz. Her iki yöntem de işletim sisteminin `ARG_MAX` sınırını dikkate alarak grupları böler.

| Yöntem | Komut çağrısı | Dosya adı güvenliği | Paralellik |
|---|---:|---|---|
| `-exec ... \;` | Her dosya için bir | Yüksek | Doğrudan yok |
| `-exec ... +` | Toplu | Yüksek | Doğrudan yok |
| `xargs` | Toplu | Ayırıcılara bağlı | `-P` ile var |
| `-print0 \| xargs -0` | Toplu | Yüksek | `-P` ile var |

## Güvenlikte asıl tuzaklar

Şu kullanım güvenilir değildir:

```bash
find uploads -type f | xargs rm
```

`rapor final.txt` iki ayrı argümana bölünebilir. Daha kötüsü, dosya adında satır sonu veya tırnak bulunması ayrıştırmayı bozabilir. Çözüm `-print0 | xargs -0` kullanmak ya da doğrudan `-exec ... +` seçmektir.

`xargs` kendi başına bir shell başlatmaz; bu nedenle dosya adındaki `;` veya `$()` otomatik olarak çalıştırılmaz. Tehlike genellikle girdiyi metin olarak ayrıştırmaktan veya gereksiz yere `sh -c` kullanmaktan doğar:

```bash
# Güvenilmeyen adları komut metnine gömmeyin
find uploads -type f -exec sh -c "process {}" \;
```

Bunun yerine yolu konumsal argüman yapın:

```bash
find uploads -type f -exec sh -c 'for f; do process "$f"; done' sh '{}' +
```

Ayrıca bulunan dosya ile işlemin uygulanması arasında dosyanın değiştirilebildiği yarış koşulları her iki yöntemi de etkileyebilir. Güvenilmeyen, başkalarının yazabildiği dizinlerde `-execdir` komutu dosyanın bulunduğu dizinde çalıştırarak bazı yol değiştirme saldırılarını azaltır. Bununla birlikte güvenli bir `PATH` ayarlamak gerekir.

## Hangisini seçmeli?

Genel amaçlı ve sağlam varsayılan seçenek `-exec ... +` kullanmaktır: hızlıdır, okunaklıdır ve dosya adlarını doğru taşır. Paralel işlem gerekiyorsa `-print0 | xargs -0 -P 4` güçlüdür; ancak komutun eş zamanlı çalışmaya uygun olduğundan emin olun. Her dosyanın ayrı süreçte çalışması özellikle gerekmiyorsa `-exec ... \;` büyük veri kümelerinde gereksiz derecede pahalıdır.
