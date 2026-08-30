---
layout: post
title: "Programlama Dilleri ve Sapir-Whorf: Python Gibi Mi Düşünüyoruz?"
math: true
categories: 
  - Bilgi
tags: 
  - programlama dilleri
  - python
  - c++
  - sapir-whorf
  - yazılım düşüncesi
toc: true
---

Bir programlama dili yalnızca bilgisayara talimat vermenin aracı değildir; aynı zamanda geliştiricinin problemi nasıl parçaladığını, hangi çözümleri önce aklına getirdiğini ve hangi maliyetleri görünmez kabul ettiğini etkileyen bir düşünme ortamıdır. Sapir-Whorf hipotezinin güçlü yorumu, konuştuğumuz dilin düşüncemizi kesin biçimde belirlediğini söyler. Programlamaya uyarladığımızda bu iddia fazla sert görünür: Python kullanan bir kişi C++ tarzı düşünemez mi? Elbette düşünebilir. Ancak zayıf yorum çok daha ikna edicidir: Dil, bazı zihinsel yolları kolaylaştırır; bazılarını ise daha zahmetli ve dolayısıyla daha az görünür hâle getirir.
``

## Hipotezden kod editörüne

Dilsel görelilik fikrinin programlamadaki karşılığı, bir dilin sunduğu soyutlamaların çözüm uzayını **eğmesi**dir. Python'da liste üreteçleri, sözlükler ve dinamik nesneler gündelik araçlardır. C++'ta bellek yerleşimi, sahiplik, tür maliyeti ve ömür yönetimi daha erken aşamada gündeme gelir. Bu fark, birinin yaratıcı diğerinin kısıtlı olduğu anlamına gelmez; iki dil farklı maliyet fonksiyonlarını öne çıkarır.

Bir geliştiricinin kabaca çözüm seçimi şu şekilde modellenebilir:

$$
\text{Tercih edilen çözüm} = \arg\min_{s \in S}(M_s + B_s + H_s)
$$

Burada $M_s$ makine maliyeti, $B_s$ bilişsel yük, $H_s$ ise dilin ve ekosistemin çözüm için oluşturduğu sürtünmedir. Python, birçok işte $B_s$ ve $H_s$ değerini azaltır. C++ ise performans veya bellek kritik senaryolarda $M_s$ üzerinde daha doğrudan kontrol sağlayabilir.

| Boyut | Python'ın varsayılan sezgisi | C++'ın varsayılan sezgisi |
|---|---|---|
| Veri işleme | "Önce açık ve kısa yaz" | "Temsilin maliyetini düşün" |
| Türler | Çalışma anında esneklik | Derleme zamanında güvence |
| Bellek | Çoğunlukla otomatik yönetim | Sahiplik ve ömür farkındalığı |
| Performans | Gerekirse sonra ölç | Tasarımın başından itibaren hesaba kat |
| Soyutlama | Hızlı prototipleme | Sıfır maliyetli soyutlama hedefi |

## Aynı problem, farklı ilk refleksler

Örneğin bir listedeki çift sayıların karelerini üretelim. Python geliştiricisinin zihninde dönüşüm hattı doğal biçimde belirir:

```python
numbers = [1, 2, 3, 4, 5, 6]
squares = [n * n for n in numbers if n % 2 == 0]
print(squares)  # [4, 16, 36]
```

Bu kod, **ne yapılacağını** öne çıkarır: filtrele, dönüştür, sonucu al. Orta düzeydeki geliştirici için burada önemli ders, ifade gücü yüksek bir yapının niyeti görünür kılmasıdır. Ancak çok büyük verilerde ara koleksiyonun maliyeti veya gecikmeli değerlendirme ihtiyacı ayrıca düşünülmelidir.

C++ tarafında aynı niyet algoritmalar, iterator'lar ve çıktı kapsayıcısı üzerinden ifade edilebilir:

```cpp
std::vector<int> numbers{1, 2, 3, 4, 5, 6};
std::vector<int> squares;

for (int n : numbers) {
    if (n % 2 == 0) {
        squares.push_back(n * n);
    }
}
```

Bu örnek C++'ın mutlaka uzun yazıldığı klişesini kanıtlamaz. Asıl fark, `squares` kapsayıcısının büyümesi, ayrılan bellek ve veri temsilinin daha kolay fark edilmesidir. Modern C++ ranges araçlarıyla kod daha bildirimselleşebilir; yani dilin sürümü ve kütüphanesi de düşünme biçiminin parçasıdır.

## Zihinsel sınır mı, alışkanlık mı?

Programlama dili mutlak bir zihinsel hapishane değildir. Tecrübeli bir Python geliştiricisi veri yerelliğini öğrenebilir; C++ geliştiricisi fonksiyonel dönüşümlerle rahatça çalışabilir. Yine de günlük tekrarlar önemlidir. Her gün mutasyonla çalışan biri, değişmez veri yapılarını; her gün garbage collector'a güvenen biri, deterministik kaynak kapatmayı daha geç düşünebilir.

Bu nedenle en sağlıklı yaklaşım, dili kimlik değil mercek olarak görmektir. Performans kritik bir modülü C++ zihniyetiyle, veri analizi akışını Python zihniyetiyle incelemek geliştiricinin çözüm repertuvarını büyütür. Sapir-Whorf'un programcıya verdiği eğlenceli ders şudur: Kullandığınız dil sizi tamamen yönetmez; ama editörü her açtığınızda size hangi soruları önce sormanız gerektiğini fısıldar.
