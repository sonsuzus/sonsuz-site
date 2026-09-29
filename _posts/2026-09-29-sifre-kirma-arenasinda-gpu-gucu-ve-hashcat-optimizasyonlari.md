---
layout: post
title: "Şifre Kırma Arenasında GPU Gücü ve Hashcat Optimizasyonları"
math: true
categories: 
  - Bilgi
tags: 
  - hashcat
  - gpu
  - parola güvenliği
  - siber güvenlik
  - maskeleme saldırısı
  - hash
toc: true
image: /img/sifre-kirma-arenasinda-73.png
---

![sifre-kirma-arenasinda-73](/img/sifre-kirma-arenasinda-73.svg)


Modern ekran kartları yalnızca oyunlardaki ejderhaları gerçekçi göstermek için çalışmıyor; binlerce paralel çekirdeği sayesinde parola denetimlerinde de ciddi hesaplama gücü sunuyor. Hashcat, bu gücü kullanarak hash karşılaştırmalarını büyük ölçekte gerçekleştiriyor. Bu yazıdaki örnekler yalnızca size ait sistemlerde veya açıkça izin verilmiş güvenlik testlerinde kullanılmalıdır.
``

## GPU neden bu kadar hızlı?

CPU çekirdekleri karmaşık ve birbirinden farklı görevleri hızla yürütmek üzere tasarlanır. GPU ise aynı matematiksel işlemi çok sayıda veri üzerinde eş zamanlı uygulamakta ustadır. Bir parola adayının hash değerini hesaplamak da çoğunlukla bu modele uygundur: Adaylar birbirinden bağımsız biçimde işlenebilir.

Bir sistem saniyede $R$ aday deneyebiliyor ve toplam anahtar uzayı $N$ aday içeriyorsa kaba kuvvet saldırısının yaklaşık tamamlanma süresi:

$$T = \frac{N}{R}$$

Ortalama bulunma süresi ise adayların eşit olasılıklı olduğu varsayımıyla yaklaşık $T/2$ olur. Sekiz karakterli, yalnızca küçük harflerden oluşan bir parola için uzay $26^8$ iken karakter kümesine büyük harf ve rakam eklenmesiyle bu değer $62^8$ olur. Küçük görünen tercihlerin maliyeti üstel biçimde büyütmesi işte bu yüzden önemlidir.

| Özellik | CPU | GPU |
|---|---|---|
| Çekirdek yapısı | Az sayıda, güçlü | Binlerce, daha basit |
| Paralel hash hesabı | Sınırlı | Çok yüksek |
| Dallanan algoritmalar | Daha başarılı | Verim kaybedebilir |
| Güç ve ısı | Genellikle daha düşük | Yoğun yükte yüksek |
| Uygun senaryo | Karmaşık genel görevler | Tekrarlanan paralel işlemler |

## Her hash aynı kolaylıkta değildir

MD5, SHA-1 ve NTLM gibi hızlı algoritmalar GPU üzerinde çok yüksek deneme hızlarına ulaşabilir. Bu özellik dosya doğrulamada yararlı olsa da parola saklamak için tehlikelidir. bcrypt, scrypt ve Argon2 gibi parola türetme algoritmaları ise hesaplama maliyetini artırır; özellikle scrypt ve Argon2 bellek kullanımını da yükselterek GPU paralelliğini sınırlar.

| Algoritma türü | Tasarım hedefi | GPU karşısındaki durum |
|---|---|---|
| MD5 / SHA-1 | Hızlı özet üretmek | Parolalar için zayıf |
| bcrypt | Ayarlanabilir işlem maliyeti | Daha yavaş deneme |
| scrypt | İşlem ve bellek maliyeti | Paralelliği zorlaştırır |
| Argon2id | Modern parola saklama | Genellikle güçlü tercih |

Salt kullanımı da aynı parolaların aynı hash değerini üretmesini engeller ve önceden hazırlanmış tabloların etkisini azaltır. Ancak salt, zayıf bir parolayı tek başına güçlü hâle getirmez.

## Maskeleme saldırısının mantığı

Kaba kuvvet her konumu bütün karakterlerle denerken maskeleme saldırısı bilinen biçimlerden yararlanır. Örneğin kurum testinde parolaların “bir büyük harf, üç küçük harf ve iki rakam” düzenini izlediği gözlemlenmişse anahtar uzayı:

$$N = 26 \times 26^3 \times 10^2$$

olur. Bu, altı konumda tüm karakterleri denemekten çok daha küçüktür. Verim artarken sadece maskeye uymayan parolaların bulunamayacağı unutulmamalıdır.

İzinli bir laboratuvarda donanımı tanımak için önce yerleşik benchmark çalıştırılabilir:

```bash
hashcat -b
```

Bu komut farklı hash modlarında yaklaşık performansı ölçer; gerçek saldırı sonucu üretmez. OpenCL veya CUDA aygıtlarını listelemek için:

```bash
hashcat -I
```

Test amacıyla hazırlanmış bir hash dosyasında örnek maske kullanımı şöyledir:

```bash
hashcat -m 0 -a 3 test-hashes.txt '?u?l?l?l?d?d'
```

Burada `-m 0` MD5 modunu, `-a 3` maske saldırısını belirtir. `?u`, `?l` ve `?d` sırasıyla büyük harf, küçük harf ve rakam konumlarıdır.

## Güvenli optimizasyon yaklaşımı

`-O` seçeneği optimize çekirdekleri etkinleştirebilir; ancak desteklenen parola uzunluğunu sınırlayabilir. `-w` iş yükü profili performans ile masaüstü tepkiselliği arasındaki dengeyi değiştirir. En yüksek değeri körlemesine seçmek yerine sıcaklık, güç tüketimi ve sürücü kararlılığı izlenmelidir. Dar ve gerçekçi maskeler, doğru hash modu ve güncel sürücüler genellikle rastgele ayarlardan daha değerlidir.

Savunma tarafındaki sonuç nettir: Uzun ve benzersiz parolalar, parola yöneticileri, çok faktörlü kimlik doğrulama ve doğru ayarlanmış Argon2id gibi algoritmalar GPU’nun milyarlarca denemelik kas gücünü pahalı ve verimsiz hâle getirir.
