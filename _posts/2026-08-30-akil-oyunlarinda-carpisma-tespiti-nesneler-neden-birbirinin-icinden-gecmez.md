---
layout: post
title: "Akıl Oyunlarında Çarpışma Tespiti: Nesneler Neden Birbirinin İçinden Geçmez?"
math: true
categories: 
  - Bilgi
tags: 
  - oyun geliştirme
  - çarpışma tespiti
  - geometri
  - 2D matematik
---

Bir 2D akıl oyununda kutunun duvardan geçmemesi, taşların aynı kareyi paylaşmaması veya oyuncunun engelde durması ilk bakışta basit görünür. Ancak bu davranışın arkasında geometri, vektör matematiği ve doğru zamanlama vardır. Çarpışma tespiti iki soruya cevap verir: Nesneler temas ediyor mu? Ediyorsa, oyun onları nasıl ayırmalı? İlk soru **algılama** (detection), ikinci soru ise **çözümleme** (resolution) aşamasıdır.

``

En temel yaklaşım, nesneleri eksenlere hizalı dikdörtgenlerle, yani **AABB** (*Axis-Aligned Bounding Box*) ile temsil etmektir. Bir dikdörtgenin sol, sağ, üst ve alt sınırları biliniyorsa iki nesnenin çakışması kolayca bulunur. A nesnesi B'nin solunda kalıyorsa ya da tamamen üstündeyse çarpışma yoktur. Bunun tersi durumların hiçbiri geçerli değilse dikdörtgenler kesişir.

Matematiksel olarak A ve B için şu koşul çarpışmayı ifade eder:

$$A_{sol} < B_{sağ} \land A_{sağ} > B_{sol} \land A_{üst} < B_{alt} \land A_{alt} > B_{üst}$$

Bu testin güzel yanı, sabit zamanda çalışmasıdır: $O(1)$. Sokoban benzeri kare tabanlı bulmacalarda çoğu zaman daha da kolay bir çözüm uygulanır: Dünya bir ızgaradır ve her hücre dolu veya boştur. Oyuncu hareket etmeden önce hedef hücrenin duvar, kutu ya da boş alan olup olmadığına bakılır. Böylece çarpışmayı sonradan düzeltmek yerine, geçersiz hareket en baştan reddedilir.

| Yaklaşım | En uygun kullanım | Güçlü yanı | Sınırı |
|---|---|---|---|
| Izgara/hücre kontrolü | Sokoban, labirent, karo oyunları | Çok hızlı ve anlaşılır | Serbest, çapraz hareketlerde kaba kalır |
| AABB | Platform, üstten görünüşlü oyunlar | Ucuz hesaplama, kolay kod | Dönen nesneleri iyi sarmaz |
| Daire çarpışması | Toplar, menzil alanları | Doğal ve simetrik | Köşeli objelerde hatalı his verebilir |
| SAT | Dönen çokgenler | Daha hassas geometri | Uygulaması ve maliyeti daha yüksektir |

Daireler için mantık merkezler arası uzaklığa dayanır. Merkez farkı $\vec{d} = \vec{p_B} - \vec{p_A}$ olsun. Çarpışma için kareli uzaklığın yarıçapların toplamının karesinden küçük olması yeterlidir:

$$d_x^2 + d_y^2 < (r_A + r_B)^2$$

Karekök almamak küçük ama değerli bir optimizasyondur. Özellikle ekranda onlarca nesne varsa, her karede yapılan gereksiz $\sqrt{x}$ hesapları birikir.

AABB çarpışmasını kontrol edip oyuncuyu engelin dışına iten orta seviye bir örnek şöyledir:

```javascript
function resolveAABB(player, wall) {
  const overlapX = Math.min(player.x + player.w, wall.x + wall.w) -
                   Math.max(player.x, wall.x);
  const overlapY = Math.min(player.y + player.h, wall.y + wall.h) -
                   Math.max(player.y, wall.y);

  if (overlapX <= 0 || overlapY <= 0) return false;

  // En az nüfuz edilen eksende geri itmek, doğal bir duvar tepkisi üretir.
  if (overlapX < overlapY) {
    player.x += player.x < wall.x ? -overlapX : overlapX;
  } else {
    player.y += player.y < wall.y ? -overlapY : overlapY;
  }
  return true;
}
```

Bu kod yalnızca temas var mı diye bakmaz; en küçük çakışma miktarını seçerek oyuncuyu uygun yönde dışarı taşır. Buna **minimum translation vector** fikrinin sade bir versiyonu denebilir. Fakat hızlı hareket eden nesnelerde yeni bir sorun doğar: Nesne bir karede duvarın önünde, sonraki karede arkasında olabilir. Buna *tunneling* denir.

Çözüm, hareketi küçük adımlara bölmek veya **sürekli çarpışma tespiti** kullanmaktır. Sürekli yöntemde konum yerine zaman aralığı incelenir; nesnenin duvara ilk temas ettiği $t \in [0,1]$ bulunur. Akıl oyunlarında genellikle hamle tabanlı yapı veya küçük hızlar yeterlidir. Yine de temel ilke değişmez: Önce geniş ve ucuz bir testle adayları ele, sonra hassas testi uygula, en sonunda nesneleri tutarlı bir kuralla ayır. Böylece hem matematik hem oyun hissi çarpışmadan kurtulur.
