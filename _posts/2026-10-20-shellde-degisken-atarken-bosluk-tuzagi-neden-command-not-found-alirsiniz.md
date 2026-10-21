---
layout: post
title: "Shell’de Değişken Atarken Boşluk Tuzağı: Neden “Command Not Found” Alırsınız?"
math: true
categories: 
  - Bilgi
tags: 
  - shell
  - bash
  - linux
  - değişkenler
  - terminal
  - hata ayıklama
toc: true
image: /img/shellde-degisken-atarken-43.png
---

Shell’de değişken tanımlamak ilk bakışta son derece kolaydır: bir isim, `=` işareti ve bir değer yazarsınız. Ancak `kullanici = ali` gibi okunaklı görünen masum bir satır, Bash tarafından değişken ataması değil komut çalıştırma girişimi olarak yorumlanır. Sonuçta terminal, `kullanici: command not found` diyerek bizi şaşırtır. Suçlu `=` değil; onun etrafına yerleştirdiğimiz boşluklardır.

``

## Shell satırı nasıl okur?

Bash ve diğer POSIX uyumlu shell’ler, girilen satırı önce boşluklara göre **sözcüklere** ayırır. Normal bir komutta ilk sözcük komut adı, sonraki sözcükler ise argümanlardır:

```bash
cp kaynak.txt hedef.txt
```

Burada shell şu üç parçayı görür:

1. `cp`: Çalıştırılacak komut
2. `kaynak.txt`: Birinci argüman
3. `hedef.txt`: İkinci argüman

Değişken ataması ise özel bir sözdizimine sahiptir. Basitleştirilmiş biçimiyle kuralı şöyle gösterebiliriz:

$$
Atama := İsim=Değer
$$

Kritik nokta, `İsim=Değer` ifadesinin **tek bir sözcük** olmasıdır. `=` çevresine boşluk eklendiğinde bu bütünlük parçalanır.

| Yazım | Shell’in gördüğü | Sonuç |
|---|---|---|
| `renk=mavi` | Tek atama sözcüğü | Değişken oluşturulur |
| `renk =mavi` | `renk` komutu ve `=mavi` argümanı | `renk: command not found` |
| `renk= mavi` | Boş değerli geçici atama ve `mavi` komutu | `mavi: command not found` |
| `renk = mavi` | `renk` komutu, `=` ve `mavi` argümanları | `renk: command not found` |

![shellde-degisken-atarken-43](/img/shellde-degisken-atarken-43.svg)


## Doğru ve yanlış kullanım

Aşağıdaki örnekte ilk satır değişkeni tanımlar, ikinci satır ise değerini ekrana basar:

```bash
mesaj="Merhaba dünya"
echo "$mesaj"
```

Çıktı şöyledir:

```text
Merhaba dünya
```

Değerde boşluk bulunması sorun değildir; değer tırnak içine alınabilir. Yasak olan, atama operatörü gibi görünen `=` işaretinin iki yanında boşluk bırakmaktır.

```bash
# Yanlış: "mesaj" adlı bir komut çalıştırılmaya çalışılır.
mesaj = "Merhaba dünya"

# Doğru: Atamanın tamamı tek sözcüktür.
mesaj="Merhaba dünya"
```

Bunu sözcük sayısıyla da düşünebiliriz. Doğru atamada ayrıştırılan parça sayısı $n=1$ iken, `mesaj = değer` yazımında $n=3$ olur. Shell’in davranışı açısından bu küçük fark, atama ile komut çağrısı arasındaki sınırdır.

## `isim=deger komut` neden çalışıyor?

Shell’de aşağıdaki kullanım da geçerlidir:

```bash
DIL=tr_TR.UTF-8 date
```

Burada `DIL=tr_TR.UTF-8`, yalnızca `date` komutunun ortamına eklenen geçici bir değişkendir. Komut tamamlandığında mevcut shell oturumundaki `DIL` değişkeni kalıcı olarak değiştirilmez. Bu özellik, programları farklı ayarlarla tek seferlik çalıştırmak için kullanışlıdır.

```bash
DEBUG=1 python3 uygulama.py
NODE_ENV=production node server.js
```

Fakat `DIL= tr_TR.UTF-8 date` yazılırsa shell, `DIL` için boş bir değer ayarlayıp `tr_TR.UTF-8` adında bir komut aramaya başlar. Yani boşluğun konumu yorumlamayı tamamen değiştirir.

## Hata ayıklama ipuçları

Bir betik beklenmedik biçimde `command not found` hatası veriyorsa ilgili satırları görünür kılmak için izleme modunu kullanabilirsiniz:

```bash
set -x
kullanici = ali
set +x
```

`set -x`, shell’in çalıştırmaya uğraştığı komutları terminalde gösterir. Ayrıca betikleri `shellcheck betik.sh` komutuyla incelemek, bu tür sözdizimi hatalarını daha çalıştırmadan yakalayabilir.

Kısacası shell dünyasında `=` çevresindeki boşluk estetik bir tercih değildir. `isim=deger` tek ve bölünmez bir atama ifadesidir. Terminal size “komut bulunamadı” diyorsa önce komutun kurulu olup olmadığını değil, yanlışlıkla bir değişken adını komuta dönüştürüp dönüştürmediğinizi kontrol edin.
