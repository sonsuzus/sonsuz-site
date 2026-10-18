---
layout: post
title: "Shell Alias’ları Script İçinde Neden Ortadan Kaybolur?"
math: true
categories: 
  - Bilgi
tags: 
  - shell
  - bash
  - alias
  - linux
  - script
  - terminal
toc: true
image: /img/shell-aliaslari-script-38.png
---

![shell-aliaslari-script-38](/img/shell-aliaslari-script-38.svg)


Terminalde neşeyle çalışan `ll`, `gs` veya `deploy` alias’ınız bir shell scriptine taşındığında aniden tanınmayan komuta dönüşebilir. Bu durum bir hata değil, shell’in etkileşimli kullanım ile otomasyonu bilinçli biçimde ayırmasının sonucudur. Gelin alias’ların neden saklambaç oynadığını ve scriptlerde hangi çözümün daha güvenilir olduğunu inceleyelim.
``
## Etkileşimli shell nedir?

Bir shell, davranışını nasıl başlatıldığına göre belirler. Terminal açıp komut yazdığınız oturum **etkileşimlidir**; shell kullanıcıdan sürekli komut bekler. Bir dosyayı `bash görev.sh` ile çalıştırdığınızda ise çoğunlukla **etkileşimsiz** bir oturum oluşur.

Bash içerisinde bu ayrımı şöyle görebiliriz:

```bash
case $- in
  *i*) echo "Etkileşimli shell" ;;
  *)   echo "Etkileşimsiz shell" ;;
esac
```

`$-` değişkeninde `i` bayrağının bulunması etkileşimli oturumu gösterir. Alias genişletme davranışını basitleştirerek şu mantıksal ifadeyle düşünebiliriz:

$$
A = D \land (I \lor E)
$$

Burada $A$ alias’ın genişletilmesini, $D$ alias’ın tanımlı olmasını, $I$ etkileşimli oturumu ve $E$ ise `expand_aliases` seçeneğinin açık olmasını temsil eder. Yani alias’ın yalnızca tanımlanması her zaman yeterli değildir.

| Özellik | Etkileşimli shell | Script shell’i |
|---|---|---|
| Kullanıcıdan komut bekler | Evet | Hayır |
| `.bashrc` genellikle okunur | Evet | Hayır |
| Alias genişletme | Varsayılan olarak açık | Varsayılan olarak kapalı |
| Otomasyon için uygunluk | Düşük | Yüksek |

## Alias neden bulunamıyor?

Örneğin `.bashrc` dosyanızda şu tanım bulunsun:

```bash
alias selam='echo Merhaba geliştirici!'
```

Terminalde `selam` çalışır. Ancak aşağıdaki script başarısız olabilir:

```bash
#!/usr/bin/env bash
selam
```

İlk neden, etkileşimsiz Bash’in çoğunlukla `.bashrc` dosyasını okumamasıdır. Dolayısıyla alias henüz tanımlanmamıştır. İkinci neden ise alias tanımlansa bile `expand_aliases` seçeneğinin scriptlerde varsayılan olarak kapalı olmasıdır.

Geçici bir çözüm şöyledir:

```bash
#!/usr/bin/env bash
shopt -s expand_aliases
alias selam='echo Merhaba geliştirici!'
selam
```

`shopt -s expand_aliases`, Bash’e etkileşimsiz ortamda da alias genişletmesini söyler. Tanımları ayrı bir dosyada tutuyorsanız dosyayı açıkça yükleyebilirsiniz:

```bash
#!/usr/bin/env bash
shopt -s expand_aliases
source "$HOME/.bash_aliases"
selam
```

Bununla birlikte `.bashrc` dosyasını bütünüyle `source` etmek risklidir. Dosyada yalnızca terminale uygun `stty`, `bind` veya çıktı üreten komutlar bulunabilir. Otomasyon kodu böyle sürprizlerden pek hoşlanmaz.

## Daha sağlam çözüm: fonksiyonlar

Scriptlerde alias yerine shell fonksiyonu kullanmak genellikle daha güvenlidir:

```bash
selam() {
  local isim=${1:-geliştirici}
  printf 'Merhaba %s!\n' "$isim"
}

selam "Ada"
```

Fonksiyonlar parametre alabilir, yerel değişken kullanabilir ve normal shell sözdizimiyle çalışır. Alias ise esas olarak komut satırında kısa yol oluşturmak için yapılan metinsel bir değiştirmedir.

| Yaklaşım | Parametre desteği | Script güvenilirliği | Önerilen kullanım |
|---|---:|---:|---|
| Alias | Sınırlı | Düşük | Terminal kısayolları |
| Fonksiyon | Güçlü | Yüksek | Tekrarlanan shell işlemleri |
| Ayrı script | Güçlü | Çok yüksek | Paylaşılan otomasyon |

## Shell farkını unutmayın

`#!/bin/sh` ile başlayan bir scriptin Bash özelliklerini desteklemesi garanti değildir. `shopt` Bash’e özgüdür; Dash veya başka bir POSIX shell altında çalışmayabilir. Bash özellikleri kullanıyorsanız shebang satırını açıkça `#!/usr/bin/env bash` yapın.

Kısacası alias’lar terminal konforu içindir, otomasyon sözleşmesi değildir. Script içinde zorunlu olarak kullanacaksanız tanımı yükleyip `expand_aliases` seçeneğini açın; uzun vadede ise fonksiyon veya bağımsız çalıştırılabilir dosya tercih edin. Böylece alias’ınız üretim ortamında görünmezlik pelerinini kuşanamaz.
