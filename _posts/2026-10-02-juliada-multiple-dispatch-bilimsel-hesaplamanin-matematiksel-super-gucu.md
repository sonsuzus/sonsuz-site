---
layout: post
title: "Julia’da Multiple Dispatch: Bilimsel Hesaplamanın Matematiksel Süper Gücü"
math: true
categories: 
  - Bilgi
tags: 
  - julia
  - multiple dispatch
  - bilimsel hesaplama
  - performans
  - tip sistemi
  - programlama
toc: true
image: /img/juliada-multiple-dispatch-93.png
---

Julia’nın bilimsel hesaplamada parlamasının arkasında yalnızca hızlı döngüler veya LLVM bulunmaz. Dilin asıl süper güçlerinden biri **multiple dispatch**, yani çoklu dağıtımdır. Bu yaklaşımda çalıştırılacak metot sadece ilk argümanın sınıfına göre değil, fonksiyona verilen **bütün argümanların tip bileşimine** göre seçilir. Böylece matematiksel işlemler hem doğal biçimde ifade edilir hem de derleyiciye güçlü optimizasyon fırsatları sunar.

``

## Multiple dispatch tam olarak nedir?

Bir fonksiyon çağrısını $f(x_1, x_2, \ldots, x_n)$ olarak düşünelim. Tekli dağıtım kullanan klasik nesne yönelimli dillerde metot seçimi çoğunlukla ilk nesnenin tipine bağlıdır:

$$M = D(T_1)$$

Julia’da ise seçim fonksiyonun adıyla birlikte tüm argüman tipleri üzerinden yapılır:

$$M = D(f, T_1, T_2, \ldots, T_n)$$

Buradaki $D$, uygun metodu bulan dağıtım mekanizmasıdır. Örneğin bir `çarp` işlemi; matris-matris, matris-vektör veya sayı-matris çiftleri için ayrı davranabilir. Bu davranışları tek bir sınıf hiyerarşisine zorla yerleştirmek gerekmez.

| Yaklaşım | Metot seçimi | Bilimsel modellemeye etkisi |
|---|---|---|
| Tekli dispatch | Genellikle alıcı nesnenin tipi | İşlem bir sınıfa aitmiş gibi tasarlanır |
| Fonksiyon aşırı yükleme | Derleme zamanındaki imza | Statik ve çoğu zaman sınırlı esneklik |
| Multiple dispatch | Tüm çalışma zamanı tipleri | Matematiksel ilişkiler doğrudan modellenir |

![juliada-multiple-dispatch-93](/img/juliada-multiple-dispatch-93.svg)


## Küçük ama güçlü bir örnek

Aşağıdaki kod, parçacıkların etkileşimini tür çiftine göre tanımlar:

```julia
abstract type Particle end

struct Electron <: Particle
    charge::Float64
end

struct Proton <: Particle
    charge::Float64
end

interact(a::Electron, b::Electron) = "Elektrostatik itme"
interact(a::Proton, b::Proton) = "Elektrostatik itme"
interact(a::Electron, b::Proton) = "Elektrostatik çekim"
interact(a::Proton, b::Electron) = interact(b, a)

println(interact(Electron(-1.0), Proton(1.0)))
```

Burada `interact` fonksiyonunun hangi sürümünün çalışacağı hem `a` hem de `b` argümanının tipine bağlıdır. Son metot, simetrik ilişkiyi tekrar kodlamak yerine argümanları ters çevirerek mevcut davranışı kullanır. Bu yapı, $F(a,b)=F(b,a)$ gibi matematiksel simetrileri okunabilir şekilde programa taşır.

## Peki neden hızlı?

Multiple dispatch tek başına sihirli biçimde hız üretmez. Asıl kazanç, Julia’nın **tip çıkarımı** ve **JIT derlemesi** ile birleştiğinde ortaya çıkar. Derleyici bir çağrıda somut tipleri gördüğünde, ilgili metot için özelleştirilmiş makine kodu üretir.

Örneğin `add(x, y) = x + y` fonksiyonu `Float64` değerlerle çağrıldığında derleyici genel bir “her türü kontrol et” döngüsü çalıştırmak yerine `Float64` toplamasına özel kod oluşturabilir. Süreç kabaca şöyledir:

1. Argümanların somut tipleri belirlenir.
2. En özel uyumlu metot seçilir.
3. Fonksiyon bu tip bileşimi için uzmanlaştırılır.
4. LLVM gereksiz dalları ve ara nesneleri kaldırabilir.
5. Üretilen kod sonraki çağrılar için önbelleğe alınır.

Performansı basitçe şu fikirle özetleyebiliriz:

$$T_{toplam} = T_{derleme} + N \cdot T_{çalıştırma}$$

İlk çağrıda $T_{derleme}$ hissedilebilir; ancak büyük bir bilimsel simülasyonda $N$ büyüdükçe uzmanlaştırılmış kodun düşük $T_{çalıştırma}$ maliyeti baskın avantaj sağlar.

## Soyutlama bedava olabilir mi?

Julia’nın önemli vaadi, doğru tiplerle yazılmış yüksek seviyeli kodun düşük seviyeli koda yakın çalışabilmesidir. Bir diferansiyel denklem çözücüsü; normal sayılar, yüksek hassasiyetli sayılar, birim taşıyan değerler veya otomatik türev tipleriyle aynı algoritmayı kullanabilir. Yeni bir sayısal tip ekleyen geliştirici, gerekli aritmetik metotlarını tanımladığında mevcut ekosistemin büyük bölümüne katılabilir.

Ancak tip kararsızlığı bu avantajı zayıflatır. Bir fonksiyon farklı dallarda ilgisiz tipler döndürüyorsa derleyici kesin makine kodu üretmekte zorlanabilir. Bu nedenle `@code_warntype` ve `@btime` gibi araçlar önemlidir.

Sonuç olarak multiple dispatch, yalnızca şık bir fonksiyon seçme tekniği değildir. Matematiksel işlemleri nesnelerin içine hapsetmeden ifade eder, bağımsız paketlerin birlikte genişletilebilmesini sağlar ve somut tip uzmanlaştırmasıyla yüksek performansa dönüşür. Julia’nın hızı, dinamik esneklik ile derlenmiş kod disiplininin oldukça bilimsel bir evliliğidir.
