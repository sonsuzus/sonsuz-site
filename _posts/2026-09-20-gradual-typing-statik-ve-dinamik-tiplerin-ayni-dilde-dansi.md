---
layout: post
title: "Gradual Typing: Statik ve Dinamik Tiplerin Aynı Dilde Dansı"
math: true
categories: 
  - Bilgi
tags: 
  - gradual typing
  - tip sistemleri
  - typescript
  - python
  - statik analiz
  - programlama dilleri
toc: true
image: /img/gradual-typing-statik-32.png
---

Bir programlama dili hem özgür ruhlu hem de disiplinli olabilir mi? Gradual Typing, yani kademeli tipleme, bu soruya güçlü bir “evet” yanıtı verir. Geliştiriciye dinamik tiplerin esnekliğini sunarken ihtiyaç duyulan bölgelerde statik tip denetimini devreye sokar. Böylece mevcut bir projeyi baştan yazmadan, tip güvenliğini adım adım artırmak mümkün olur.

``

## İki dünyanın kısa özeti

Statik tip sistemlerinde değişkenlerin ve ifadelerin türleri çoğunlukla program çalıştırılmadan önce denetlenir. Dinamik sistemlerde ise tip uyuşmazlıkları çalışma zamanında ortaya çıkar. Gradual Typing, programın bazı parçalarını statik, bazılarını dinamik bırakmamıza izin verir.

| Özellik | Statik tipleme | Dinamik tipleme | Kademeli tipleme |
|---|---|---|---|
| Tip kontrolü | Derleme veya analiz zamanı | Çalışma zamanı | Her iki aşamada |
| Başlangıç hızı | Daha fazla tanım gerekebilir | Genellikle hızlıdır | İhtiyaca göre değişir |
| Hata yakalama | Erken | Geç | Tiplendirilen bölgelerde erken |
| Esneklik | Görece düşük | Yüksek | Dengeli |
| Örnek | Java, Rust | JavaScript, Ruby | TypeScript, Python type hints |

Basitçe, bir programdaki statik olarak bilinen değerlerin oranını $s$, dinamik bırakılanların oranını $d$ kabul edersek:

$$s + d = 1$$

Kademeli tiplemede geliştirici, proje olgunlaştıkça $s$ değerini yükseltebilir. Ancak amaç her zaman $s=1$ yapmak değildir; kritik olmayan veya doğası gereği dinamik bölgeler bilinçli biçimde korunabilir.

## Köprü görevi gören dinamik tip

Bu yaklaşımın merkezinde çoğunlukla `any`, `dynamic` veya benzer isimli özel bir tip bulunur. Bu tip, statik sistem ile dinamik değerler arasında bir kaçış kapısıdır. TypeScript örneğine bakalım:

```typescript
function etiketle(deger: any): string {
  return "Değer: " + deger.toUpperCase();
}

console.log(etiketle("merhaba"));
console.log(etiketle(42)); // Derlenebilir, fakat çalışma zamanında patlar.
```

`any`, derleyicinin kontrollerini büyük ölçüde kapatır. Bu nedenle özgürlük sağlar ama güvenlik kemerini de çözer. TypeScript’in `unknown` tipi daha temkinli bir alternatiftir:

```typescript
function guvenliEtiketle(deger: unknown): string {
  if (typeof deger === "string") {
    return "Değer: " + deger.toUpperCase();
  }
  return "Metin olmayan değer";
}
```

Burada tip daraltma sayesinde `toUpperCase` yalnızca değerin metin olduğu kanıtlandıktan sonra çağrılır. Statik analiz, çalışma zamanındaki kontrolle iş birliği yapar.

## Sınırlar ve çalışma zamanı kontrolleri

Statik ve dinamik bölgeler karşılaştığında bir **tip sınırı** oluşur. Dinamik kaynaktan gelen bir değerin statik bölgeye aktarılması sırasında sistem açık kontroller, örtük dönüşümler veya çalışma zamanı sözleşmeleri kullanabilir.

Örneğin bir API’den gelen JSON verisi derleme sırasında kesin olarak bilinemez:

```typescript
type Kullanici = {
  id: number;
  ad: string;
};

function kullaniciMi(veri: unknown): veri is Kullanici {
  if (typeof veri !== "object" || veri === null) return false;
  const aday = veri as Record<string, unknown>;
  return typeof aday.id === "number" && typeof aday.ad === "string";
}
```

Bu fonksiyon, dinamik veriyi doğrulayarak statik dünyaya güvenli biçimde taşır. Yalnızca `as Kullanici` yazmak ise kanıt sunmaz; derleyiciye “bana güven” demektir.

## Gradual Guarantee nedir?

Kademeli tiplemenin önemli kuramsal hedeflerinden biri **Gradual Guarantee** ilkesidir. Bir programdan bazı tip açıklamaları kaldırıldığında program aniden anlamsız hâle gelmemeli; daha dinamik davranmaya başlamalıdır. Ters yönde, tip bilgisi eklemek programın kabul ettiği değerleri daraltabilir ve hataları erkenden görünür kılabilir.

Bunu sezgisel olarak şöyle ifade edebiliriz:

$$\text{daha fazla tip bilgisi} \Rightarrow \text{daha güçlü erken doğrulama}$$

Yine de bütün diller bu ilkeyi kusursuz uygulamaz. Tip çıkarımı, dönüşümler ve dilin mevcut davranışları sonucu etkileyebilir.

## Ne zaman tercih edilmeli?

Gradual Typing özellikle büyük JavaScript veya Python projelerinde, eski kod tabanlarının aşamalı modernizasyonunda ve farklı güven seviyelerine sahip modüllerin birlikte çalışmasında değerlidir. En sağlıklı strateji; önce dış veri sınırlarını, ortak modelleri ve kritik iş kurallarını tiplendirmektir. Kısacası kademeli tipleme, “ya tamamen statik ya tamamen dinamik” kavgasını bitirir: Kod tabanına bir anda takım elbise giydirmek yerine, önce kravatı takar.

![gradual-typing-statik-32](/img/gradual-typing-statik-32.svg)

