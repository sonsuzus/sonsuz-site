---
layout: post
title: "Semantic Versioning: Sürüm Numaralarının Gizli Dili"
math: true
categories: 
  - Bilgi
tags: 
  - semantic-versioning
  - semver
  - yazılım-sürümleri
---

Bir paketin `2.4.1` sürümünü gördüğünüzde bunun sadece üç rastgele sayı olduğunu düşünmek kolaydır. Oysa doğru kullanıldığında bu numara, güncellemenin projenizi bozup bozmayacağına dair güçlü bir sözleşmedir. Semantic Versioning (SemVer), geliştiriciler, paket yöneticileri ve kullanıcılar arasında ortak bir dil kurar: Yeni özellik mi geldi, hata mı düzeldi, yoksa mevcut entegrasyonlar tehlikede mi?
``
SemVer’in temel biçimi `MAJOR.MINOR.PATCH` şeklindedir. Matematiksel olarak bir sürümü $V=(M,m,p)$ üçlüsüyle ifade edebiliriz. Burada $M$ ana sürüm, $m$ küçük sürüm ve $p$ yama sürümüdür. Sürüm karşılaştırması soldan sağa yapılır: Önce ana sürüme, eşitse küçük sürüme, o da eşitse yamaya bakılır. Bu nedenle $2.10.0 > 2.9.9$ olur; sayılar metin değil, sayısal değerlerdir.

En önemli kavram **geriye uyumluluk**tur. Bir kütüphanenin eski kullanıcı kodlarını çalıştırmaya devam etmesi, geriye uyumlu olduğu anlamına gelir. Örneğin `calculateTotal()` fonksiyonuna isteğe bağlı bir parametre eklemek çoğunlukla uyumludur. Buna karşılık fonksiyonun adını değiştirmek veya dönüş tipini tamamen farklılaştırmak, kullanıcıların kodunu kırabilir.

| Bölüm | Ne zaman artar? | Örnek değişiklik | Kullanıcı için anlamı |
|---|---|---|---|
| `MAJOR` | Geriye uyumsuz değişiklikte | Bir API metodunun kaldırılması | Kod güncellemesi gerekebilir |
| `MINOR` | Uyumlu yeni özellikte | Yeni, isteğe bağlı endpoint | Güvenle yeni yetenek kullanılabilir |
| `PATCH` | Uyumlu hata düzeltmesinde | Hatalı doğrulamanın düzeltilmesi | Güncellemek genellikle güvenlidir |

Örneğin `1.3.5` sürümünde çalışan bir API düşünelim. Sadece ödeme hesaplamasındaki yuvarlama hatasını düzeltiyorsanız sürüm `1.3.6` olmalıdır. Yeni bir `refundPayment()` endpoint’i eklediyseniz `1.4.0` mantıklıdır. Ancak `createPayment()` metodunun parametrelerini zorunlu biçimde değiştiriyorsanız `2.0.0` yayınlamalısınız. Kuralı kısa bir karar ağacı gibi düşünebilirsiniz:

```text
Geriye uyumsuz değişiklik var mı?
├─ Evet: MAJOR artır, MINOR ve PATCH sıfırla
└─ Hayır: Yeni uyumlu özellik var mı?
   ├─ Evet: MINOR artır, PATCH sıfırla
   └─ Hayır: PATCH artır
```

Bu yapı özellikle `npm`, `Composer`, `pip` ve `Maven` gibi paket ekosistemlerinde hayat kurtarır. Bağımlılık aralıkları, hangi güncellemelerin otomatik alınabileceğini sürüm numarasına göre belirler. JavaScript dünyasında örneğin şu ifade yaygındır:

```json
{
  "dependencies": {
    "example-lib": "^1.4.2"
  }
}
```

Buradaki `^1.4.2`, çoğu araçta `>=1.4.2` ve `<2.0.0` anlamına gelir. Yani hata düzeltmeleri ve uyumlu özellikler alınabilir; olası kırıcı `2.0.0` güncellemesi otomatik gelmez. Bu, teoride güzel görünen SemVer’in pratikte neden kritik olduğunu gösterir: Paket yöneticisi, sizin verdiğiniz sözlere göre risk hesabı yapar.

Ön sürümler de bu dilin parçasıdır. `2.0.0-alpha.1`, `2.0.0-beta.2` ve `2.0.0-rc.1` gibi ekler, sürümün henüz üretim için tam kararlı olmayabileceğini söyler. Genel akış şöyledir:

| Ek | Amaç | Kararlılık |
|---|---|---|
| `alpha` | Erken geliştirme ve deney | Düşük |
| `beta` | Özellikleri büyük ölçüde tamamlanmış test | Orta |
| `rc` | Yayın adayı, son kontroller | Yüksek |
| Ek yok | Kararlı üretim sürümü | En yüksek |

SemVer kullanırken iki disiplin şarttır. Birincisi, herkese açık API’nin ne olduğunu açıkça belgelemektir; belgelenmemiş davranışların kullanıcı tarafından kullanılmayacağını varsaymak risklidir. İkincisi ise değişiklik kayıtlarını (`CHANGELOG`) sürüm numaralarıyla birlikte tutmaktır. İnsanlar `3.1.0` gördüğünde ne kazanacaklarını, `4.0.0` gördüğünde ise neyi değiştirmeleri gerektiğini hızla anlayabilmelidir.

Sonuçta Semantic Versioning, sayıları büyütme ritüeli değil; güven inşa etme mekanizmasıdır. Sürüm numaranız ne kadar dürüstse, kullanıcılarınızın güncelleme tuşuna basması da o kadar cesur olur.
