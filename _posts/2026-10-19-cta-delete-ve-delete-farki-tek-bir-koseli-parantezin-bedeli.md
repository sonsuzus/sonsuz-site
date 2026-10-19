---
layout: post
title: "C++’ta delete ve delete[] Farkı: Tek Bir Köşeli Parantezin Bedeli"
math: true
categories: 
  - Bilgi
tags: 
  - c++
  - bellek yönetimi
  - delete
  - delete[]
  - tanımsız davranış
  - modern c++
toc: true
image: /img/cta-delete-ve-81.png
---

![cta-delete-ve-81](/img/cta-delete-ve-81.svg)


C++’ta dinamik bellek yönetirken `delete` ile `delete[]` arasındaki iki köşeli parantez küçük görünebilir. Ancak yanlış silme ifadesini kullanmak; bellek sızıntısı, eksik yıkıcı çağrıları, heap bozulması ve yalnızca üretim ortamında ortaya çıkan gizemli çökmeler gibi ciddi sonuçlara yol açabilir.
``
## Temel eşleştirme kuralı

C++’ta bellek ayırma ve serbest bırakma işlemleri doğru biçimde eşleştirilmelidir:

| Bellek ayırma | Belleği serbest bırakma | Kullanım amacı |
|---|---|---|
| `new T` | `delete` | Tek bir nesne |
| `new T[n]` | `delete[]` | Nesne dizisi |
| `malloc` / `calloc` | `free` | C tarzı ham bellek |

Başka bir ifadeyle şu eşitlik korunmalıdır:

$$
new\ T \longleftrightarrow delete
$$

$$
new\ T[n] \longleftrightarrow delete[]
$$

`new[]` ile oluşturulan bir diziyi normal `delete` ile silmek **tanımsız davranıştır**. Tanımsız davranış, programın mutlaka anında çökeceği anlamına gelmez. Program düzgün çalışıyor gibi görünebilir, rastgele sonuç üretebilir veya başka bir noktada çökebilir. Tehlikeli olan da budur.

## Neden iki farklı silme işlemi var?

Tek bir nesne oluşturulduğunda çalışma zamanı yalnızca o nesnenin yıkıcısını çağırır ve belleği serbest bırakır. Dizilerde ise her elemanın ayrı ayrı yok edilmesi gerekir.

Bir dizi $n$ elemandan oluşuyorsa beklenen yıkıcı çağrısı sayısı şöyledir:

$$
D(n) = n
$$

Bazı C++ çalışma zamanı uygulamaları, ayrılan bloğun başında eleman sayısını saklayan ve halk arasında **array cookie** denilen ek bilgiler tutar. `delete[]`, bu bilgiyi kullanarak kaç yıkıcı çağrılması gerektiğini belirleyebilir. Standart, bu mekanizmanın nasıl uygulanacağını zorunlu kılmaz; fakat programcıya doğru silme ifadesini kullanma sorumluluğunu verir.

```cpp
class Sensor {
public:
    Sensor() = default;

    ~Sensor() {
        // Dosya, soket veya başka bir kaynak burada kapatılabilir.
    }
};

int main() {
    Sensor* sensors = new Sensor[4];

    // Dört elemanın da yıkıcısını çalıştırır.
    delete[] sensors;
}
```

Burada `delete sensors;` kullanılsaydı sonuç tanımsız olurdu. Yalnızca ilk elemanın yıkıcısının çağrılacağını varsaymak bile güvenli değildir; standart böyle bir garanti sunmaz.

## İlkel türlerde sorun yok mu?

`int` veya `double` gibi türlerin yıkıcısı olmadığı için yanlış kullanımın zararsız olduğu düşünülebilir:

```cpp
int* scores = new int[100];
delete scores; // Hatalı: delete[] kullanılmalıydı.
```

Bu kod yine tanımsız davranıştır. Bellek yöneticisi dizi tahsisini farklı biçimde izleyebilir. Hata hemen görünmese bile heap yapısı bozulabilir. Doğru kullanım şöyledir:

```cpp
int* scores = new int[100];
delete[] scores;
scores = nullptr;
```

İşaretçiyi `nullptr` yapmak, aynı işaretçinin yanlışlıkla tekrar silinmesi riskini azaltabilir. Ayrıca `delete nullptr` ve `delete[] nullptr` güvenlidir; ikisi de işlem yapmaz.

## Hataları nasıl yakalarız?

AddressSanitizer, Valgrind ve benzeri araçlar tahsis-silme uyumsuzluklarını bulabilir. GCC veya Clang ile örnek bir kontrol derlemesi şöyledir:

```bash
g++ -std=c++20 -Wall -Wextra -fsanitize=address main.cpp
./a.out
```

Derleyici uyarıları yardımcı olsa da işaretçi farklı fonksiyonlara taşındığında hatayı her zaman yakalayamaz.

## Modern C++ çözümü

En güvenli yaklaşım, çıplak `new[]` kullanmaktan kaçınmaktır. Boyutu çalışma zamanında belirlenen diziler için `std::vector`, sabit boyutlular için `std::array` tercih edilmelidir:

```cpp
#include <vector>

int main() {
    std::vector<int> scores(100);
    scores[0] = 42;
} // Bellek otomatik olarak temizlenir.
```

Dinamik bir diziye gerçekten ihtiyaç varsa `std::unique_ptr<T[]>` kullanılabilir. Böylece doğru `delete[]` otomatik olarak çağrılır. Kısacası, `new` gördüğünüzde `delete`, `new[]` gördüğünüzde `delete[]` düşünün; daha iyisi, bu işi RAII kapsayıcılarına bırakın.
