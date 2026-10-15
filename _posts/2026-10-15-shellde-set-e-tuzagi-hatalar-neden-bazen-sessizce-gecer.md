---
layout: post
title: "Shell’de set -e Tuzağı: Hatalar Neden Bazen Sessizce Geçer?"
math: true
categories: 
  - Bilgi
tags: 
  - shell
  - bash
  - set-e
  - pipefail
  - linux
  - hata-yönetimi
toc: true
image: /img/shellde-set-e-47.png
---

`set -e` etkinleştirildiğinde bir shell betiğinin ilk hatada duracağını düşünmek oldukça doğaldır. Ne yazık ki Bash’in hata modeli bu kadar basit değildir. Özellikle pipeline, koşul ifadeleri ve alt kabuklar devreye girdiğinde başarısız bir komut sessizce geçebilir; betik de hiçbir şey olmamış gibi yoluna devam edebilir.

``

## `set -e` gerçekte ne yapar?

Unix dünyasında komutlar başarı veya başarısızlık durumlarını bir **çıkış koduyla** bildirir. Genel kural şöyledir:

$$
\text{başarı} \iff exit\_code = 0
$$

$$
\text{hata} \iff exit\_code \neq 0
$$

`set -e`, diğer adıyla `errexit`, belirli koşullar altında sıfırdan farklı kod döndüren komut görüldüğünde shell’i sonlandırır:

```bash
#!/usr/bin/env bash
set -e

mkdir /root/yasak-klasor
echo "Bu satır büyük olasılıkla çalışmaz."
```

Normal bir kullanıcı için `mkdir` başarısız olur ve betik durur. Buradaki kritik ifade ise **belirli koşullar altında** kısmıdır. Bash, hatanın program akışını kontrol etmek amacıyla kullanıldığı bazı yapılarda `errexit` davranışını devre dışı bırakır.

## Pipeline neden tehlikelidir?

Bir pipeline’ın çıkış kodu, varsayılan olarak son komutun çıkış kodudur. Örneğin:

```bash
set -e

olmayan_komut | grep "örnek"
echo "Betik hâlâ çalışıyor olabilir."
```

İlk komut başarısız olsa bile `grep` başarılı sonuçlanırsa pipeline’ın tamamı başarılı kabul edilir. Bunu kabaca şöyle ifade edebiliriz:

$$
status(A \mid B \mid C) = status(C)
$$

Bu davranışı değiştirmek için `pipefail` kullanılmalıdır:

```bash
set -euo pipefail

veri_uret | veriyi_donustur | dosyaya_yaz
```

`pipefail`, pipeline içindeki başarısız komutların durumunu görünür kılar. Böylece `set -e`, hatayı yakalayıp betiği durdurabilir.

| Ayar | Pipeline sonucu | Risk |
|---|---|---|
| Yalnızca `set -e` | Son komutun kodu | Önceki hatalar gizlenebilir |
| `set -e -o pipefail` | Başarısız komutun kodu | Hatalar çoğunlukla yakalanır |
| Açık hata kontrolü | Geliştirici tarafından belirlenir | Daha uzun ama daha anlaşılırdır |

## Hatanın beklenen sayıldığı yerler

Bash, `if`, `while`, `until`, `&&`, `||` ve `!` gibi yapılarda başarısızlığın bilinçli olarak test edildiğini varsayar. Dolayısıyla aşağıdaki kullanım betiği durdurmaz:

```bash
set -e

if grep -q "admin" kullanicilar.txt; then
    echo "Admin bulundu."
else
    echo "Admin bulunamadı."
fi
```

Burada `grep` için `1` çıkış kodu gerçek bir felaket değil, “eşleşme bulunamadı” anlamındadır. Benzer biçimde şu komut da devam eder:

```bash
gecici_islem || echo "İşlem başarısız oldu, devam ediyoruz."
```

Çünkü `||` yapısının amacı zaten başarısızlığı ele almaktır.

## Alt kabuk ve komut ikamesi sürprizleri

Komut ikamesinde `errexit` davranışı Bash sürümüne ve seçeneklere göre şaşırtıcı olabilir:

```bash
set -e
sonuc=$(false; echo "devam")
echo "$sonuc"
```

Bazı bağlamlarda `$(...)` içindeki `false`, alt ortamı durdurmaz. Bash’te daha tutarlı davranış için şu seçenek açılabilir:

```bash
set -euo pipefail
shopt -s inherit_errexit
```

Yine de bunu sihirli bir zırh olarak görmemek gerekir. `-u`, tanımsız değişkenleri hata sayar; `pipefail`, pipeline hatalarını taşır; `inherit_errexit` ise komut ikamelerinde davranışı güçlendirir.

## Daha güvenilir yaklaşım

Kritik işlemleri açıkça kontrol etmek genellikle en okunabilir çözümdür:

```bash
if ! yedek_al; then
    echo "Yedekleme başarısız!" >&2
    exit 1
fi
```

Özetle `set -e`, eksiksiz bir hata yönetim sistemi değil, yardımcı bir güvenlik ağıdır. Sağlam betikler için `set -euo pipefail`, anlamlı hata mesajları, açık `if` kontrolleri ve farklı başarısızlık senaryolarını kapsayan testler birlikte kullanılmalıdır.

![shellde-set-e-47](/img/shellde-set-e-47.svg)

