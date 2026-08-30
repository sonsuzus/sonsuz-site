---
layout: post
title: "Rubik Küpü İçin Kociemba Algoritması: 20 Hamlelik Matematik"
math: true
categories: 
  - Bilgi
tags: 
  - rubik küpü
  - kociemba
  - grup teorisi
toc: true
---

Rubik küpünü çözmek, yalnızca renkleri eşleştirmek değil; devasa ama sonlu bir matematiksel uzayda rota planlamaktır. Herbert Kociemba’nın iki aşamalı algoritması, pratikte çok hızlı çözümler üretirken grup teorisinin zarif fikirlerinden yararlanır. Hedef her zaman mutlak en kısa çözüm değildir; buna karşın algoritma çoğu karışıklığı yaklaşık 20 hamle civarında çözer. Bu yaklaşım, küpü tek seferde “fethedilecek” bir problem yerine, akıllıca daraltılmış iki ayrı problem olarak görür.
``

## Küp, hamleler ve grup fikri

Küpün her yasal durumu bir **permütasyon** ve **oryantasyon** birleşimidir: parçalar hem yer değiştirir hem de yönleri değişebilir. `R`, `U`, `F` gibi yüz hamleleri durum uzayı üzerinde çalışan dönüşümlerdir. Bu dönüşümler birleşince bir grup oluşturur; çünkü birim durum vardır, her hamlenin tersi vardır ve hamle dizileri birleşebilir.

Küpün teorik durum sayısı yaklaşık olarak şöyledir:

$$
\frac{8!\cdot 3^7\cdot 12!\cdot 2^{11}}{12} = 43\,252\,003\,274\,489\,856\,000
$$

Bu sayı 43 kentilyondan fazladır. Dolayısıyla her durumu tek tek dolaşan kaba kuvvetli arama, bilgisayarınızın fanını küçük bir jet motoruna çevirebilir. Kociemba’nın temel numarası, bu uzayı bir **alt gruba** doğru yönlendirmektir.

| Kavram | Küp üzerindeki karşılığı | Neden önemlidir? |
|---|---|---|
| Grup | Tüm yasal küp durumları | Hamlelerin matematiksel modelidir. |
| Üreteç | `U, D, L, R, F, B` hamleleri | Tüm erişilebilir durumları üretir. |
| Alt grup | Belirli kısıtları sağlayan durumlar | Arama alanını dramatik biçimde küçültür. |
| Koset | Alt gruba göre sınıflandırılan durum | Birinci aşamada hedeflenen “bölgeyi” temsil eder. |

## Birinci aşama: Küpü doğru mahalleye taşımak

Kociemba, ilk aşamada küpü $G_1$ adlı alt gruba getirir. Bu aşamanın hedefi küpü tamamen çözmek değildir. Bunun yerine üç yapısal koşul sağlanır:

1. Köşe parçalarının yönleri düzeltilir.
2. Kenar parçalarının yönleri düzeltilir.
3. Orta katman kenarları kendi dilim grubuna yerleştirilir.

Bu noktada küp hâlâ karışık görünebilir, fakat artık ikinci aşamada kullanılabilecek hamleler çok daha kontrollüdür. Birinci aşama genellikle tüm yüz dönüşlerini kullanır; arama sırasında ters hamleler ve aynı yüzün gereksiz tekrarları elenir.

Örneğin hamle isimleri ve etkileri şöyle okunur:

```text
R   : Sağ yüzü saat yönünde çevir
R'  : Sağ yüzü saat yönünün tersine çevir
R2  : Sağ yüzü 180 derece çevir
U   : Üst yüzü saat yönünde çevir
```

Bir çözücü, küp durumunu genellikle parça indeksleri ve yön bitleriyle saklar. Böylece renkleri tekrar tekrar yorumlamak yerine, hızlı tablo erişimleri yapılır.

## İkinci aşama: Kısıtlı hamlelerle eve dönüş

$G_1$ içine girildiğinde algoritma daha sınırlı bir hamle kümesi kullanır:

$$
\{U, U2, U', D, D2, D', R2, L2, F2, B2\}
$$

Yan yüzlerde yalnızca çift dönüşlerin kalması kritik bir ayrıntıdır. Bu hamleler, ilk aşamada düzeltilen yönleri bozmaz. Artık problem; köşeleri, kenarları ve dilimleri doğru konumlarına permüte etmektir.

| Aşama | Ana hedef | İzin verilen hamleler | Tipik rol |
|---|---|---|---|
| Faz 1 | Yönleri ve dilim üyeliğini düzeltmek | Tüm temel yüz hamleleri | Alt gruba geçiş |
| Faz 2 | Parçaları kesin konumlarına taşımak | `U`, `D` ve yan yüzlerin çift dönüşleri | Tam çözüm |

Arama çoğunlukla **IDA\*** (Iterative Deepening A*) ile yapılır. Bu yöntem derinlik sınırını kademeli artırır; ancak sezgisel alt sınır tabloları sayesinde imkânsız dalları erkenden keser. Örneğin bir koordinatın çözülmesi için en az 5 hamle gerektiği biliniyorsa, geriye 3 hamle kalmış bir dal doğrudan atılır.

Kociemba algoritması “Tanrı’nın Sayısı” olan 20 hamleyi her durumda garanti eden yöntem değildir; bu rekor, çok daha geniş hesaplamalarla kanıtlanmıştır. Yine de hız, çözüm uzunluğu ve uygulama kolaylığı arasındaki dengesi olağanüstüdür. Grup teorisi burada soyut bir ders konusu olmaktan çıkar: renkli bir küpü, iyi seçilmiş alt gruplar ve akıllı arama ile dakikalar değil saniyeler içinde çözen gerçek bir mühendislik aracına dönüşür.
