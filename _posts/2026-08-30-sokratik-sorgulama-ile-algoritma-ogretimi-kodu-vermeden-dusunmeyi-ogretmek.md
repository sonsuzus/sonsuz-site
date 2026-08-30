---
layout: post
title: "Sokratik Sorgulama ile Algoritma Öğretimi: Kodu Vermeden Düşünmeyi Öğretmek"
math: true
categories: 
  - Bilgi
tags: 
  - algoritma
  - eğitim
  - sokratik-sorgulama
toc: true
---

Bir öğrenciye çalışan kodu doğrudan vermek, kısa vadede alkış aldırır; fakat uzun vadede onu hata mesajı karşısında yalnız bırakabilir. Algoritma öğretiminin asıl amacı `for` döngüsünü ezberletmek değil, problemi parçalara ayırma, varsayım kurma ve çözümü sınama alışkanlığı kazandırmaktır. Sokratik sorgulama tam burada devreye girer: Eğitmen cevap makinesi olmaz; öğrencinin kendi cevabına ulaşmasını sağlayan, dikkatle tasarlanmış sorular sorar.
``

## Neden soru sormak kod vermekten güçlüdür?

Sokratik yaklaşımın temelinde bilişsel çatışma vardır. Öğrenci ilk fikrini söyler, eğitmen bu fikrin sınırlarını görünür kılan bir soru yöneltir ve öğrenci modelini günceller. Bu süreç, algoritmik düşünmenin çekirdeği olan **girdi–işlem–çıktı** zincirini somutlaştırır.

Örneğin amaç bir listedeki en büyük sayıyı bulmak olsun. Eğitmen “Hangi fonksiyonu kullanırız?” diye sorarsa öğrenci kütüphane adı arar. Bunun yerine “Listenin tamamına bakmadan en büyüğü bildiğini nasıl iddia edebilirsin?” sorusu, tarama gereksinimini öğrenciye keşfettirir. Ardından “Şu ana kadar gördüklerin içinden en büyüğü nerede saklayacağız?” sorusu, değişken kavramına doğal bir köprü kurar.

| Doğrudan öğretim refleksi | Sokratik eğitmen refleksi | Kazanım |
|---|---|---|
| “`max()` kullan.” | “Hazır fonksiyon olmasaydı ne yapardın?” | Algoritma tasarımı |
| “Döngü burada yanlış.” | “Bu döngü son elemana ulaşıyor mu?” | Sınır analizi |
| “Koşulu `>=` yap.” | “Eşit değer geldiğinde hangi sonucu bekliyoruz?” | Gereksinim netleştirme |
| “Kodunu böyle düzelt.” | “Bu varsayımı çürütecek bir test üretir misin?” | Hata ayıklama |

## Soruların bir algoritması vardır

Rastgele soru sormak yerine, eğitmen de bir akış izlemelidir. Önce problemi öğrencinin kendi cümlesiyle yeniden anlatmasını isteyin. Sonra örnek girdiler, uç durumlar ve başarı ölçütleri üzerinden ilerleyin. En son çözümün doğruluğunu sorgulatın.

Bir algoritmanın maliyetini konuşurken de cevap yerine karşılaştırma sunun. Öğrenci her elemanı bir kez geziyorsa işlem sayısı yaklaşık $n$ olur; iç içe iki tam tarama varsa yaklaşık $n \times n = n^2$ işlem gerçekleşir. Böylece Big-O, ezberlenecek bir etiket değil, yapılan işin büyüme hikâyesi hâline gelir.

| Soru aşaması | Örnek eğitmen sorusu | Öğrencinin hedeflediği düşünme |
|---|---|---|
| Anlama | “Girdi ve beklenen çıktı tam olarak nedir?” | Problemi modelleme |
| Parçalama | “Tekrar eden küçük iş hangisi?” | Alt problem bulma |
| Tasarlama | “Her adımda hangi bilgi korunmalı?” | Değişmez tanımlama |
| Sınama | “Boş liste gelirse ne olur?” | Uç durum yönetimi |
| Gerekçelendirme | “Neden hiçbir elemanı atlamıyoruz?” | Doğruluk kanıtı |

## Örnek diyalog: en büyük elemanı bulmak

Öğrenci “Bir değişken açıp sayıları karşılaştırırım” dediğinde eğitmen hemen kod yazdırmamalıdır. “Bu değişken başlangıçta hangi değeri taşımalı?”, “Negatif sayıların hepsi gelirse sıfırla başlamak güvenli mi?” ve “Döngü bittiğinde bu değişken hakkında neyi garanti edebilirsin?” soruları, doğru başlangıç ve değişmez fikrini doğurur.

Öğrencinin ulaştığı çözüm şu olabilir:

```python
def en_buyuk(sayilar):
    if not sayilar:
        return None

    en_buyuk_deger = sayilar[0]
    for sayi in sayilar[1:]:
        if sayi > en_buyuk_deger:
            en_buyuk_deger = sayi
    return en_buyuk_deger
```

Bu kodun kritik noktası yalnızca `if` koşulu değildir. Döngünün her turundan sonra şu değişmez korunur: `en_buyuk_deger`, o ana kadar incelenen elemanların en büyüğüdür. Eğitmen öğrenciden bu cümleyi kurmasını isterse, kod satırları anlam kazanır. Algoritma $O(n)$ zamanda çalışır; çünkü her eleman en fazla bir kez karşılaştırılır.

Son olarak, sessizliği hata sanmayın. Öğrenci düşündüğünde birkaç saniye beklemek, ona cevap yetiştirmekten daha öğreticidir. İyi Sokratik eğitmen çözümü gizleyen kişi değil; öğrencinin çözümü görebileceği doğru pencereyi açan kişidir.
