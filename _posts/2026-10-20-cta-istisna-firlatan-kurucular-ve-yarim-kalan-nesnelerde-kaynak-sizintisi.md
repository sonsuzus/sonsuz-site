---
layout: post
title: "C++’ta İstisna Fırlatan Kurucular ve Yarım Kalan Nesnelerde Kaynak Sızıntısı"
math: true
categories: 
  - Bilgi
tags: 
  - c++
  - istisna yönetimi
  - raii
  - kurucu
  - kaynak yönetimi
  - akıllı işaretçiler
toc: true
image: /img/cta-istisna-firlatan-51.png
---

Bir C++ kurucusu çalışırken istisna fırlatırsa nesne hiçbir zaman tamamen oluşmuş sayılmaz. Bu nedenle nesnenin kendi yıkıcısı çağrılmaz. Kurucu içinde elle edinilmiş bellek, dosya veya kilit gibi kaynaklar varsa bu davranış kolayca sızıntıya dönüşebilir. Neyse ki C++’ın üye yıkım kuralları ve RAII yaklaşımı, doğru kullanıldığında yarım kalan inşaatı güvenli biçimde temizler.

``

## Nesne neden “yarım” kalır?

Bir nesnenin yaşam süresi, kurucusu başarıyla tamamlandığında başlar. Kurucu istisna ile sonlanırsa dışarıdan kullanılabilecek geçerli bir nesne yoktur. Dolayısıyla aşağıdaki yıkıcı çalıştırılmaz:

```cpp
class RiskliTampon {
    int* veri_;

public:
    explicit RiskliTampon(std::size_t adet)
        : veri_(new int[adet]) {
        if (adet > 1000) {
            throw std::runtime_error("Tampon çok büyük");
        }
    }

    ~RiskliTampon() {
        delete[] veri_;
    }
};
```

`new int[adet]` başarılı olduktan sonra istisna fırlatılırsa `~RiskliTampon()` çağrılmaz. Sonuç olarak `veri_` tarafından gösterilen dizi serbest bırakılamaz. Ham işaretçi üyesinin yok edilmesi yalnızca işaretçi değerini ortadan kaldırır; gösterdiği belleğe `delete[]` uygulamaz.

Basit bir risk modeli şu şekilde düşünülebilir:

$$R = P(E) \times K$$

Burada $P(E)$ kurucunun kaynak edinildikten sonra istisna fırlatma olasılığı, $K$ ise temizlenmeden kalan kaynağın maliyetidir. Dosya tanıtıcısı veya mutex gibi sınırlı kaynaklarda $K$, birkaç baytlık bellekten çok daha yüksek olabilir.

## Hangi parçalar otomatik temizlenir?

C++ önemli bir güvence sağlar: Kurucu başarısız olduğunda, yapımı başarıyla tamamlanmış taban sınıflar ve üye nesneler ters sırada yok edilir. Henüz kurulmamış üyeler içinse yıkıcı çağrılmaz.

| Kaynak türü | Kurucu başarısız olunca | Sızıntı riski |
|---|---|---|
| Ham işaretçiyle alınan bellek | Otomatik `delete` yapılmaz | Yüksek |
| `std::unique_ptr` | Üye yıkıcısı belleği bırakır | Düşük |
| `std::vector` | İç belleğini otomatik temizler | Düşük |
| `std::ofstream` | Dosyayı kapatır | Düşük |
| Elle kilitlenen mutex | Açık kalabilir | Yüksek |
| `std::lock_guard` | Kilidi otomatik bırakır | Düşük |

![cta-istisna-firlatan-51](/img/cta-istisna-firlatan-51.svg)


İşte RAII’nin özü budur: Kaynağın ömrünü bir nesnenin ömrüne bağlamak. “Resource Acquisition Is Initialization” adı biraz uzun, yaptığı iş ise oldukça pratiktir: Temizlik kodunu unutulamaz hâle getirir.

## Güvenli çözüm: Kaynakları üyelere emanet etmek

Riskli sınıf `std::vector` kullanılarak şöyle düzeltilebilir:

```cpp
class GuvenliTampon {
    std::vector<int> veri_;
    std::ofstream gunluk_;

public:
    explicit GuvenliTampon(std::size_t adet)
        : veri_(adet), gunluk_("tampon.log") {
        if (!gunluk_) {
            throw std::runtime_error("Günlük açılamadı");
        }

        if (adet > 1000) {
            throw std::runtime_error("Tampon çok büyük");
        }
    }
};
```

İstisna ikinci kontrolda fırlatılsa bile `gunluk_` dosyayı kapatır, ardından `veri_` belleğini bırakır. Sınıfa özel bir yıkıcı yazmak bile gerekmez. Bu yaklaşım aynı zamanda **Rule of Zero** ilkesine uyar: Kaynak yöneten standart sınıfları kullan, kopyalama, taşıma ve yıkım ayrıntılarını derleyiciye bırak.

Dinamik ve tekil bir nesne gerekiyorsa `std::unique_ptr` tercih edilebilir:

```cpp
class MotorYoneticisi {
    std::unique_ptr<Motor> motor_;

public:
    MotorYoneticisi()
        : motor_(std::make_unique<Motor>()) {
        ayarlariYukle(); // Fırlatsa bile Motor yok edilir.
    }
};
```

Kurucu gövdesindeki `try/catch` ile elle temizlik yapmak mümkündür; ancak birden fazla çıkış yolu olduğunda kırılgandır. Kurucuya ait function-try-block da genellikle istisnayı kaydetmek veya başka türe çevirmek içindir; RAII’nin yerini almamalıdır.

Pratik kural nettir: Kurucuda `new`, `fopen`, `lock` veya benzeri çıplak kaynak edinimleri görüyorsanız alarm zilleri çalsın. Kaynağı hemen `std::vector`, `std::unique_ptr`, dosya akışı ya da kilit koruyucusu gibi bir RAII nesnesine teslim edin. Böylece nesne yarım kalsa bile temizlik tam olur.
