---
layout: post
title: "Foreign Function Interface: Programlama Dilleri Arasında Köprü Kurmak"
math: true
categories: 
  - Bilgi
tags: 
  - ffi
  - programlama
  - yerel-kod
  - bellek-yönetimi
  - c
  - python
toc: true
---

Bir Python uygulamasının C ile yazılmış ışık hızındaki bir kütüphaneyi çağırması veya Rust kodunun işletim sistemine ait işlevleri kullanması sihir değildir. Bu iletişimi sağlayan mekanizma **Foreign Function Interface**, kısaca **FFI** olarak adlandırılır. FFI, farklı kurallara ve çalışma zamanlarına sahip programlama dillerinin aynı masaya oturup anlaşmasını sağlayan teknik bir tercümandır.
``
## FFI tam olarak nedir?

Her programlama dili fonksiyonları çağırmak, verileri bellekte tutmak ve hataları aktarmak için belirli kurallar kullanır. FFI ise bir dilin, başka bir dilde derlenmiş fonksiyonları sanki kendi fonksiyonlarıymış gibi çağırabilmesini sağlayan arayüzdür.

Örneğin C ile yazılmış aşağıdaki fonksiyonu düşünelim:

```c
int topla(int a, int b) {
    return a + b;
}
```

Bu kod paylaşımlı bir kütüphane olarak derlendiğinde Python, Rust veya Java tarafından kullanılabilir. Ancak tarafların `int` türünün boyutu, fonksiyonun adı ve parametrelerin hangi sırayla aktarılacağı konusunda anlaşması gerekir.

## ABI: Köprünün trafik kuralları

FFI çoğunlukla **Application Binary Interface**, yani ABI üzerinde çalışır. API kaynak kod düzeyindeki sözleşmeyi tanımlarken ABI, derlenmiş kod düzeyindeki ayrıntıları belirler. Çağırma kuralı, işlemci yazmaçlarının kullanımı, veri hizalaması ve sembol adları bu sözleşmenin parçalarıdır.

Bir veri türünün taşıdığı bit sayısı kabaca şöyle ifade edilebilir:

$$\text{Değer aralığı} = -2^{n-1} \ldots 2^{n-1}-1$$

Burada $n$, işaretli tam sayının bit genişliğidir. Bir taraf 32 bit, diğer taraf 64 bit kabul ederse veriler yanlış yorumlanabilir; köprü daha açılmadan trafik kazası yaşanır.

| Kavram | Görevi | Olası sorun |
|---|---|---|
| API | Kaynak kod sözleşmesini tanımlar | Sürüm uyumsuzluğu |
| ABI | İkili çağrı kurallarını belirler | Platform farklılığı |
| FFI | Diller arası çağrıyı mümkün kılar | Tür ve bellek hataları |
| Serileştirme | Veriyi taşınabilir biçime çevirir | Dönüştürme maliyeti |

## Python ile C fonksiyonu çağırmak

Python’ın standart kütüphanesindeki `ctypes`, basit FFI denemeleri için kullanışlıdır. C kodunun Linux üzerinde `libmatematik.so` adıyla derlendiğini varsayalım:

```python
import ctypes

kutuphane = ctypes.CDLL("./libmatematik.so")

kutuphane.topla.argtypes = [ctypes.c_int, ctypes.c_int]
kutuphane.topla.restype = ctypes.c_int

sonuc = kutuphane.topla(20, 22)
print(sonuc)  # 42
```

`argtypes`, C fonksiyonunun beklediği parametreleri; `restype` ise dönüş türünü açıklar. Bu tanımlar yalnızca belgeleme değildir: Python’ın değerleri doğru biçimde dönüştürmesine yardım eder. Yanlış bir işaretçi türü belirtmek, kontrollü bir Python istisnası yerine programın aniden çökmesine yol açabilir.

## Bellek yönetimi neden kritik?

FFI dünyasının temel sorusu şudur: **Belleğin sahibi kim?** C tarafında `malloc` ile ayrılan alanın çoğunlukla yine C tarafında `free` ile bırakılması gerekir. Python’ın çöp toplayıcısı veya Rust’ın sahiplik sistemi, yabancı kütüphanenin kurallarını kendiliğinden bilemez.

| Yaklaşım | Avantaj | Dezavantaj |
|---|---|---|
| Veriyi kopyalamak | Güvenli ve anlaşılır | Ek süre ve bellek tüketir |
| İşaretçi paylaşmak | Yüksek performans sağlar | Yaşam süresi hatalarına açıktır |
| Güvenli sarmalayıcı | Kullanımı kolaylaştırır | Geliştirme ve bakım ister |

Kopyalama maliyeti yaklaşık olarak veri miktarıyla doğrusal artar:

$$T(n) = O(n)$$

Bu yüzden büyük görüntüler veya makine öğrenmesi tensörleri aktarılırken sıfır kopyalı yöntemler tercih edilebilir. Fakat performans uğruna güvenliği pencereden aşağı atmamak gerekir.

## Ne zaman kullanılmalı?

FFI; mevcut yerel kütüphaneleri yeniden kullanmak, işletim sistemi API’lerine erişmek ve performans gerektiren bölümleri hızlandırmak için idealdir. Buna karşılık süreçler arası veya ağ üzerinden iletişim gerekiyorsa REST, gRPC ya da mesaj kuyrukları daha uygun olabilir.

İyi tasarlanmış bir FFI katmanı küçük, açık ve test edilebilir tutulmalıdır. Sınırda basit veri türleri kullanılmalı, hata kodları anlamlı istisnalara dönüştürülmeli ve bellek sahipliği belgelenmelidir. Böylece farklı diller rakip olmak yerine aynı orkestrada çalan enstrümanlara dönüşür.
