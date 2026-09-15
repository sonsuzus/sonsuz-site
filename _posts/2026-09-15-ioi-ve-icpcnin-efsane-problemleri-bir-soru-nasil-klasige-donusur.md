---
layout: post
title: "IOI ve ICPC’nin Efsane Problemleri: Bir Soru Nasıl Klasiğe Dönüşür?"
math: true
categories: 
  - Bilgi
tags: 
  - ioi
  - icpc
  - algoritma
  - rekabetçi programlama
  - dinamik programlama
  - graf teorisi
toc: true
---

Bazı yarışma problemleri çözülüp unutulur; bazılarıysa yıllar sonra bile eğitim kamplarında, çevrim içi jürilerde ve algoritma sohbetlerinde karşımıza çıkar. IOI ile ICPC tarihinde klasikleşen soruların sırrı yalnızca zor olmaları değildir. Bu problemler, gündelik görünen bir hikâyenin altına güçlü bir matematiksel model saklar ve çözücüye belirli bir algoritmayı ezberletmek yerine onu keşfettirir.
``

## İki yarışma, iki farklı problem kültürü

International Olympiad in Informatics (IOI), lise öğrencilerine yönelik bireysel bir yarışmadır. Sorular çoğunlukla alt görevler ve kısmi puanlama içerir. Bu nedenle önce yavaş ama doğru bir çözüm kurup ardından onu aşamalı biçimde hızlandırmak mümkündür.

International Collegiate Programming Contest (ICPC) ise üç kişilik üniversite takımlarının süreye karşı yarıştığı bir formattır. Burada problem seçimi, hatasız uygulama ve takım koordinasyonu da algoritma bilgisi kadar önemlidir.

| Özellik | IOI | ICPC |
|---|---|---|
| Katılım | Bireysel | Üç kişilik takım |
| Puanlama | Genellikle kısmi puanlı | Çoğunlukla kabul veya ret |
| Tipik vurgu | Derin modelleme ve optimizasyon | Hızlı teşhis ve geniş konu yelpazesi |
| Klasikleşme biçimi | Yeni bir tekniği katman katman öğretmesi | Basit anlatımdan şaşırtıcı model çıkarması |

## IOI 2000: Post Office

**Post Office**, doğrusal bir yol üzerindeki köylere belirli sayıda postane yerleştirme problemidir. Amaç, her köyün en yakın postaneye uzaklıkları toplamını küçültmektir. Tek bir postanenin hizmet verdiği sıralı köy grubu için en iyi konum medyandır.

Köy konumları $x_l,\ldots,x_r$ ise grubun maliyeti

$$
C(l,r)=\sum_{i=l}^{r}\vert x_i-x_m\vert 
$$

şeklindedir; burada $m=\lfloor(l+r)/2\rfloor$ seçilebilir. Ardından bölümlemeli dinamik programlama gelir:

$$
dp[k][i]=\min_{0\le j<i}\left(dp[k-1][j]+C(j+1,i)\right).
$$

Bu soru klasikleşmiştir çünkü üç önemli fikri kusursuz biçimde birleştirir: sıralama, medyanın mutlak uzaklık için optimal oluşu ve aralıkları dinamik programlamayla bölme.

```cpp
for (int k = 1; k <= postaneSayisi; ++k) {
    for (int i = 1; i <= koySayisi; ++i) {
        for (int j = 0; j < i; ++j) {
            dp[k][i] = min(dp[k][i], dp[k - 1][j] + maliyet[j + 1][i]);
        }
    }
}
```

Bu çekirdek kod, ilk `i` köyü `k` postaneyle kapsamak için son grubun nerede başladığını dener. Asıl ustalık, `maliyet[l][r]` değerlerini önceden hesaplayarak geçişi ucuzlatmaktır.

## IOI 2011: Race

**Race**, ağırlıklı bir ağaçta toplam uzunluğu tam $K$ olan ve mümkün olan en az kenarı kullanan yolu arar. İlk bakışta bütün düğüm çiftlerini denemek doğal görünür; fakat bu yaklaşık $O(N^2)$ yol anlamına gelir.

Klasik çözüm centroid decomposition kullanır. Ağaç dengeli parçalara ayrılır; centroid’den alt ağaçlara olan uzaklıklar toplanır ve daha önce görülen $K-d$ uzaklığı aranır. Böylece çalışma süresi kabaca $O(N\log N)$ seviyesine iner. Problem, centroid decomposition tekniğini yalnızca sergilemediği, neden gerekli olduğunu hissettirdiği için efsanedir.

## ICPC klasiği: Tower of Cubes

1997 Dünya Finalleri ile özdeşleşen **Tower of Cubes**, renkli yüzlere sahip küpleri üst üste dizerken temas eden renklerin eşleşmesini ister. Hikâye fiziksel görünse de yapı, yönlendirilmiş en uzun yol problemine dönüşür. Her küpün altı olası yönelimi birer durumdur; bir yönelimden diğerine geçiş, üst ve alt renklerin uyuşmasına bağlıdır.

| Görünen hikâye | Algoritmik gerçek |
|---|---|
| Küpleri döndürmek | Durum üretmek |
| Renkleri eşleştirmek | Geçiş koşulu |
| En yüksek kule | En uzun yol / dinamik programlama |
| Küp sırasını korumak | Döngüsüz durum düzeni |

## Peki bir problem neden klasikleşir?

Klasik bir problem genellikle kısa anlatılır, birden fazla makul fakat yetersiz çözüm sunar ve çözüm bulunduğunda “Bunu nasıl göremedim?” duygusu yaratır. Dahası, kullanılan fikir başka problemlere taşınabilir: **Post Office** medyanı ve bölümlemeyi, **Race** dengeli ağaç ayrıştırmayı, **Tower of Cubes** ise hikâyeyi durum grafiğine çevirmeyi öğretir.

Efsane sorular geçmişin zor bilmeceleri değildir; algoritmik düşüncenin laboratuvarlarıdır. Onları çözerken yalnızca kabul işareti kazanmaz, bir sonraki bilinmeyen probleme bakmak için yeni bir gözlük edinirsiniz.
