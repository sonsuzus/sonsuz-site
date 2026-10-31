---
layout: post
title: "Domatesin Dijital Pasaportu: Blok Zincir ile Tarladan Sofraya İzlenebilirlik"
math: true
categories: 
  - Bilgi
tags: 
  - blok zincir
  - tarım
  - izlenebilirlik
  - gıda güvenliği
  - javascript
  - tedarik zinciri
toc: true
image: /img/domatesin-dijital-pasaportu-50.png
---

![domatesin-dijital-pasaportu-50](/img/domatesin-dijital-pasaportu-50.svg)


Bir domatesin yolculuğu, market rafında başlamaz. Tarlada hasat edilir, paketlenir, kamyona yüklenir ve sonunda sofranıza ulaşır. Peki ambalajdaki “yerel üretim” iddiasını nasıl doğrulayabilirsiniz? Blok zincir, bu yolculuğun kayıtlarını farklı işletmeler arasında paylaşmayı ve sonradan yapılan değişiklikleri fark etmeyi sağlayabilir. Domatese dijital pasaport çıkarmaya hazır mısınız?

``

## Temel Mantık: Birbirine Bağlanan Kayıtlar

İzlenebilirlik, bir ürünün kim tarafından, nerede ve ne zaman işlendiğini takip edebilmektir. Klasik sistemlerde kayıtlar çoğunlukla ayrı veritabanlarında tutulur. Çiftçinin defteriyle lojistik firmasının tablosu uyuşmadığında, gerçeği bulmak dedektiflik işine dönüşebilir.

Blok zincirde işlemler, ortak kurallarla doğrulanan bir deftere eklenir. Bloklar önceki blokların kriptografik özetlerine bağlanır. Basitleştirilmiş bir olay zincirini şöyle düşünebiliriz:

$$h_i = H(h_{i-1} \Vert E_i)$$

Burada $E_i$ yeni olay, $H$ özet fonksiyonu, $h_i$ yeni özettir. $\Vert$ verilerin birleştirilmesini gösterir. Eski kayıtta küçük bir değişiklik bile özeti değiştirir. Ancak güvenlik yalnızca bu matematikten gelmez: dijital imzalar, doğrulayıcılar ve uzlaşma mekanizması da gerekir.

## Önce Ürünü Değil, Partiyi Tanımlayın

Her domatese ayrı kimlik vermek genellikle pahalıdır. Bunun yerine aynı hasattan gelen ürünler bir parti numarasıyla izlenebilir: `DOM-2026-042` gibi.

Her olay; parti kimliği, aşama, zaman, işletme kimliği, miktar ve konum referansı taşımalıdır. Parti bölünürse yeni alt partiler oluşturulur; karıştırılırsa kaynak partiler açıkça ilişkilendirilir. Yoksa dijital pasaport, yolculuğun yarısında hafızasını kaybeder!

| Aşama | Kaydedilen bilgi | Sağladığı fayda |
|---|---|---|
| Hasat | Tarla, tarih, üretici | Kaynağı belirleme |
| Paketleme | Parti, tesis, miktar | Bölünmeleri takip etme |
| Sevkiyat | Taşıyıcı, sıcaklık özeti | Soğuk zinciri denetleme |
| Teslim | Alıcı, zaman, kabul durumu | Sorumluluk devrini görme |

Miktar kontrolü de önemlidir. Basit bir denge için $Q_g = Q_c + Q_f + Q_k$ kullanılabilir: giren miktar; çıkan ürün, fire ve kalan stok toplamına eşit olmalıdır. Böylece 120 kilogram domatesten sihirli biçimde 180 kilogram ürün çıkması işaretlenir.

## Küçük Bir Kod Deneyi

Aşağıdaki Node.js örneği, bir olayın önceki özete bağlanmasını gösterir. Bu, çalışan bir blok zincir değil; kayıt bağlantısının öğretici bir modelidir.

```javascript
import { createHash } from "node:crypto";

const stages = new Set([
  "hasat", "paketleme", "sevkiyat", "teslim"
]);

function makeRecord(previousHash, event) {
  if (!stages.has(event.stage)) {
    throw new Error("Geçersiz aşama");
  }
  if (!(event.quantityKg > 0)) {
    throw new Error("Miktar pozitif olmalı");
  }

  const payload = JSON.stringify([
    event.batchId, event.stage, event.time,
    event.actorId, event.quantityKg
  ]);
  const hash = createHash("sha256")
    .update(previousHash + payload)
    .digest("hex");

  return { previousHash, payload, hash };
}

const harvest = makeRecord("0".repeat(64), {
  batchId: "DOM-2026-042", stage: "hasat",
  time: "2026-10-06T08:00:00Z",
  actorId: "ciftci-17", quantityKg: 120
});
console.log(harvest.hash);
```

Sabit alan sırası, aynı verinin aynı özeti üretmesine yardımcı olur. Sonraki olayda `previousHash` olarak `harvest.hash` kullanılır. Gerçek uygulamada şema doğrulaması, yetkilendirme ve imza kontrolü eklenmelidir. Tek kişinin yönettiği bu örnek zincir baştan hesaplanabilir; onu ortak uzlaşmayla korunan ağla karıştırmayın.

## Değiştirilemezlik, Doğruluk Demek Değildir

Sensör yanlış ölçüyorsa blok zincir yanlış sıcaklığı sadakatle saklar. Buna fiziksel dünya ile dijital kayıt arasındaki güven problemi diyebiliriz. Kalibrasyon, mühürlü ambalaj, denetim ve güvenilir veri girişleri hâlâ gereklidir.

“Değiştirilemez” ifadesi de koşulludur: geçmişin değiştirilmesi ağın güvenlik varsayımları altında zorlaştırılır. Hatalı kayıt silinmek yerine, önceki olaya referans veren düzeltme işlemiyle tamamlanır.

| Yaklaşım | Avantaj | Dikkat noktası |
|---|---|---|
| Merkezi veritabanı | Basit, hızlı, ekonomik | Yöneticiye güven gerekir |
| İzinli blok zincir | Kurumlar arası ortak doğrulama | Katılımcı yönetimi gerekir |
| Açık blok zincir | Geniş doğrulanabilirlik | Ücret ve gizlilik değerlendirilir |

## Pilot Projeyi Nasıl Kurarsınız?

Bir üretici, paketleme tesisi ve marketle başlayın. Belgeleri ve ayrıntılı sensör verilerini erişim kontrollü depoda tutun; zincire özetlerini ve gerekli referansları yazın. Özet, belgenin değiştiğini gösterebilir ama belgenin erişilebilirliğini garanti etmez.

Ambalajdaki QR kod, tüketiciyi izlenebilirlik ekranına götürsün. Ticari sırları herkese açmadan köken ve aşamaları gösterin. Başarıyı işlem sayısıyla değil; geri çağırma süresi, kayıt eksikliği ve doğrulama maliyetiyle ölçün. Amaç domatesi teknolojiyle süslemek değil, sorun çıktığında doğru partiyi hızla bulmaktır.
