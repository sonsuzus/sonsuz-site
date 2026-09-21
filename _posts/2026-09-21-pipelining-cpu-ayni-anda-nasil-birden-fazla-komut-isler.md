---
layout: post
title: "Pipelining: CPU Aynı Anda Nasıl Birden Fazla Komut İşler?"
math: true
categories: 
  - Bilgi
tags: 
  - pipelining
  - cpu
  - işlemci-mimarisi
  - performans
  - assembly
  - bilgisayar-bilimi
toc: true
---

Bir CPU’nun aynı anda birden fazla komut çalıştırdığını duyduğumuzda, işlemcinin düzinelerce eli olan bir robot gibi davrandığını düşünebiliriz. Gerçekteyse pipelining, tek bir işi parçalara ayırıp farklı komutların farklı parçalarını eş zamanlı yürütme tekniğidir. Bir otomobil fabrikasında bir araç boyanırken diğerinin motorunun takılması gibi, işlemci de bir komutu çözerken sıradaki komutu bellekten getirebilir.

``

## Komutlar hangi aşamalardan geçer?

Basitleştirilmiş bir işlemci hattı genellikle beş aşamadan oluşur:

1. **IF — Instruction Fetch:** Komut bellekten getirilir.
2. **ID — Instruction Decode:** Komut çözülür ve gerekli register’lar okunur.
3. **EX — Execute:** Aritmetik işlem veya adres hesabı yapılır.
4. **MEM — Memory Access:** Gerekiyorsa belleğe erişilir.
5. **WB — Write Back:** Sonuç register’a yazılır.

Pipelining olmayan bir CPU, bir komutun beş aşamasını bitirmeden yenisine başlamaz. Boru hatlı CPU ise her saat çevriminde yeni bir komutu hatta sokabilir.

| Saat çevrimi | Komut 1 | Komut 2 | Komut 3 |
|---|---|---|---|
| 1 | IF | - | - |
| 2 | ID | IF | - |
| 3 | EX | ID | IF |
| 4 | MEM | EX | ID |
| 5 | WB | MEM | EX |
| 6 | - | WB | MEM |
| 7 | - | - | WB |

Tabloda üç komut gerçekten tek bir anda tamamlanmaz; aynı anda farklı aşamalarda bulunur. Hat dolduktan sonra ideal durumda her çevrimde bir komut tamamlanır.

## Hız nereden geliyor?

Her komutun gecikmesi mutlaka azalmaz. Hatta aşamalar arasındaki kayıtlar nedeniyle biraz artabilir. Asıl kazanç, birim zamanda tamamlanan komut sayısı olan **throughput** değerindedir.

Pipelining olmadan yaklaşık çalışma süresi:

$$T_{normal} = n \times k \times t$$

İdeal bir pipeline için:

$$T_{pipeline} = (k + n - 1) \times t$$

Burada $n$ komut sayısı, $k$ aşama sayısı, $t$ ise bir aşamanın süresidir. Çok sayıda komut için teorik hızlanma $k$ değerine yaklaşır. Beş aşamalı bir hat teoride yaklaşık beş kat throughput sağlayabilir; fakat gerçek dünya küçük sürprizlerle doludur.

## Pipeline hazard: Boruya çomak sokan durumlar

Pipeline’ın akışını bozan sorunlara **hazard** denir.

| Hazard türü | Neden oluşur? | Yaygın çözüm |
|---|---|---|
| Veri hazard’ı | Bir komut öncekinin sonucunu bekler | Forwarding veya stall |
| Kontrol hazard’ı | Dallanmanın yönü henüz bilinmez | Branch prediction |
| Yapısal hazard | İki aşama aynı donanımı ister | Kaynakları çoğaltmak |

Şu assembly örneğine bakalım:

```asm
ADD R1, R2, R3   ; R1 = R2 + R3
SUB R4, R1, R5   ; Yeni R1 değerine hemen ihtiyaç duyar
```

`SUB`, `ADD` komutunun sonucunu beklemek zorundadır. CPU hiçbir önlem almazsa yanlış değeri okuyabilir. **Stall**, hattı birkaç çevrim durdurup araya baloncuk ekler. **Forwarding** ise sonucu register’a yazılmasını beklemeden doğrudan sonraki aşamaya iletir. Böylece trafik ışığında beklemek yerine kestirme bir yol kullanılır.

## Dallanma tahmini neden önemlidir?

`if`, `switch` ve döngüler makine kodunda dallanma komutlarına dönüşür. CPU, koşulun sonucunu beklerse pipeline boş kalabilir. Bu yüzden modern işlemciler dalın hangi yöne gideceğini tahmin eder ve komutları spekülatif olarak yürütür.

Tahmin doğruysa zaman kazanılır. Yanlışsa hatta alınmış komutlar iptal edilir ve doğru adresten yeniden başlanır. Buna **pipeline flush** denir. Özellikle derin pipeline’larda yanlış tahminin cezası yüksektir.

## Pipelining ile paralellik aynı şey mi?

Tam olarak değil. Pipelining, komutların farklı aşamalarını örtüştürür. Çok çekirdeklilik ise ayrı çekirdeklerde gerçekten farklı komut akışları çalıştırır. Superscalar işlemciler buna bir katman daha ekleyerek aynı çevrimde birden fazla komutu farklı yürütme birimlerine gönderebilir.

Kısacası pipelining, CPU’nun zamanı daha verimli kullanmasını sağlar. İşlemci tek bir komutu sihirli biçimde anında bitirmez; üretim bandını sürekli dolu tutarak toplam performansı yükseltir. Modern CPU hızının ardındaki en önemli numaralardan biri, işte bu düzenli ve son derece hızlı komut koreografisidir.
