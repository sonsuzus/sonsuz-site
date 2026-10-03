---
layout: post
title: "Teknoloji Borcu Faizi: Kötü Kod Ekip Moralini Nasıl Tüketir?"
math: true
categories: 
  - Bilgi
tags: 
  - teknoloji borcu
  - temiz kod
  - yazılım geliştirme
  - ekip kültürü
  - refactoring
  - teknik liderlik
toc: true
image: /img/teknoloji-borcu-faizi-42.png
---

Bir özelliği cuma akşamına yetiştirmek için eklenen masum bir `if`, geçici olduğu söylenen sabit bir değer ve test yazmadan yapılan hızlı bir düzeltme… İlk bakışta bunlar ekibe zaman kazandırır. Ancak “sonra düzeltiriz” denilen kod, çoğu zaman yıllarca sistemde yaşar. Üstelik yalnızca yazılımı değil, onunla çalışan geliştiricilerin sabrını, güvenini ve üretme isteğini de yavaşça tüketir.


![teknoloji-borcu-faizi-42](/img/teknoloji-borcu-faizi-42.svg)

``

## Teknoloji borcu neden gerçekten borçtur?

Teknoloji borcu, kısa vadeli hız uğruna gelecekte daha fazla çalışma maliyetini kabul etmektir. Finansal borçta ana para ve faiz bulunur; yazılımda ise ana para, ertelenen düzenleme işidir. Faiz de yeni bir değişiklik yapılırken ödenen ek analiz, hata ayıklama, test ve koordinasyon süresidir.

Bunu basitçe şöyle modelleyebiliriz:

$$
M(t) = B_0 + \sum_{i=1}^{t} F_i
$$

Burada $B_0$ başlangıçtaki düzeltme maliyetini, $F_i$ ise her geliştirme döneminde borç nedeniyle ödenen ek maliyeti gösterir. Kodun bağımlılıkları arttıkça faiz sabit kalmayabilir:

$$
F(t) = B_0(1+r)^t
$$

$r$, borcun yayılma oranıdır. Kötü tasarlanmış bir ödeme modülünün beş farklı servise bağlanması, küçük bir kusuru kurumsal bir boss savaşına dönüştürebilir.

| Kısa vadeli tercih | İlk etkisi | Uzun vadeli sonucu |
|---|---|---|
| Test yazmamak | Teslimat hızlanır | Hata korkusu ve manuel kontrol artar |
| Sabit değer kullanmak | Çözüm hemen çalışır | Ortam değişince sistem kırılır |
| Kopyala-yapıştır yapmak | Yeni akış çabuk eklenir | Aynı hata birçok yerde düzeltilir |
| Karmaşık metodu bırakmak | Refactoring ertelenir | Yeni geliştirici kodu anlayamaz |

## Kod kokusu nasıl moral kokusuna dönüşür?

Teknoloji borcunun psikolojik etkisi genellikle görünmezdir. Geliştirici, üç satırlık bir değişiklik için iki gün boyunca yan etkilerle uğraştığında kendi yeteneğini sorgulayabilir. Tahminler sürekli şaşar, ürün ekibi “Bu kadar küçük iş neden bitmedi?” diye sorar, geliştiriciler de baskının kaynağını birbirlerinde aramaya başlar.

Sonuçta şu döngü oluşur:

1. Karmaşık kod geliştirmeyi yavaşlatır.
2. Yavaşlama teslimat baskısını artırır.
3. Baskı daha fazla kestirme çözüm doğurur.
4. Yeni kestirmeler sistemi daha karmaşık hâle getirir.
5. Ekipte suçlama, savunma ve bıkkınlık başlar.

Bu nedenle teknoloji borcu yalnızca teknik bir metrik değildir; ekip sağlığı göstergesidir. Sürekli yangın söndüren insanlar zamanla iyileştirme önermeyi bırakır. “Nasıl olsa kabul edilmeyecek” düşüncesi, borcun en tehlikeli faizidir.

## Küçük bir örnek

Aşağıdaki fonksiyon hızlı çalışır, ancak iş kuralları büyüdükçe koşullar birbirine dolanır:

```javascript
function calculatePrice(user, total) {
  if (user.type === 'vip' && total > 1000) return total * 0.7;
  if (user.type === 'vip') return total * 0.8;
  if (total > 1000) return total * 0.9;
  return total;
}
```

Kuralların isimlendirilmesi, niyetin görünür olmasını ve ayrı ayrı test edilmesini sağlar:

```javascript
const discountRules = {
  vipLargeOrder: total => total * 0.7,
  vip: total => total * 0.8,
  largeOrder: total => total * 0.9
};

function calculatePrice(user, total) {
  if (user.type === 'vip' && total > 1000) return discountRules.vipLargeOrder(total);
  if (user.type === 'vip') return discountRules.vip(total);
  if (total > 1000) return discountRules.largeOrder(total);
  return total;
}
```

Bu değişiklik kusursuz bir mimari yaratmaz; fakat kuralları görünür kılar. Refactoring’in amacı kodu artistik hâle getirmek değil, değişikliğin zihinsel maliyetini azaltmaktır.

## Borcu yönetmek için ekip sözleşmesi

Her borç hemen kapatılmak zorunda değildir. Bilinçli alınmış, kaydedilmiş ve geri ödeme planı bulunan borç stratejik olabilir. Asıl tehlike, faizi ölçülmeyen görünmez borçtur.

| Sağlıksız yaklaşım | Sağlıklı yaklaşım |
|---|---|
| “Sonra düzeltiriz” | Takip kaydı ve hedef tarih oluşturmak |
| Borcu kişiye yüklemek | Tasarım kararını ekipçe değerlendirmek |
| Büyük temizlik projesi beklemek | Her özellikte küçük iyileştirme yapmak |
| Yalnızca teslimat hızını ölçmek | Hata, çevrim süresi ve morali birlikte izlemek |

Kod incelemelerinde suçlayıcı dil yerine “Bu karar gelecekte hangi değişiklikleri zorlaştırır?” sorusu kullanılmalıdır. Sprint kapasitesinin belirli bir bölümü bakım işlerine ayrılabilir ve kritik modüller için test güvenliği artırılabilir.

Teknoloji borcunu sıfırlamak gerçekçi değildir; onu görünür, ölçülebilir ve konuşulabilir yapmak ise mümkündür. Çünkü kötü kod önce derleme süresini değil, insanların hevesini uzatır. Sağlıklı ekipler yalnızca çalışan yazılım üretmez; yarın değiştirmekten korkmayacakları yazılım üretir.
