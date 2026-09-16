---
layout: post
title: "Ada Neden Havacılık Yazılımlarında Hâlâ İrtifa Kaybetmiyor?"
math: true
categories: 
  - Bilgi
tags: 
  - ada
  - havacılık
  - gömülü-sistemler
  - gerçek-zamanlı-sistemler
  - yazılım-güvenliği
  - aviyonik
toc: true
image: /img/ada-neden-havacilik-47.png
---

Programlama dilleri dünyasında moda hızla değişir; ancak uçuş kontrol bilgisayarı geliştirirken “Bu yıl hangi dil popüler?” diye sorulmaz. Asıl sorular, yazılımın öngörülebilir olup olmadığı ve bir hatanın daha çalıştırılmadan yakalanıp yakalanamayacağıdır. 1980’lerde ABD Savunma Bakanlığının ihtiyaçları doğrultusunda geliştirilen Ada, tam da bu nedenle havacılık, savunma ve demiryolu gibi hata toleransı düşük alanlarda hâlâ güçlü biçimde tercih ediliyor.

![ada-neden-havacilik-47](/img/ada-neden-havacilik-47.svg)

``

## Ada’nın temel tasarım felsefesi

Ada’nın amacı, geliştiriciye mümkün olduğunca fazla özgürlük vermek değil, tehlikeli belirsizlikleri azaltmaktır. Dil; güçlü tip sistemi, açık söz dizimi, çalışma zamanı kontrolleri ve eşzamanlılık desteğiyle hataları erkenden görünür kılar.

Örneğin hız ile irtifa, bilgisayar belleğinde aynı tür sayılar olarak saklanabilir. Buna rağmen fiziksel anlamları farklıdır. Ada, geliştiricinin bu değerler için ayrı türler tanımlamasına izin verir:

```ada
with Ada.Text_IO; use Ada.Text_IO;

procedure Flight_Data is
   type Altitude_Meter is new Float range 0.0 .. 15_000.0;
   type Speed_Knot     is new Float range 0.0 .. 900.0;

   Altitude : Altitude_Meter := 10_000.0;
   Speed    : Speed_Knot     := 450.0;
begin
   Put_Line ("Uçuş verileri geçerli aralıkta.");
   -- Altitude := Speed;  -- Türler farklı olduğu için derleme hatası oluşur.
end Flight_Data;
```

Buradaki yasaklama küçük görünebilir; fakat binlerce değişkenin bulunduğu aviyonik sistemlerde yanlış birim veya yanlış veri ataması ciddi sonuçlar doğurabilir. Ada’nın yaklaşımı, “Programcı ne yaptığını biliyordur” yerine “Niyeti kodda açıkça kanıtlayalım” şeklindedir.

## Gerçek zamanlılık neden önemlidir?

Bir uçuş kontrol komutunun doğru sonucu üretmesi tek başına yeterli değildir; sonucu zamanında üretmesi gerekir. Bir görevin toplam tepki süresini basitçe şöyle ifade edebiliriz:

$$R = C + B + I$$

Burada $C$ işlem süresi, $B$ kaynak bekleme süresi, $I$ ise daha yüksek öncelikli görevlerden kaynaklanan kesintidir. Güvenli bir sistemde hedef, her görev için $R \leq D$ koşulunu sağlamaktır; $D$, görevin son teslim zamanıdır.

Ada’nın görev modeli, zamanlama ve korumalı nesne gibi mekanizmaları doğrudan dil düzeyinde sunar. Bu durum, sonradan eklenen karmaşık kütüphanelere duyulan ihtiyacı azaltır ve sistem davranışının analiz edilmesini kolaylaştırır.

## Ada ile genel amaçlı dillerin karşılaştırması

| Özellik | Ada | C/C++ | Python |
|---|---|---|---|
| Güçlü tür güvenliği | Çok yüksek | Orta | Dinamik |
| Gerçek zamanlı destek | Dil ve çalışma zamanı düzeyinde | İşletim sistemi/kütüphane ağırlıklı | Sınırlı |
| Bellek hatalarını önleme | Güçlü kontroller | Geliştirici sorumluluğu yüksek | Otomatik bellek yönetimi |
| Zaman davranışı | Öngörülebilir tasarlanabilir | İyi, fakat dikkat gerektirir | Genellikle daha az öngörülebilir |
| Sertifikasyon geçmişi | Çok güçlü | Çok güçlü | Sınırlı |

Bu tablo C veya C++’ın havacılıkta kullanılmadığı anlamına gelmez. Aksine ikisi de yaygındır. Ada’nın farkı, güvenli uygulama kurallarını yalnızca ekip disiplinine bırakmak yerine dilin yapısına yerleştirmesidir.

## Sertifikasyon ve SPARK avantajı

Havacılık yazılımları çoğunlukla DO-178C gibi standartlara göre geliştirilir. Bu süreçte gereksinim izlenebilirliği, test kapsamı ve hata analizi kritik öneme sahiptir. Ada’nın belirgin söz dizimi ve sınırlı belirsizliği, kod incelemelerini kolaylaştırır.

Ada’nın doğrulanabilir alt kümesi SPARK ise statik analiz ve biçimsel doğrulama sağlar. Geliştirici; taşma, dizi sınırı ihlali veya istenmeyen veri akışı bulunmadığını matematiksel kanıtlarla gösterebilir. Böylece test, “Hata görmedik” seviyesinden “Belirli hata sınıflarının oluşamayacağını kanıtladık” seviyesine çıkar.

## Peki neden her yerde Ada yok?

Ada ekosistemi web ve mobil dünyası kadar büyük değildir. Uzman geliştirici bulmak zor olabilir; eğitim maliyeti ve mevcut C/C++ altyapıları da geçişi yavaşlatır. Üstelik güvenlik yalnızca dil seçerek kazanılmaz: doğru mimari, titiz test, donanım analizi ve disiplinli süreç yine şarttır.

Yine de milyonlarca uçuş saati boyunca çalışacak bir sistem söz konusu olduğunda popülerlikten çok öngörülebilirlik değerlidir. Ada yaşlı olduğu için değil, tehlikeli sürprizleri azaltma konusunda hâlâ son derece güncel olduğu için irtifasını koruyor.
