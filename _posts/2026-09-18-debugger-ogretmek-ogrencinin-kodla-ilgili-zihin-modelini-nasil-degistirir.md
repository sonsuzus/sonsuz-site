---
layout: post
title: "Debugger Öğretmek Öğrencinin Kodla İlgili Zihin Modelini Nasıl Değiştirir?"
math: true
categories: 
  - Bilgi
tags: 
  - debugger
  - hata ayıklama
  - programlama eğitimi
  - zihin modeli
  - öğrenme
  - yazılım geliştirme
toc: true
image: /img/debugger-ogretmek-ogrencinin-15.png
---

Programlamaya yeni başlayan bir öğrenci için kod çoğu zaman gizemli bir kutudur: Metin yazılır, “Çalıştır” düğmesine basılır ve ekranda ya doğru sonuç ya da kırmızı bir hata belirir. Debugger kullanmayı öğrenmek bu kutunun kapağını açar. Öğrenci yalnızca hatayı bulmayı değil, programın zaman içinde nasıl ilerlediğini, değişkenlerin nasıl dönüştüğünü ve bilgisayarın kodu hangi sırayla yorumladığını görmeye başlar.

``

## Zihin modeli nedir?

Zihin modeli, kişinin bir sistemin nasıl çalıştığına ilişkin içsel açıklamasıdır. Öğrenci `x = x + 1` satırını matematikteki eşitlik gibi yorumluyorsa zihin modeli henüz programlama modelinden uzaktır. Çünkü burada anlatılan şey eşitlik değil, mevcut değerin okunup artırılarak yeniden atanmasıdır.

Bir programın durumunu kabaca şöyle gösterebiliriz:

$$S_t = \{v_1, v_2, \ldots, v_n\}$$

Burada $S_t$, programın $t$ anındaki durumunu; $v_i$ ise değişkenleri, çağrı yığınını ve ilgili çalışma zamanı bilgilerini temsil eder. Bir komut çalıştığında durum değişir:

$$S_{t+1} = f(S_t, I_t)$$

Debugger, normalde görünmeyen bu geçişi gözlemlenebilir hâle getirir. Böylece öğrenci programı “bir sonuç üreten metin” olarak değil, durumları adım adım değişen dinamik bir süreç olarak düşünür.

## `print` ile debugger arasındaki fark

`print` kullanmak yanlış değildir; hatta oldukça değerlidir. Ancak debugger daha sistematik bir gözlem ortamı sunar.

| Yaklaşım | Öğrencinin gördüğü | Geliştirdiği alışkanlık | Sınırlılık |
|---|---|---|---|
| `print` eklemek | Seçilmiş birkaç değer | Hızlı hipotez kontrolü | Çıktılar kodu kalabalıklaştırabilir |
| Debugger kullanmak | Anlık değişkenler, akış ve çağrı yığını | Adım adım nedensel düşünme | Başlangıçta arayüz karmaşık gelebilir |
| Hata mesajını okumak | Hata türü ve konumu | Tanı koyma | Hatanın kök nedenini göstermeyebilir |
| Kodu tahmin ederek değiştirmek | Yalnızca yeni sonuç | Deneme-yanılma | Yanlış zihin modellerini güçlendirebilir |

Debugger’ın asıl katkısı, öğrenciyi “Neyi değiştirsem çalışır?” sorusundan “Programın gerçek durumu, beklediğim durumdan ilk kez nerede ayrılıyor?” sorusuna taşımaktır.

## Küçük bir örnek

Aşağıdaki fonksiyonun sayıların ortalamasını hesaplaması amaçlanıyor:

```python
def ortalama(sayilar):
    toplam = 0

    for sayi in sayilar:
        toplam = sayi  # Hata: birikimli toplama yapılmıyor

    return toplam / len(sayilar)

print(ortalama([10, 20, 30]))
```

Öğrenci yalnızca çıktıya bakarsa bölme işleminden veya `len` fonksiyonundan şüphelenebilir. Oysa döngü satırına breakpoint koyup **Step Over** ile ilerlediğinde `toplam` değişkeninin sırasıyla `10`, `20` ve `30` olduğunu görür. Beklenen değerler ise `10`, `30` ve `60` olmalıdır. Böylece hata, `toplam = sayi` satırının `toplam += sayi` olması gerektiği anlaşılmadan önce bile kavramsal olarak teşhis edilir.

Bu deneyim üç önemli modeli güçlendirir:

1. **Kontrol akışı modeli:** Hangi satırın ne zaman çalıştığı görülür.
2. **Durum modeli:** Değişkenlerin zaman içinde değiştiği anlaşılır.
3. **Çağrı modeli:** Fonksiyonların çağrı yığınında bağımsız çalışma alanları oluşturduğu fark edilir.

## Nasıl öğretilmeli?

Debugger eğitimi araç düğmelerini ezberletmekle başlamamalıdır. Önce öğrenciden bir sonraki satırdan sonra değişkenlerin değerini tahmin etmesi istenebilir. Ardından debugger çalıştırılarak tahmin ile gerçek durum karşılaştırılır. Bu döngü şu şekilde özetlenebilir:

$$\text{Tahmin} \rightarrow \text{Gözlem} \rightarrow \text{Çelişki} \rightarrow \text{Model Güncelleme}$$

İlk derslerde yalnızca breakpoint, Step Over ve değişken paneli yeterlidir. Daha sonra Step Into, Step Out, koşullu breakpoint ve call stack eklenebilir. Her özelliği aynı anda göstermek, öğrencinin kod yerine arayüzle mücadele etmesine neden olur.

Sonuç olarak debugger öğretmek yalnızca daha hızlı hata buldurmaz. Öğrenciye programın çalışan, değişen ve gözlemlenebilir bir sistem olduğunu gösterir. İyi kullanılan debugger, kod için bir büyüteçten fazlasıdır: Öğrencinin zihnindeki bilgisayarı yeniden inşa eden küçük bir laboratuvardır.

![debugger-ogretmek-ogrencinin-15](/img/debugger-ogretmek-ogrencinin-15.svg)

