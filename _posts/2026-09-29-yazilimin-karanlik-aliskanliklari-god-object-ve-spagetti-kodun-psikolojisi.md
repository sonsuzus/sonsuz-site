---
layout: post
title: "Yazılımın Karanlık Alışkanlıkları: God Object ve Spagetti Kodun Psikolojisi"
math: true
categories: 
  - Bilgi
tags: 
  - anti-pattern
  - god-object
  - spagetti-kod
  - refactoring
  - temiz-kod
  - yazılım-mimarisi
toc: true
image: /img/yazilimin-karanlik-aliskanliklari-18.png
---

Bir sınıfın kullanıcı doğrulamasından e-posta göndermeye, fatura hesaplamaktan veritabanı temizlemeye kadar her işi üstlendiğini düşünün. İlk bakışta bu sınıf oldukça “yetenekli” görünebilir. Gerçekte ise ekipteki herkesin çekindiği, en ufak değişiklikte üç farklı modülü bozan bir **God Object** doğmuştur. Kontrol akışı takip edilemeyen koşullar, iç içe döngüler ve rastgele bağımlılıklar da tabloya eklenince menüde spagetti kod vardır.
``

## God Object ve spagetti kod nedir?

**God Object**, sistem hakkında gereğinden fazla bilgiye ve sorumluluğa sahip sınıf ya da modüldür. Spagetti kod ise akışın ve modül sınırlarının belirsiz olduğu, bir değişikliğin nereleri etkileyeceğinin kolayca öngörülemediği yapıdır.

| Özellik | God Object | Spagetti kod |
|---|---|---|
| Temel sorun | Sorumlulukların tek yerde toplanması | Kontrol ve bağımlılık akışının karmaşası |
| Belirti | Çok büyük sınıf, çok sayıda metot | Derin koşullar, tekrarlar, gizli yan etkiler |
| Risk | Yüksek bağımlılık | Düşük okunabilirlik ve öngörülebilirlik |
| Çözüm yönü | Sorumlulukları ayırmak | Akışı sadeleştirmek ve sınırlar oluşturmak |

![yazilimin-karanlik-aliskanliklari-18](/img/yazilimin-karanlik-aliskanliklari-18.svg)


Bir modülün değişme riskini kabaca şöyle düşünebiliriz:

$$R \propto C \times D \times S$$

Burada $C$ karmaşıklığı, $D$ bağımlılık sayısını, $S$ ise modülün sorumluluk sayısını temsil eder. Bu bilimsel bir üretim formülü değildir; fakat üç değer birlikte büyüdüğünde bakım riskinin neden hızla arttığını anlatan kullanışlı bir zihinsel modeldir.

## Bu kodlar neden yazılıyor?

Sorun çoğu zaman geliştiricinin bilgisizliği değil, kısa vadeli baskılar ve insan psikolojisidir.

- **Hemen bitirme dürtüsü:** Yeni davranışı mevcut büyük sınıfa eklemek, doğru soyutlamayı tasarlamaktan daha hızlı görünür.
- **Belirsizlikten kaçınma:** Yeni bir servis veya modül oluşturmak karar vermeyi gerektirir. Tanıdık dosyaya birkaç metot eklemek daha güvenlidir.
- **Batık maliyet yanılgısı:** “Bu sınıf zaten büyük, bir metottan ne olacak?” düşüncesi büyümeyi normalleştirir.
- **Kahraman geliştirici etkisi:** Sistemin karmaşıklığını yalnızca birkaç kişinin anlayabilmesi, yanlışlıkla uzmanlık göstergesi sayılabilir.
- **Test eksikliği:** Güvenlik ağı olmayınca kimse kodu taşımaya cesaret edemez; dokunulmayan kod daha da büyür.

Sonuçta teknik borç, finansal borç gibi faiz üretir. Basit bir modelle toplam maliyet $M$, ilk kısa yol maliyeti $B$ ve değişiklik başına faiz $f$ ise:

$$M = B(1+f)^n$$

$n$ değişiklik sayısı arttıkça başlangıçta kazanılan birkaç saat, haftalar süren hata ayıklamaya dönüşebilir.

## Kontrollü bir refactoring stratejisi

Devasa sınıfı bir gecede parçalamak risklidir. Önce davranışı karakterizasyon testleriyle sabitlemek gerekir. Ardından birlikte değişen alanlar ve metotlar belirlenerek küçük sorumluluk kümeleri çıkarılabilir.

```java
class OrderService {
    private final PriceCalculator calculator;
    private final PaymentGateway paymentGateway;
    private final ReceiptSender receiptSender;

    Receipt checkout(Order order) {
        Money total = calculator.calculate(order);
        paymentGateway.charge(order.customer(), total);
        return receiptSender.send(order, total);
    }
}
```

Bu örnekte `OrderService` süreci koordine eder; fiyat hesaplama, ödeme ve bildirim ayrıntılarını sahiplenmez. Böylece her bileşen ayrı test edilebilir ve değiştirilme nedenleri ayrışır.

Spagetti akışı düzeltirken uzun metotları bölmek, erken dönüş kullanmak ve gizli global durumu kaldırmak etkilidir:

```python
def approve_application(application):
    if not application.is_complete():
        return Rejection("Eksik başvuru")

    score = calculate_score(application)
    if score < MINIMUM_SCORE:
        return Rejection("Yetersiz puan")

    return Approval(score)
```

Erken dönüşler iç içe koşulları azaltır ve mutlu yolu görünür kılar. Ancak yalnızca metotları küçültmek yeterli değildir; yeni parçaların anlamlı sorumluluklara sahip olması gerekir.

## Küçük adımlar, büyük rahatlama

Refactoring sırasında her adımın küçük, test edilebilir ve geri alınabilir olması önemlidir. Önce test ekleyin, sonra bir sorumluluğu çıkarın, testleri çalıştırın ve değişikliği kaydedin. Kod incelemelerinde dosya uzunluğundan çok **değişme nedenlerini**, bağımlılık yönünü ve yan etkileri tartışın.

Amaç her sınıfı minik parçalara bölmek değil, değişikliklerin etkisini öngörülebilir hâle getirmektir. İyi mimari, geliştiricinin kahramanlık yapmasını gerektirmeyen mimaridir. Kod tabanında yalnızca bir kişinin bildiği gizli geçitler varsa orası bir saray değil, yazılımsal bir kaçış odasıdır.
