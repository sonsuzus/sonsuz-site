---
layout: post
title: "Bir Boşluk, Bütün Disk: rm -rf Komutunun Tehlikeli Anatomisi"
math: true
categories: 
  - Bilgi
tags: 
  - linux
  - shell
  - bash
  - rm-komutu
  - veri-güvenliği
  - devops
toc: true
image: /img/bir-bosluk-butun-16.png
---

Terminalde tek bir boşluğun ne kadar pahalı olabileceğini görmek istiyorsanız, `rm -rf` bunun en ürkütücü örneklerinden biridir. Yanlış yazılmış veya hatalı genişletilmiş bir yol; belgeleri, uygulamaları, yapılandırmaları ve yedekleri saniyeler içinde silebilir. Üstelik komut çoğunlukla “Emin misiniz?” diye sormaz. Klavyedeki minicik bir hata, dijital bir meteor etkisi oluşturabilir.

``

## `rm -rf` gerçekte ne yapar?

`rm`, dosya ve dizinleri kaldırır. `-r` seçeneği dizinlerin içine özyinelemeli olarak girilmesini, `-f` ise uyarıların bastırılıp işlemin zorlanmasını sağlar. Başka bir deyişle komutun mantığı kabaca şöyledir:

$$Silme\ Riski \approx Yetki \times Hedef\ Kapsamı \times Otomasyon\ Hızı$$

Kök kullanıcı yetkisiyle geniş bir hedef seçildiğinde üç çarpan da büyür. Sonuç, geri dönüşüm kutusuna taşınan dosyalar değil; dosya sistemi kayıtlarının doğrudan kaldırılmasıdır.

| İfade | Kabuğun yorumu | Risk |
|---|---|---|
| `rm -rf ./build` | Geçerli dizindeki `build` klasörü | Sınırlı |
| `rm -rf ./build/*` | Klasörün görünür içerikleri | Orta |
| `rm -rf /*` | Kök altındaki girdiler | Felaket |
| `rm -rf /` | Kök dizinin kendisi | Felaket; bazı sistemlerde engellenir |
| `rm -rf / tmp/proje` | İki ayrı hedef: `/` ve `tmp/proje` | Felaket |

Burada önemli bir düzeltme var: `rm -rf /` ile `rm -rf /*` arasındaki fark yalnızca boşluk değildir; yıldız karakteri kabuk tarafından genişletilir. Modern GNU `rm`, `/` hedefini genellikle `--preserve-root` korumasıyla reddeder. Ancak `/*`, kabuk tarafından `/etc`, `/home`, `/usr` gibi ayrı hedeflere dönüştürülebildiğinden bu korumayı aşabilir. Yani iki komut da güvenli değildir.

## Boşluk hatası nasıl felakete dönüşür?

Shell, boşluğu argüman ayırıcı olarak kullanır. Örneğin amaç `/tmp/proje` içeriğini silmekken yanlışlıkla yolun ortasına boşluk eklenirse komut iki farklı hedef algılayabilir. Benzer şekilde boş bir değişken de beklenmeyen bir hedef meydana getirir:

```bash
# TEHLİKELİ ÖRNEK: Değişken boşsa hedef beklenenden farklılaşabilir.
rm -rf "$TARGET"/*
```

`TARGET` boş olduğunda ifade `/*` biçimine yaklaşır. Bu nedenle değişken kullanmadan önce hem doluluk hem de izin verilen kök yol denetlenmelidir.

## Daha güvenli bir silme deseni

Aşağıdaki yaklaşım hedefi doğrular, mutlak yola dönüştürür ve yalnızca belirlenmiş çalışma alanı içindeki dizinlere izin verir:

```bash
#!/usr/bin/env bash
set -euo pipefail

target="${1:-}"
allowed_root="/srv/builds"

if [[ -z "$target" ]]; then
  echo "Hata: Hedef boş olamaz." >&2
  exit 1
fi

resolved="$(realpath -- "$target")"

if [[ "$resolved" != "$allowed_root"/* ]]; then
  echo "Hata: İzin verilen alanın dışında: $resolved" >&2
  exit 1
fi

printf 'Silinecek hedef: %s\n' "$resolved"
rm -rf -- "$resolved"
```

`set -u`, tanımsız değişkenleri hata kabul eder. `realpath`, `..` ve sembolik bağlantı kaynaklı belirsizlikleri azaltır. `--` ise tireyle başlayan bir dosya adının seçenek sanılmasını engeller. Yine de bu kod, yedeklemenin yerini tutmaz.

## Kazayı önlemek için pratik kurallar

1. Komutu çalıştırmadan önce hedefi `printf '%q\n' "$target"` ile görüntüleyin.
2. Önce `ls` veya `find` kullanarak kapsamı inceleyin.
3. Betiklerde `set -euo pipefail` etkinleştirin.
4. Kritik işlemleri root yerine sınırlı yetkili kullanıcıyla yürütün.
5. Snapshot ve çevrimdışı yedek bulundurun; aynı diskteki kopya gerçek yedek değildir.
6. Etkileşimli kullanımda `rm -I` seçeneğini değerlendirin.

Yanlış silme gerçekleşirse sistemi hemen kullanmayı bırakmak, diske yeni veri yazmamak ve profesyonel kurtarma araçlarına yönelmek gerekir. En iyi kurtarma stratejisi ise hâlâ kazadan önce hazırlanmış, düzenli olarak test edilen bir yedektir.

![bir-bosluk-butun-16](/img/bir-bosluk-butun-16.svg)

