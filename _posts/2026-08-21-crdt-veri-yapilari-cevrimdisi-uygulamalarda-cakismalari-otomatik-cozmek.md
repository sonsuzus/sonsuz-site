---
layout: post
title: "CRDT Veri Yapıları: Çevrimdışı Uygulamalarda Çakışmaları Otomatik Çözmek"
math: true
categories: 
  - Bilgi
tags: 
  - crdt
  - dağıtık sistemler
  - çevrimdışı uygulamalar
image: /img/crdt-veri-yapilari-29.png
---

Bir not alma uygulamasını iki telefonda, internet bağlantısı olmadan kullandığınızı düşünün. Aynı notu bir cihazda silerken diğerinde yeni bir madde eklediniz. Bağlantı geri geldiğinde klasik bir sistem genellikle “hangi sürüm doğru?” diye panikler. CRDT'ler ise bu tartışmayı matematiksel kurallarla çözer: Her cihaz değişiklik yapabilir, ardından veriler sıradan bağımsız biçimde birleşerek aynı sonuca ulaşır.

![crdt-veri-yapilari-29](/img/crdt-veri-yapilari-29.svg)

``

CRDT, **Conflict-free Replicated Data Type** yani “çatışmasız çoğaltılmış veri tipi” anlamına gelir. Temel hedefi, birden fazla kopyada tutulan verinin ağ gecikmesi, paket kaybı veya çevrimdışı çalışma gibi koşullarda bile sonunda yakınsamasıdır. Bu özellik **eventual consistency** olarak bilinir. Kritik fikir şudur: Sistem her değişikliği anında herkese ulaştıramasa da, tüm replikalar aynı güncellemeleri gördüğünde aynı duruma erişmelidir.

Matematik tarafında CRDT'lerin süper gücü, birleştirme işleminin bazı güvenli özellikler taşımasıdır. Durum tabanlı bir CRDT için birleştirme operatörünü $\sqcup$ ile gösterelim. İdeal olarak şu kurallar geçerlidir:

$$a \sqcup b = b \sqcup a$$
$$a \sqcup (b \sqcup c) = (a \sqcup b) \sqcup c$$
$$a \sqcup a = a$$

Bunlar sırasıyla değişme, birleşme ve idempotentlik özellikleridir. Yani güncellemelerin geliş sırası sonucu değiştirmez; paket tekrar gelse bile veri iki kez uygulanmış gibi davranmaz. Dağıtık sistemlerin kaotik dünyasında oldukça huzur verici bir sözleşmedir.

| Yaklaşım | Çakışma stratejisi | Çevrimdışı deneyim | Tipik risk |
|---|---|---|---|
| Merkezi kilit | Tek yazarı bekler | Zayıf | Kullanıcı engellenir |
| Last Write Wins | En yeni zaman damgasını seçer | İyi | Değerli veri kaybolabilir |
| CRDT | Birleştirilebilir işlemler | Çok iyi | Modelleme maliyeti artar |

CRDT'ler iki ana aileye ayrılır. **State-based** ya da CvRDT yaklaşımında cihazlar mevcut durumlarını paylaşır ve alıcı bunları `merge` fonksiyonuyla birleştirir. **Operation-based** ya da CmRDT yaklaşımında ise “ekle”, “sil”, “artır” gibi operasyonlar yayılır. İlki ağda daha fazla veri taşıyabilir; ikincisi ise operasyonların güvenilir ve çoğu zaman en az bir kez teslim edilmesini ister.

En kolay örnek G-Counter'dır: Sadece artan dağıtık sayaç. Her replikada, her düğüm için ayrı bir sayaç tutulur. Bir cihaz yalnızca kendi hücresini artırır. Birleşimde her hücre için maksimum değer alınır; toplam sayaç da hücrelerin toplamıdır.

```javascript
// State-based G-Counter: her cihaz kendi alanını artırır
function increment(counter, replicaId) {
  return {
    ...counter,
    [replicaId]: (counter[replicaId] ?? 0) + 1
  };
}

function merge(left, right) {
  const ids = new Set([...Object.keys(left), ...Object.keys(right)]);
  return Object.fromEntries(
    [...ids].map(id => [id, Math.max(left[id] ?? 0, right[id] ?? 0)])
  );
}

function value(counter) {
  return Object.values(counter).reduce((sum, n) => sum + n, 0);
}
```

Örneğin `A: 2` ve `B: 3` durumları birleşince değer $2+3=5$ olur. Aynı durum paketi tekrar alınırsa `max` işlemi nedeniyle sayaç şişmez. Ancak bu model yalnızca artırmayı destekler. Azaltma gerektiğinde pozitif ve negatif sayacı ayrı ayrı tutan PN-Counter kullanılır.

Metin düzenleme, görev listeleri ve ortak beyaz tahtalar daha karmaşıktır. Bir eleman silinmişken başka cihazdan düzenlenmiş olabilir. Burada **OR-Set** gibi yapılar her eklemeye benzersiz kimlik verir; silme işlemi hangi ekleme kimliğini kaldırdığını kaydeder. Böylece “aynı ada sahip iki görev” ile “aynı görevin iki kopyası” arasındaki fark korunur.

| Veri ihtiyacı | Uygun CRDT örneği | Not |
|---|---|---|
| Beğeni sayısı | G-Counter | Sadece artırma |
| Stok farkı veya oy | PN-Counter | Artı ve eksi ayrı izlenir |
| Etiket listesi | OR-Set | Ekleme/silme çakışmalarına dayanıklı |
| Ortak metin | Sequence CRDT | Karakter ya da blok sırası korunur |

CRDT seçerken “çatışmayı tamamen yok ediyor” yanılgısına düşmeyin. CRDT teknik çakışmayı deterministik biçimde çözer; ürün kararını değil. Aynı takvim saatine iki toplantı eklenmesi veri bozulması değildir, fakat kullanıcı açısından anlamsız olabilir. Bu tür iş kuralları için ek doğrulama, sunucu otoritesi veya kullanıcıya seçim sunan arayüz gerekir. Doğru model ve doğru ürün kuralı birleştiğinde CRDT'ler, çevrimdışı deneyimi bir istisna olmaktan çıkarıp uygulamanın doğal yeteneğine dönüştürür.
