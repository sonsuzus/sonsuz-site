---
layout: post
title: "Kodun Trafik Polisi: Linter Araçlarıyla Ekip Verimliliğini Artırmak"
math: true
categories: 
  - Bilgi
tags: 
  - kodlama standartları
  - linter
  - python ve c++
toc: true
---

Bir ekipte herkes çalışan kod yazabilir; asıl mesele, herkesin okuyabildiği ve güvenle değiştirebildiği kod yazmaktır. Girintilerden değişken adlarına, kullanılmayan importlardan olası bellek hatalarına kadar pek çok ayrıntıyı otomatik denetleyen linter araçları, kod incelemelerini küçük tartışmalardan kurtarıp mimari kararlara odaklar. Kısacası linter, yalnızca kodun trafik polisi değil, ekibin sessiz kalite koçudur.

``

## Kodlama standardı neden gereklidir?

Kodlama standardı; kaynak kodun biçimini, isimlendirme kurallarını, dosya düzenini ve bazı güvenli programlama ilkelerini tanımlar. Python dünyasında **PEP 8**, C++ tarafında ise **Google C++ Style Guide** ve **C++ Core Guidelines** sık kullanılan referanslardır.

Standartların temel amacı estetik değildir. Tutarlılık, geliştiricinin kodu anlamak için harcadığı zihinsel enerjiyi azaltır. Bu durumu basitçe şöyle modelleyebiliriz:

$$T_{toplam} = T_{mantık} + T_{biçim} + T_{hata}$$

Burada linter ve otomatik biçimlendiriciler $T_{biçim}$ süresini küçültür, bazı hataları erkenden yakalayarak $T_{hata}$ değerini de düşürür. Böylece ekip, zamanının daha büyük bölümünü iş mantığına ayırabilir.

| Yaklaşım | Avantaj | Dezavantaj |
|---|---|---|
| Kuralları geliştiriciye bırakmak | Başlangıçta esnektir | Tutarsızlık ve tartışma üretir |
| Yalnızca kod incelemesi yapmak | İnsan bağlamı anlayabilir | Tekrarlayan kontroller zaman kaybettirir |
| Linter ve formatlayıcı kullanmak | Hızlı, tarafsız ve tekrarlanabilirdir | İlk yapılandırma emek ister |
| CI üzerinde zorunlu denetim | Hatalı kodun birleşmesini önler | Fazla katı kurallar akışı yavaşlatabilir |

## Python tarafındaki araçlar

Python projelerinde **Ruff**, **Pylint** ve **Flake8** yaygın linter seçenekleridir. **Black** ise kodu otomatik biçimlendirir. Ruff, çok sayıda denetimi yüksek hızla gerçekleştirdiği için modern projelerde özellikle popülerdir.

Aşağıdaki kod çalışabilir, ancak gereksiz import ve okunabilirlik sorunları içerir:

```python
import os

def calculate_total(items):
    total=0
    for x in items:
        total=total+x
    return total
```

Ruff kullanılmayan `os` importunu bildirir. Black ise operatörlerin çevresindeki boşlukları düzenler. Daha anlaşılır sürüm şöyle olabilir:

```python
def calculate_total(items):
    total = 0
    for item in items:
        total += item
    return total
```

Denetimi terminalde çalıştırmak oldukça kolaydır:

```bash
ruff check .
black --check .
```

İlk komut olası problemleri tarar; ikinci komut dosyaların Black biçimine uygun olup olmadığını, içerikleri değiştirmeden kontrol eder.

## C++ tarafında güvenlik de sahneye çıkar

C++ projelerinde biçim kadar tür güvenliği, kaynak yönetimi ve tanımsız davranış ihtimali de önemlidir. **clang-tidy** statik analiz yaparken **clang-format** kod görünümünü standartlaştırır. **Cppcheck** de olası hata ve taşınabilirlik problemlerini araştırır.

```cpp
#include <iostream>

int main() {
    int* value = new int(42);
    std::cout << *value << '\n';
    return 0;
}
```

Bu örnekte ayrılan bellek serbest bırakılmamıştır. Modern C++ yaklaşımı, çıplak işaretçi yerine otomatik ömür yönetimini tercih eder:

```cpp
#include <iostream>
#include <memory>

int main() {
    auto value = std::make_unique<int>(42);
    std::cout << *value << '\n';
}
```

`clang-tidy`, yapılandırmaya bağlı olarak modernleştirme ve kaynak yönetimi önerileri sunabilir. Böylece linter, yalnızca boşluk sayan huysuz bir robot olmaktan çıkar; üretim hatalarını önleyen bir yardımcıya dönüşür.

## Ekip verimliliğine gerçek katkı

Linter kuralları depo içinde paylaşılmalı ve CI sürecine eklenmelidir. Python için `pyproject.toml`, C++ için `.clang-tidy` ve `.clang-format` dosyaları kuralları merkezi hâle getirir. Yerel **pre-commit** kontrolleri de geliştiriciye hızlı geri bildirim verir.

Ölçülebilir kazanç yaklaşık olarak şöyle ifade edilebilir:

$$Kazanç = İnceleme\ Süresi_{önce} - İnceleme\ Süresi_{sonra}$$

Ancak her uyarıyı zorunlu hata yapmak doğru değildir. Eski bir projede yüzlerce uyarıyı bir gecede engelleyici hâle getirmek ekibi felç edebilir. Önce yeni veya değiştirilen kodu denetlemek, ardından teknik borcu kademeli temizlemek daha sağlıklıdır.

İyi yapılandırılmış bir linter, geliştiricinin yerine düşünmez; tekrar eden kontrolleri üstlenerek geliştiricinin daha değerli problemleri düşünmesini sağlar. Sonuçta kazanan yalnızca temiz kod değil, daha hızlı inceleme yapan, daha az hata üreten ve “bu süslü parantez nereye gelmeli?” toplantılarını tarihe gömen ekiptir.
