---
layout: post
title: "Nim Dili: Python Sözdizimiyle C Hızı Vaadi Gerçek mi?"
math: true
categories: 
  - Bilgi
tags: 
  - nim
  - python
  - performans
toc: true
---

Nim, ilk bakışta Python’ın derlenmiş ve spor salonuna yazılmış kuzeni gibi görünür: girintili, temiz bir sözdizimi sunar; ancak kodu doğrudan yorumlamak yerine çoğunlukla C’ye çevirip yerel makine koduna derler. Peki “Python rahatlığı, C hızı” sloganı gerçeği mi anlatıyor, yoksa pazarlama departmanının kahvesi biraz fazla mı sertti?

``

## Nim nasıl çalışıyor?

Python’ın yaygın uygulaması CPython, kaynak kodunu bytecode’a dönüştürür ve bu komutları bir sanal makinede yürütür. Dinamik tür denetimi, nesne modeli ve yorumlayıcı maliyeti özellikle yoğun döngülerde performansı sınırlar.

Nim ise statik türlere sahip derlenen bir dildir. Derleyici, Nim kodunu varsayılan olarak C kaynak koduna çevirir; ardından GCC veya Clang gibi bir C derleyicisi çalıştırılır. C++, Objective-C ve JavaScript hedefleri de bulunur. Buradaki önemli nokta şudur: Hızı sağlayan yalnızca “C üretmesi” değil, türlerin derleme anında bilinmesi ve yüksek seviyeli yapıların düşük maliyetli kodlara dönüştürülebilmesidir.

Basitleştirilmiş çalışma maliyetini şöyle düşünebiliriz:

$$T_{toplam} = T_{algoritma} + T_{soyutlama} + T_{çalışma\ zamanı}$$

Nim, statik uzmanlaştırma ve derleme zamanı özellikleri sayesinde son iki terimi küçültmeye çalışır. Fakat kötü bir algoritmayı hiçbir derleyici süper kahramana çeviremez. $O(n^2)$ hâlâ $O(n^2)$’dir.

| Özellik | Python | Nim | C |
|---|---|---|---|
| Tür sistemi | Dinamik | Statik, tür çıkarımlı | Statik |
| Çalıştırma | Genellikle yorumlanan bytecode | Yerel koda derlenir | Yerel koda derlenir |
| Sözdizimi | Çok sade | Python’a oldukça yakın | Daha ayrıntılı |
| Bellek yönetimi | Otomatik | ARC, ORC ve farklı seçenekler | Genellikle manuel |
| Ham performans | Çoğu döngüde düşük | Çoğu senaryoda C’ye yakın | Çok yüksek |

## Sözdizimi gerçekten Python gibi mi?

Girinti tabanlı bloklar, az noktalama işareti ve tür çıkarımı tanıdık hissettirir:

```nim
proc toplamKare(n: int): int =
  var sonuc = 0
  for i in 1..n:
    sonuc += i * i
  return sonuc

echo toplamKare(1_000_000)
```

Bu prosedür, 1’den `n` değerine kadar sayıların karelerini toplar. `sonuc` değişkeninin türü sağ taraftaki sıfırdan çıkarılır; prosedürün giriş ve dönüş türleri ise açıktır. Python’daki benzer kod kadar okunaklı olmasına rağmen döngü, derlenmiş makine kodunda çalışır.

Üretim performansını görmek için kodu doğru seçeneklerle derlemek gerekir:

```bash
nim c -d:release --opt:speed -r hesap.nim
```

`-d:release` hata ayıklama kontrollerinin bir bölümünü kapatır, `--opt:speed` hız optimizasyonlarını seçer ve `-r` oluşan programı çalıştırır. Bu nedenle geliştirme sürümüyle ölçüm yapıp Nim’i yavaş ilan etmek, yarış arabasını el freni çekiliyken test etmeye benzer.

## C kadar hızlı mı?

Kısa cevap: Sıklıkla yaklaşır, bazen eşleşir, her zaman değil. Sayısal döngüler, ayrıştırıcılar, komut satırı araçları ve sistem uygulamalarında C’ye yakın sonuçlar alınabilir. Buna karşılık yoğun bellek tahsisi, metin işlemleri veya uygun olmayan veri yapıları fark oluşturabilir. ARC ve ORC deterministik bellek yönetimini kolaylaştırsa da referans sayımı tamamen ücretsiz değildir.

Ayrıca Python karşılaştırmasının adil yapılması gerekir. Saf CPython döngüsüne karşı Nim büyük fark yaratabilir; NumPy ise kritik işi zaten optimize edilmiş C veya Fortran koduna devreder. Böyle bir durumda karşılaştırma “Nim ve Python” değil, çoğu kez “Nim ve NumPy’nin yerel çekirdeği” olur.

| Senaryo | Beklenen sonuç |
|---|---|
| Saf Python döngüsü | Nim genellikle belirgin biçimde hızlıdır |
| NumPy ile vektörleştirme | Fark azalabilir |
| C ile dikkatle optimize edilmiş kod | Nim yakın olabilir, garanti değildir |
| G/Ç ağırlıklı uygulama | Dil hızından çok disk ve ağ belirleyicidir |

## Son karar

Nim’in vaadi büyük ölçüde tutuyor; fakat doğru ifade “Python’ın aynısı ve otomatik olarak C kadar hızlı” değildir. Daha doğrusu Nim, Python benzeri okunabilirliği statik türler, güçlü metaprogramlama ve yerel derlemeyle birleştirir. Küçük ikili dosyalar, hızlı komut satırı araçları veya sistem seviyesinde kontrol istiyorsanız etkileyici bir seçenektir. Yine de ekosistemi Python ve C kadar geniş değildir; performans için ölçüm, profil çıkarma ve doğru veri yapısı seçimi şarttır. Sonuçta Nim hızlıdır, ama kronometreyi yine sizin tutmanız gerekir.
