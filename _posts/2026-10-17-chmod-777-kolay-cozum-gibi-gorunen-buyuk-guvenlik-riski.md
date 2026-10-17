---
layout: post
title: "chmod 777: Kolay Çözüm Gibi Görünen Büyük Güvenlik Riski"
math: true
categories: 
  - Bilgi
tags: 
  - linux
  - shell
  - chmod
  - dosya-izinleri
  - siber-güvenlik
  - devops
toc: true
image: /img/chmod-777-kolay-72.png
---

Linux üzerinde bir dosya çalışmadığında veya uygulama erişim hatası verdiğinde internette sıkça şu öneriyle karşılaşırız: `chmod 777 dosya`. Komut sorunu saniyeler içinde çözebilir; ancak bunu yapmak, kilidi açmak yerine kapıyı tamamen sökmeye benzer. Gelin `777` sayısının arkasındaki mantığı ve neden üretim sistemlerinde ciddi bir güvenlik riski oluşturduğunu inceleyelim.

``

## Linux izinlerinin temel mantığı

Linux, her dosya ve dizin için izinleri üç kullanıcı sınıfında değerlendirir:

- **Sahip (user):** Dosyanın sahibi olan kullanıcı.
- **Grup (group):** Dosyanın bağlı olduğu gruptaki kullanıcılar.
- **Diğerleri (others):** Geriye kalan herkes.

Her sınıfa okuma, yazma ve çalıştırma yetkileri atanabilir. Sayısal gösterimde bu izinlerin değerleri şöyledir:

| İzin | Sembol | Sayısal değer | Dosyada anlamı |
|---|---:|---:|---|
| Okuma | `r` | 4 | İçeriği görüntüleyebilme |
| Yazma | `w` | 2 | İçeriği değiştirebilme |
| Çalıştırma | `x` | 1 | Dosyayı program olarak çalıştırabilme |

![chmod-777-kolay-72](/img/chmod-777-kolay-72.svg)


Bir sınıfa ait izin sayısı şu formülle düşünülebilir:

$$P = 4r + 2w + x$$

Burada izin varsa değişkenin değeri $1$, yoksa $0$ olur. Okuma, yazma ve çalıştırma izinlerinin tamamı için sonuç $4+2+1=7$ çıkar. Dolayısıyla `777`, sahip, grup ve diğer kullanıcıların tamamına bütün yetkileri verir:

```bash
chmod 777 uygulama.sh
ls -l uygulama.sh
# -rwxrwxrwx ... uygulama.sh
```

Bu çıktıda üç ayrı `rwx` grubu bulunması, sistemdeki herkesin dosyayı okuyabileceği, değiştirebileceği ve çalıştırabileceği anlamına gelir.

## Neden tehlikelidir?

Bir betiğin herkes tarafından değiştirilebildiğini düşünün. Saldırgan, betiğe zararlı bir komut ekleyebilir. Betik daha sonra yetkili bir kullanıcı veya zamanlanmış görev tarafından çalıştırılırsa saldırganın kodu da çalışır. Böylece sıradan bir izin hatası, yetki yükseltme zincirinin ilk halkasına dönüşebilir.

Dizinlerde risk daha da şaşırtıcıdır. Bir dizindeki `w` izni, kullanıcının dosya oluşturmasına veya uygun koşullarda dosyaları silmesine olanak tanır. Web sunucusunun herkese yazılabilir yükleme dizini, zararlı betiklerin sisteme bırakılması için davetiye çıkarabilir.

| İzin | Kullanım yaklaşımı | Risk düzeyi |
|---|---|---|
| `777` | Herkese tam yetki | Çok yüksek |
| `755` | Sahip yazar, diğerleri okur ve çalıştırır | Genellikle uygun |
| `750` | Yalnızca sahip ve grup erişir | Daha kısıtlı |
| `644` | Sahip yazar, diğerleri yalnızca okur | Normal dosyalar için yaygın |
| `600` | Yalnızca sahip okur ve yazar | Gizli dosyalar için uygun |

## Daha güvenli çözüm nasıl bulunur?

Önce hatayı hangi kullanıcının aldığını ve gerçekten hangi izne ihtiyaç duyduğunu belirleyin:

```bash
whoami
ls -l config.yml
namei -l /opt/uygulama/config.yml
```

`whoami` mevcut kullanıcıyı, `ls -l` dosyanın sahibini ve izinlerini gösterir. `namei -l` ise yol üzerindeki dizinlerin izinlerini tek tek inceleyerek erişimin nerede kesildiğini bulmaya yardımcı olur.

Dosya yanlış kullanıcıya aitse herkese izin vermek yerine sahipliği düzeltmek daha doğrudur:

```bash
sudo chown uygulama:web config.yml
chmod 640 config.yml
```

Bu örnekte dosya sahibi okuyup yazabilir, `web` grubu yalnızca okuyabilir, diğer kullanıcılar ise erişemez. Çalıştırılabilir bir betik için genellikle şu yaklaşım yeterlidir:

```bash
chmod 750 deploy.sh
```

Ayrıca servis kullanıcısını uygun gruba eklemek, ACL kullanmak veya uygulamanın çalışma dizinini düzeltmek düşünülebilir. Temel ilke **en az ayrıcalık** yaklaşımıdır: Bir kullanıcıya görevini tamamlamak için gereken en düşük izin verilmelidir.

Kısacası `chmod 777`, izin sorununu çözmekten çok görünmez hâle getirir. Bir komutun çalışması sistemin güvenli olduğu anlamına gelmez. Kilidi kırmak yerine doğru kişiye doğru anahtarı vermek, Linux güvenliğinin en sade ve en etkili kuralıdır.
