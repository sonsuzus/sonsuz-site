---
layout: post
title: "PATH Sırası: Terminal Hangi Komutu Çalıştırıyor?"
math: true
categories: 
  - Bilgi
tags: 
  - shell
  - path
  - linux
  - terminal
  - komut-satırı
  - güvenlik
toc: true
image: /img/path-sirasi-terminal-76.png
---

Terminale `python`, `node` veya `git` yazdığınızda kabuk, bu programın nerede olduğunu sihirli biçimde bilmez. Bunun yerine `PATH` adlı ortam değişkenindeki dizinleri soldan sağa tarar ve eşleşen ilk çalıştırılabilir dosyayı seçer. Dolayısıyla aynı isimli iki komuttan hangisinin çalışacağı, çoğu zaman sürüm numarasından değil dizinlerin sırasından kaynaklanır.
``
## PATH tam olarak nedir?

`PATH`, çalıştırılabilir dosyaların aranacağı dizinleri tutan bir listedir. Linux ve macOS sistemlerinde dizinler `:` karakteriyle ayrılır:

```bash
printf '%s\n' "$PATH"
```

Örnek bir çıktı şöyle olabilir:

```text
/home/ada/bin:/usr/local/bin:/usr/bin:/bin
```

Kabuk, `ornek` komutu girildiğinde önce `/home/ada/bin/ornek`, sonra `/usr/local/bin/ornek` ve devamında diğer olasılıkları kontrol eder. İlk uygun dosya bulunduğunda arama sona erer.

Bunu matematiksel olarak $PATH = (d_1, d_2, \ldots, d_n)$ biçiminde sıralı bir dizi kabul ederek düşünebiliriz. Çalıştırılan dosyanın indeksi:

$$k = \min\{i \mid d_i/komut \text{ çalıştırılabilir durumdadır}\}$$

Buradaki `min`, neden sıranın kritik olduğunu anlatır: İlk eşleşme kazanır; sonraki dosyalar daha yeni veya daha doğru olsa bile dikkate alınmaz.

\vert  PATH sırası \vert  Seçilen komut \vert  Olası sonuç \vert 
\vert ---\vert ---\vert ---\vert 
\vert  `/usr/local/bin:/usr/bin` \vert  `/usr/local/bin/python` \vert  Elle kurulan sürüm çalışabilir \vert 
\vert  `/usr/bin:/usr/local/bin` \vert  `/usr/bin/python` \vert  Sistem sürümü çalışabilir \vert 
\vert  `./bin:/usr/bin` \vert  Projedeki komut \vert  Projeye özel araç öne geçer \vert 

## Hangi dosyanın çalıştığını bulmak

Bir komutun çözümlendiği ilk yolu görmek için `command -v` kullanılabilir:

```bash
command -v python
command -v git
```

Aynı ada sahip bütün adayları görmek için Bash ve Zsh üzerinde `type -a` oldukça kullanışlıdır:

```bash
type -a python
```

Örneğin çıktı hem `/home/ada/bin/python` hem de `/usr/bin/python` gösteriyorsa terminal yalnızca ilkini çalıştırır. Belirli dosyayı kesin olarak kullanmak istediğinizde tam yol vermek arama mekanizmasını devre dışı bırakır:

```bash
/usr/bin/python --version
```

\vert  Yöntem \vert  PATH araması yapar mı? \vert  Kullanım amacı \vert 
\vert ---\vert ---:\vert ---\vert 
\vert  `python` \vert  Evet \vert  Normal komut çağrısı \vert 
\vert  `/usr/bin/python` \vert  Hayır \vert  Kesin dosyayı çalıştırma \vert 
\vert  `command -v python` \vert  Arama sonucunu gösterir \vert  Tanılama \vert 
\vert  `type -a python` \vert  Tüm eşleşmeleri gösterir \vert  Çakışma inceleme \vert 

## Sırayı bilinçli olarak değiştirmek

Kullanıcıya özel araçları öne almak için dizin listenin başına eklenebilir:

```bash
export PATH="$HOME/bin:$PATH"
```

Bu komut mevcut `PATH` değerini korur, fakat `$HOME/bin` dizinine öncelik verir. Değişikliğin kalıcı olması için satır genellikle `~/.bashrc`, `~/.zshrc` veya kullanılan kabuğun ilgili yapılandırma dosyasına eklenir. Sona eklemek ise sistem araçlarına öncelik tanır:

```bash
export PATH="$PATH:$HOME/bin"
```

Bazı kabuklar daha önce buldukları yolları önbelleğe alabilir. Bir dosyayı taşıdıktan sonra hâlâ eski komut çalışıyorsa Bash üzerinde önbelleği temizlemek mümkündür:

```bash
hash -r
```

## Güvenlik tarafı: Noktaya dikkat

Geçerli dizini temsil eden `.` değerini PATH'in başına koymak risklidir:

```bash
export PATH=".:$PATH"
```

İçinde zararlı bir `ls` dosyası bulunan klasöre girildiğinde gerçek `/bin/ls` yerine bu dosya çalışabilir. Bu nedenle `.` mümkünse PATH'e hiç eklenmemeli; gerekiyorsa yerel program açıkça `./program` şeklinde çağrılmalıdır.

Özetle PATH yalnızca bir dizin listesi değil, bir öncelik sistemidir. Beklenmeyen sürüm çalıştığında önce `command -v`, ardından `type -a` kullanın; sırayı inceleyin ve gerekirse tam dosya yoluyla doğrulama yapın. Terminal gizemli davranmıyordur—yalnızca listeyi soldan sağa okumaktadır.

![path-sirasi-terminal-76](/img/path-sirasi-terminal-76.svg)

