---
layout: post
title: "Az Sözcük, Çok İş: Forth ve Yığın Tabanlı Programlamanın Minimalist Felsefesi"
math: true
categories: 
  - Bilgi
tags: 
  - forth
  - yığın
  - minimalizm
  - programlama dilleri
  - stack machine
  - ters polonya gösterimi
toc: true
---

Modern programlama dünyası katmanlar, paket yöneticileri ve devasa çalışma zamanlarıyla doluyken Forth, küçük bir sırt çantasıyla yola çıkan gezgin gibidir. Sözdizimi son derece azdır; veriler bir yığın üzerinde dolaşır ve program, küçük sözcüklerin yan yana gelmesiyle büyür. İlk bakışta tuhaf görünen bu yaklaşım, bilgisayarın yaptığı işi şaşırtıcı ölçüde görünür kılar.
``
## Forth’un temel fikri

Charles H. Moore tarafından geliştirilen Forth’ta fonksiyonlara genellikle **sözcük** denir. Sayılar yığına eklenir; operatörler gerekli değerleri yığından alıp sonuçları geri bırakır. Bu nedenle `3 + 4` yerine şu ifade yazılır:

```forth
3 4 + .
```

Burada `3` ve `4` yığına itilir, `+` ikisini çıkararak toplar ve sonucu geri iter. `.` ise en üstteki değeri ekrana yazar. İşlem matematiksel olarak $3 + 4 = 7$ olsa da yürütme sırası şöyledir:

$$[] \rightarrow [3] \rightarrow [3,4] \rightarrow [7] \rightarrow []$$

Bu yazım biçimi **ters Polonya gösterimi** olarak bilinir. Parantezlere ve operatör önceliği kurallarına ihtiyaç duymaz; çünkü işlem sırası doğrudan sözcüklerin dizilişiyle belirlenir.

| Yaklaşım | Toplama ifadesi | Ara depolama | Öncelik kuralı |
|---|---|---|---|
| Geleneksel | `(3 + 4) * 2` | Değişken veya geçici değer | Gerekli |
| Yığın tabanlı | `3 4 + 2 *` | Yığının kendisi | Gerekli değil |

## Yığınla düşünmek

Bir yığın, **son giren ilk çıkar** ilkesine göre çalışır. Bunu üst üste konmuş tabaklar gibi düşünebiliriz. En üstteki tabağı almak kolaydır; alttakine ulaşmak için üsttekileri hareket ettirmek gerekir.

Forth, yığını yönetmek için küçük ama güçlü sözcükler sunar:

```forth
5 DUP * .       \ 5'i kopyalar; 5 * 5 sonucunu yazdırır
10 20 SWAP - .  \ değerlerin sırasını değiştirir; 20 - 10 hesaplar
3 8 DROP .      \ 8'i atar ve 3'ü yazdırır
```

Kodun anlaşılabilmesi için sözcüklerin yığın üzerindeki etkisi belgelenir. Örneğin kare alma işlemi şöyle tanımlanabilir:

```forth
: SQUARE ( n -- n² )
  DUP *
;

6 SQUARE .
```

Parantez içindeki `( n -- n² )` bir **yığın etkisi açıklamasıdır**. `--` işaretinin solu girdileri, sağı çıktıları gösterir. Böylece sözcüğü çağırmadan önce yığında ne bulunması gerektiği anlaşılır.

## Minimalizm yalnızca kısa kod değildir

Forth’un minimalist felsefesi, mümkün olan en az karakteri yazmaktan ibaret değildir. Asıl amaç, problemi birbirine eklenebilen küçük kavramlara ayırmaktır. Yeni bir sözcük tanımlandığında dilin sözlüğü genişler. Bir süre sonra program, problem alanına özel küçük bir dile dönüşür.

```forth
: CUBE   ( n -- n³ ) DUP DUP * * ;
: SUM-CUBES ( a b -- result ) CUBE SWAP CUBE + ;

2 3 SUM-CUBES .  \ 2³ + 3³ = 35
```

Burada karmaşık görünen hesap, anlamlı iki sözcüğe bölünmüştür. Matematiksel karşılığı $f(a,b)=a^3+b^3$ biçimindedir. Her sözcük tek başına denenebilir; bu da etkileşimli geliştirmeyi doğal hâle getirir.

| Forth ilkesi | Sağladığı avantaj | Olası bedel |
|---|---|---|
| Küçük sözcükler | Yeniden kullanım ve kolay test | Aşırı bölünmüş kod |
| Açık yığın kullanımı | Düşük seviyede kontrol | Zihinsel takip gereksinimi |
| Etkileşimli yorumlayıcı | Hızlı deney ve hata ayıklama | Araç ekosisteminin küçüklüğü |
| Minimal çalışma zamanı | Gömülü sistemlere uygunluk | Daha fazla geliştirici sorumluluğu |

## Neden hâlâ önemli?

Forth; gömülü sistemlerde, donanım kontrolünde, önyükleyicilerde ve kaynakların sınırlı olduğu ortamlarda yaşamaya devam eder. Ancak asıl mirası belirli bir kullanım alanından büyüktür: Programcıya soyutlamanın hazır kütüphanelerden değil, dikkatle seçilmiş küçük yapı taşlarından da doğabileceğini gösterir.

Yığın tabanlı düşünce WebAssembly, sanal makineler ve bytecode yorumlayıcıları gibi teknolojileri anlamayı da kolaylaştırır. Forth öğrenmek her projeyi Forth ile yazmak anlamına gelmez. Bazen amaç, gereksiz katmanları sorgulamak ve şu soruyu sormaktır: Bu problemi gerçekten kaç temel işlemle çözebilirim?
