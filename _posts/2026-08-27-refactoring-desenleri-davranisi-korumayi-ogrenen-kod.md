---
layout: post
title: "Refactoring Desenleri: Davranışı Korumayı Öğrenen Kod"
math: true
categories: 
  - Bilgi
tags: 
  - refactoring
  - temiz kod
  - yazılım geliştirme
---

Bir kod tabanını iyileştirmek, her zaman yeni özellik eklemek anlamına gelmez. Bazen en değerli geliştirme; çalışan ama okunması zor, genişletmesi pahalı ve hata üretmeye yatkın kodu daha anlaşılır hâle getirmektir. Refactoring, dışarıdan gözlemlenen davranışı değiştirmeden kodun iç tasarımını düzenleme disiplinidir. Amaç yalnızca “güzel kod” yazmak değil; gelecekteki değişikliklerin maliyetini ve riskini azaltmaktır.
``

Refactoring ile yeniden yazımı ayırmak önemlidir. Yeniden yazımda çözümün mimarisi, teknolojisi veya davranışı kökten değişebilir. Refactoring ise küçük, güvenli ve doğrulanabilir adımlarla ilerler. Bu yaklaşımın temel denklemi şöyle özetlenebilir:

$$Davranış_{önce} = Davranış_{sonra}$$

Buradaki davranış; dönen değerler, yan etkiler, hata durumları, API sözleşmeleri ve kullanıcıya görünen çıktıları kapsar. Kodun satır sayısının azalması tek başına başarı değildir; değişikliğin güvenle yapılabilmesi başarıdır.

| Kavram | Ana hedef | Risk seviyesi | Tipik örnek |
|---|---|---:|---|
| Refactoring | İç yapıyı iyileştirmek | Düşük | Uzun metodu bölmek |
| Bug fix | Hatalı davranışı düzeltmek | Orta | Yanlış hesaplamayı düzeltmek |
| Yeni özellik | Yeni davranış eklemek | Orta/Yüksek | Kupon sistemi eklemek |
| Rewrite | Sistemi yeniden kurmak | Yüksek | Eski uygulamayı baştan yazmak |

## Güvenlik ağı: Testler

Refactoring’in yakıtı test, emniyet kemeri ise otomasyondur. Değişiklikten önce mevcut davranışı yakalayan testler bulunmalıdır. Test yoksa önce karakterizasyon testi yazmak akıllıcadır: Kodun şu an ne yaptığını, ideal olarak ne yapması gerektiğini değil, ölçülebilir biçimde kaydeder.

Örneğin aşağıdaki kod hem indirim mantığını hem de çıktı üretimini tek yerde topluyor:

```javascript
function printOrder(customer, total) {
  let discount = 0;
  if (customer.type === "gold") discount = total * 0.20;
  else if (customer.type === "silver") discount = total * 0.10;

  const payable = total - discount;
  console.log(`${customer.name}: ${payable} TL`);
  return payable;
}
```

İlk refactoring adımı, hesaplamayı yan etkiden ayırmaktır. **Extract Function** deseniyle hesaplama ayrı bir fonksiyona taşınır:

```javascript
function calculateDiscount(customer, total) {
  if (customer.type === "gold") return total * 0.20;
  if (customer.type === "silver") return total * 0.10;
  return 0;
}

function printOrder(customer, total) {
  const payable = total - calculateDiscount(customer, total);
  console.log(`${customer.name}: ${payable} TL`);
  return payable;
}
```

Bu dönüşümün kazancı, `calculateDiscount` fonksiyonunun konsol çıktısına ihtiyaç duymadan test edilebilmesidir. Ayrıca indirim kuralları büyüdüğünde ilgili değişiklik tek bir noktada yapılır.

## Sık kullanılan desenler

Refactoring desenleri, kod kokularına verilen küçük reçetelerdir. Her kokunun tek bir çözümü yoktur; bağlam karar verir.

| Kod kokusu | Uygun desen | Beklenen fayda |
|---|---|---|
| Çok uzun fonksiyon | Extract Function | Okunabilirlik ve test edilebilirlik |
| Anlamsız değişken adı | Rename Variable | Niyetin görünür olması |
| Tekrarlanan bloklar | Extract Function / Pull Up Method | Tek doğruluk kaynağı |
| Devasa koşul zinciri | Replace Conditional with Polymorphism | Yeni kural ekleme kolaylığı |
| Fazla parametre | Introduce Parameter Object | Daha anlamlı arayüz |

Özellikle **Rename** küçümsenmemelidir. `x`, `data` veya `flag` gibi isimler, okuyucuyu zihinsel tersine mühendisliğe zorlar. İyi bir isim, yorum satırına duyulan ihtiyacı azaltır. Buna karşılık her satırı soyutlamak da zararlıdır: Aşırı parçalanmış kodda asıl akışı takip etmek zorlaşabilir.

Sağlıklı çalışma döngüsü basittir: önce testleri çalıştırın, tek küçük dönüşüm yapın, testleri yeniden çalıştırın ve değişikliği kaydedin. Risk kabaca değişiklik büyüklüğüyle artar: $Risk \propto Değişen\ Alan$. Bu yüzden “bir kerede temizlik” yerine kısa iterasyonlar tercih edilir.

Sonuçta refactoring, estetik bir hobi değil; yazılımın değişime direnç göstermesini azaltan mühendislik pratiğidir. Kod bugün çalışıyor olabilir. Asıl soru şudur: Yarın yeni bir kural geldiğinde, onu korkmadan değiştirebilecek misiniz?
