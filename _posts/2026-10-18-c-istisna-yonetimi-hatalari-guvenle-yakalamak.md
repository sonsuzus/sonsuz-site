---
layout: post
title: "C++ İstisna Yönetimi: Hataları Güvenle Yakalamak"
math: true
categories: 
  - Bilgi
tags: 
  - c++
  - istisna yönetimi
  - exception handling
  - try-catch
  - hata yönetimi
toc: true
image: /img/c-istisna-yonetimi-33.png
---

Bir C++ programı derlenmiş olsa bile çalışma sırasında dosya bulunamaması, belleğin ayrılamaması veya geçersiz veriyle karşılaşılması gibi sorunlar yaşayabilir. İstisna yönetimi, bu beklenmedik durumları programı aniden sonlandırmadan uygun bir noktaya bildirmemizi sağlar. Kısacası `throw` alarmı çalıştırır, `try` riskli bölgeyi gözetler, `catch` ise olaya müdahale eder.
``
## İstisna yönetiminin temel mantığı

Normal koşullarda fonksiyonlar sonuçlarını `return` ile döndürür. Ancak bir fonksiyon görevini tamamlayamıyorsa sıradan bir sonuç döndürmek yanıltıcı olabilir. Örneğin pozitif sayı bekleyen bir karekök fonksiyonuna negatif değer verilmesi ayrı bir kontrol akışı gerektirir.

İstisna oluştuğunda program, uygun bir `catch` bloğu bulana kadar çağrı zincirinde geriye ilerler. Bu sürece **stack unwinding** denir. Matematiksel olarak bir fonksiyonun geçerli kümesini şöyle gösterebiliriz:

$$
f(x) = \sqrt{x}, \qquad x \in [0, \infty)
$$

Burada $x < 0$ olması, fonksiyon sözleşmesinin ihlal edildiğini belirtir.

| Araç | Görevi | Benzetme |
|---|---|---|
| `try` | Hata oluşturabilecek kodu çalıştırır | Güvenlik kamerası |
| `throw` | İstisna üretir | Alarm düğmesi |
| `catch` | Belirli istisnayı yakalar | Müdahale ekibi |
| `noexcept` | Fonksiyonun istisna fırlatmayacağını bildirir | Güvenlik garantisi |

## Temel `try`, `throw` ve `catch` kullanımı

Aşağıdaki örnek, bölme işleminden önce paydayı denetler. Sıfıra bölme tespit edildiğinde `std::runtime_error` nesnesi fırlatılır:

```cpp
#include <iostream>
#include <stdexcept>

double bol(double pay, double payda) {
    if (payda == 0.0) {
        throw std::runtime_error("Sıfıra bölme girişimi!");
    }
    return pay / payda;
}

int main() {
    try {
        std::cout << bol(42, 0) << '\n';
    } catch (const std::runtime_error& hata) {
        std::cerr << "Hata: " << hata.what() << '\n';
    }
}
```

İstisnanın `const` referansla yakalanması gereksiz kopyalamayı engeller ve çok biçimliliği korur. `what()` metodu ise hatanın açıklamasını verir. Program kontrolsüz biçimde çökmek yerine kullanıcıya anlamlı bir mesaj sunar.

## Standart mı, özel istisna mı?

C++ standart kütüphanesi `std::exception` tabanlı birçok hata türü sağlar.

| İstisna | Uygun kullanım |
|---|---|
| `std::invalid_argument` | Geçersiz fonksiyon argümanı |
| `std::out_of_range` | Aralık dışı indeks |
| `std::runtime_error` | Genel çalışma zamanı sorunu |
| `std::bad_alloc` | Bellek ayırma başarısızlığı |

Uygulamaya özgü hatalar için özel bir sınıf da tanımlanabilir:

```cpp
#include <stdexcept>
#include <string>

class BakiyeHatasi : public std::runtime_error {
public:
    explicit BakiyeHatasi(const std::string& mesaj)
        : std::runtime_error(mesaj) {}
};

void paraCek(double bakiye, double miktar) {
    if (miktar > bakiye) {
        throw BakiyeHatasi("Yetersiz bakiye");
    }
}
```

Bu yaklaşım, çağıran kodun banka işlemlerine özgü problemi diğer çalışma zamanı hatalarından ayırmasını sağlar.

## Yakalama sırası ve yeniden fırlatma

`catch` blokları özel türden genel türe doğru sıralanmalıdır. Aksi hâlde `std::exception` gibi genel bir blok, türetilmiş bütün istisnaları önce yakalayabilir.

```cpp
try {
    paraCek(100, 250);
} catch (const BakiyeHatasi& hata) {
    std::cerr << hata.what() << '\n';
    throw; // Aynı istisnayı üst seviyeye iletir
} catch (const std::exception& hata) {
    std::cerr << "Genel hata: " << hata.what() << '\n';
}
```

Parametresiz `throw;`, mevcut istisnayı türünü kaybetmeden yeniden fırlatır. Bu yöntem, alt seviyede kayıt tutup üst seviyede kullanıcıya cevap vermek için kullanışlıdır.

## Güvenli tasarım için kısa kurallar

İstisnaları sıradan döngü kontrolü amacıyla değil, gerçekten olağan dışı durumlar için kullanın. Kaynak yönetiminde RAII yaklaşımını tercih edin; `std::vector`, `std::string` ve akıllı işaretçiler stack unwinding sırasında otomatik olarak temizlenir. Yıkıcılar mümkünse istisna fırlatmamalıdır. Ayrıca yalnızca gerçekten garanti verebildiğiniz fonksiyonları `noexcept` olarak işaretleyin.

Doğru tasarlanmış istisna yönetimi hataları yok etmez; onları görünür, sınıflandırılabilir ve güvenli biçimde yönetilebilir hâle getirir. Böylece programınız ilk beklenmedik durumda havlu atmak yerine kontrollü bir iniş yapar.

![c-istisna-yonetimi-33](/img/c-istisna-yonetimi-33.svg)

