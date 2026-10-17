---
layout: post
title: "Shell Pipe Zincirlerinde Sessiz Hataları Yakalamak: pipefail Neden Hayati?"
math: true
categories: 
  - Bilgi
tags: 
  - shell
  - bash
  - pipefail
  - linux
  - hata-yönetimi
  - devops
toc: true
image: /img/shell-pipe-zincirlerinde-32.png
---

Shell pipe operatörü `|`, bir komutun çıktısını diğerinin girdisine bağlayarak güçlü ve okunabilir iş akışları kurmamızı sağlar. Ne var ki zincirin ortasındaki bir komut başarısız olduğunda son komut başarılıysa bütün işlem başarılı görünür. İşte `set -o pipefail`, bu sessiz sabotajcıyı görünür hâle getiren küçük ama kritik bir Bash ayarıdır.


![shell-pipe-zincirlerinde-32](/img/shell-pipe-zincirlerinde-32.svg)

``

## Pipe zincirinin varsayılan davranışı

Aşağıdaki zinciri düşünelim:

```bash
üretici | dönüştürücü | kaydedici
```

Her komut ayrı bir çıkış kodu üretir. Unix dünyasında `0` başarıyı, sıfırdan farklı değerler ise hata veya özel bir durumu ifade eder. Buna rağmen Bash, varsayılan olarak bütün zincirin çıkış kodunu yalnızca **son komutun** çıkış koduna eşitler.

Matematiksel olarak komutların çıkış kodları $s_1, s_2, \ldots, s_n$ ise varsayılan davranış şöyledir:

$$
s_{pipeline} = s_n
$$

Örneğin:

```bash
cat bulunmayan-dosya.txt | grep "ERROR" | sort > hatalar.txt
echo $?
```

`cat` dosyayı bulamadığı için başarısız olur. Ancak `sort`, kendisine ulaşan boş girdiyi sorunsuzca işleyebilir ve `0` döndürür. Sonuç: zincir başarılı görünür, `hatalar.txt` oluşturulur ve otomasyon sistemi keyifle yanlış rapor verir.

\vert  Durum \vert  Varsayılan pipe \vert  `pipefail` etkin \vert 
\vert ---\vert ---:\vert ---:\vert 
\vert  İlk komut başarısız, son komut başarılı \vert  Başarılı \vert  Başarısız \vert 
\vert  Ara komut başarısız \vert  Genellikle başarılı görünür \vert  Başarısız \vert 
\vert  Tüm komutlar başarılı \vert  Başarılı \vert  Başarılı \vert 
\vert  Birden fazla komut başarısız \vert  Son komut belirler \vert  Sağdaki başarısız komut belirler \vert 

## pipefail neyi değiştirir?

Ayarı etkinleştirmek oldukça kolaydır:

```bash
set -o pipefail

cat bulunmayan-dosya.txt \vert  grep "ERROR" \vert  sort > hatalar.txt
echo $?
```

`pipefail` etkinken zincirin çıkış kodu, başarısız olan komutlar arasından **en sağdakinin** sıfır olmayan çıkış kodudur. Bütün komutlar başarılıysa sonuç yine `0` olur:

$$
s_{pipeline} =
\begin{cases}
0, & \text{tüm komutlar başarılıysa} \\
 s_k, & \text{sağdaki son başarısız komut } k \text{ ise}
\end{cases}
$$

Bu özellik özellikle yedekleme, dağıtım ve veri dönüştürme betiklerinde önemlidir. Örneğin `mysqldump | gzip > backup.gz` zincirinde veritabanı aktarımı başarısız olsa bile `gzip` boş veriyi sıkıştırıp başarı döndürebilir. Elinizde teknik olarak geçerli, pratikte tamamen işe yaramaz bir arşiv kalır.

## Güvenli betik başlangıcı

Bash betiklerinde sık kullanılan koruyucu kombinasyon şöyledir:

```bash
#!/usr/bin/env bash
set -Eeuo pipefail

mysqldump uygulama | gzip > uygulama.sql.gz
```

| Seçenek | Görevi |
|---|---|
| `-e` | Yakalanmamış bir hata oluştuğunda betiği durdurur |
| `-u` | Tanımsız değişken kullanımını hata sayar |
| `-o pipefail` | Pipe içindeki hataları zincire yansıtır |
| `-E` | `ERR` tuzağının fonksiyonlarda miras alınmasına yardım eder |

Yine de `set -e` sihirli bir güvenlik kemeri değildir; `if`, `while`, `&&` ve `||` gibi yapılarda özel kuralları vardır. Beklenen başarısızlıkları açıkça yönetmek daha güvenlidir:

```bash
if ! grep "ERROR" uygulama.log | sort > kritik.log; then
    echo "Log işleme zinciri başarısız oldu" >&2
    exit 1
fi
```

## Hangi komut çöktü?

Bash, son pipe zincirindeki komutların durumlarını `PIPESTATUS` dizisinde saklar:

```bash
komut1 | komut2 | komut3
statuslar=("${PIPESTATUS[@]}")
printf 'Çıkış kodları: %s\n' "${statuslar[*]}"
```

Bu değerleri zincirden hemen sonra kopyalamak gerekir; araya giren başka bir komut `PIPESTATUS` içeriğini değiştirir. Ayrıca `grep` için `1`, teknik arızadan ziyade “eşleşme bulunamadı” anlamına gelebilir. Dolayısıyla her sıfır olmayan kodu aynı şekilde yorumlamak yerine kullanılan komutun sözleşmesini bilmek gerekir.

Kısacası pipe zinciri bir ekip çalışmasıdır; yalnızca son çalışanın raporuna bakmak yeterli değildir. `set -o pipefail`, ortadaki çalışanın masayı devirip sessizce uzaklaşmasını engeller.
