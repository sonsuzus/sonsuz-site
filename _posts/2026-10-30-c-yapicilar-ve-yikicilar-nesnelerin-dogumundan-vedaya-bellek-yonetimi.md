---
layout: post
title: "C++ Yapıcılar ve Yıkıcılar: Nesnelerin Doğumundan Vedaya Bellek Yönetimi"
math: true
categories: 
  - Bilgi
tags: 
  - c++
  - constructors
  - destructors
  - bellek yönetimi
  - raii
  - nesne yaşam döngüsü
toc: true
image: /img/c-yapicilar-ve-65.png
---

![c-yapicilar-ve-65](/img/c-yapicilar-ve-65.svg)


C++ nesnelerini küçük bir atölyenin çalışanları gibi düşünün: İşe başlarken ekipmanlarını hazırlamaları, ayrılırken de masalarını toplamaları gerekir. Yapıcılar nesneyi kullanıma hazırlar; yıkıcılar ise nesnenin sorumluluğundaki kaynakların bırakılmasını sağlar. Bu ikiliyi anlamak, yalnızca bellek sızıntılarını önlemek değil, güvenilir sınıflar tasarlamak için de temel bir adımdır.

``

## Önce teori: Bellek ile nesne aynı şey değildir

Bir nesne için depolama alanı ayrılması, o nesnenin doğru biçimde kurulmuş olması anlamına gelmez. Yapıcı, üyeleri başlatır ve sınıfın geçerli durum koşullarını oluşturur. Örneğin bir tamponun boyutu ile sahip olduğu depolama alanı birbiriyle uyumlu olmalıdır. Bu koşullara **sınıf değişmezi**, yani invariant denir.

Yıkıcı kaynakları temizler; nesnenin kendi depolama alanının bırakılması ise kullanılan depolama modeline bağlıdır. Dolayısıyla “yıkıcı belleği siler” ifadesi tek başına eksiktir.

| Özellik | Yapıcı | Yıkıcı |
|---|---|---|
| İsim | Sınıf adı | Sınıf adının önünde `~` |
| Dönüş türü | Yok | Yok |
| Parametre | Alabilir | Alamaz |
| Aşırı yükleme | Yapılabilir | Yapılamaz |
| Temel görev | Geçerli başlangıç durumu | Kaynak temizliği |

## Yapıcılar: Başlangıç ayarları önemlidir

Parametresiz çağrılabilen yapıcıya **varsayılan yapıcı** denir. Parametreli yapıcılar farklı başlangıç seçenekleri sunar. Bir yapıcının başka bir yapıcıyı çağırması ise delegasyon olarak adlandırılır; böylece aynı kurulum mantığını tekrar yazmazsınız.

Üyeleri yapıcı gövdesinde atamak yerine **üye başlatma listesinde** başlatmak genellikle daha doğrudur. Özellikle referans üyeler ve `const` üyeler burada başlatılmalıdır. Ayrıca üyeler, listede yazdığınız sırayla değil, sınıf içinde bildirildikleri sırayla başlatılır. Bu ayrıntı, başka bir üyeye bağlı başlangıç değerlerinde kritik önem taşır.

## Uygulama: Kendi tamponunu yöneten sınıf

Aşağıdaki sınıf, tamsayı dizisini kurulum sırasında edinir ve yıkım sırasında bırakır. Ham işaretçi burada mekanizmayı görünür kılmak için kullanılıyor:

```cpp
#include <cstddef>
#include <iostream>
#include <memory>

class Tampon {
    std::size_t boyut_;
    int* veri_;

public:
    Tampon() : Tampon(4) {}

    explicit Tampon(std::size_t boyut)
        : boyut_(boyut), veri_(new int[boyut]{}) {}

    Tampon(const Tampon&) = delete;
    Tampon& operator=(const Tampon&) = delete;

    ~Tampon() {
        delete[] veri_;
    }

    std::size_t boyut() const noexcept {
        return boyut_;
    }
};

int main() {
    Tampon yerel;
    auto dinamik = std::make_unique<Tampon>(8);
    std::cout << yerel.boyut() << '\n';
}
```

`Tampon()` dört elemanlık kuruluma yönlendirir. `explicit`, bir sayının istemeden `Tampon` nesnesine dönüştürülmesini engeller. Dizinin sonundaki `{}`, tamsayıları sıfırla başlatır. `delete[]`, `new[]` ile edinilen diziyi doğru biçimde bırakır.

Kopyalama işlemleri özellikle kapatıldı: Varsayılan kopyalama iki nesnenin aynı adresi sahiplenmesine, ardından aynı belleğin iki kez bırakılmasına yol açabilirdi. Bu sınıf taşıma işlemleri de tanımlamadığından, sahipliğin nesneler arasında aktarılmasını desteklemez.

## Yaşam süresi ve RAII

`yerel`, blok sona erdiğinde otomatik olarak yıkılır. `dinamik` ise bir `std::unique_ptr` tarafından sahiplenilir; akıllı işaretçi yıkılınca yönettiği `Tampon` da yıkılır ve depolama alanı bırakılır. Bu örnekte önce `dinamik`, ardından `yerel` temizlenir.

| Kullanım | Temizlik sorumluluğu | Risk |
|---|---|---|
| Yerel nesne | Otomatik kapsam yönetimi | Genellikle düşük |
| Ham `new` | Programcı, uygun `delete` ile | Unutulan temizlik |
| `std::unique_ptr` | Sahiplik nesnesi | Genellikle düşük |

Bu yaklaşımın adı **RAII**: Kaynak edinimini nesne kurulmasına, kaynak bırakmayı nesne yıkımına bağlamak. Kaynak yalnızca bellek değildir; dosya, kilit veya bağlantı da olabilir.

Basit bir kaynak sayacıyla hedefi ifade edebiliriz:

$$R_{son} = R_{ilk} + R_{edinilen} - R_{birakilan}$$

Başlangıçta sahip olunan kaynak sayısı sıfırsa, nesnenin işi bittiğinde sonuç yine sıfır olmalıdır. Atölyeden çıkarken masada unutulan tornavida istemiyoruz!

## İstisnalar ve güvenli tasarım

Yapıcı istisna fırlatırsa nesne tamamen kurulmuş sayılmaz; o nesnenin yıkıcısı çağrılmaz. Ancak başarıyla kurulmuş üyeler ve taban sınıflar temizlenir. Bu yüzden kaynakları akıllı işaretçi veya standart kapsayıcı üyelerde tutmak, yarım kalan kurulumlarda da güvenlik sağlar.

Yıkıcılardan istisna kaçırmaktan kaçının: Özellikle başka bir istisna nedeniyle yığın çözülürken bu durum `std::terminate` ile programı sonlandırabilir. Taban sınıf işaretçisi üzerinden türetilmiş nesneleri silecekseniz, taban yıkıcısını `virtual` yapın.

Gerçek projelerde bu tampon için çoğunlukla `std::vector<int>` tercih edilir. Böylece özel yıkıcı ve sahiplik kodu yazmadan **Rule of Zero** yaklaşımına ulaşılır. En iyi temizlik kodu, çoğu zaman güvenilir bir üyeye devrettiğiniz koddur.
