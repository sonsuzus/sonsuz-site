---
layout: post
title: "Cyclomatic Complexity: Kodunuzun Bakım Haritasını Çıkarın"
math: true
categories: 
  - Bilgi
tags: 
  - Cyclomatic Complexity
  - Kod Kalitesi
  - Yazılım Metrikleri
---

Bir fonksiyonun uzun olması her zaman karmaşık olduğu anlamına gelmez; asıl yorucu olan, kodun içinde kaç farklı karar yolunun saklandığıdır. Cyclomatic Complexity (döngüsel karmaşıklık), Thomas McCabe tarafından geliştirilen ve bir program parçasındaki bağımsız yürütme yollarını sayısallaştıran metriktir. Bu sayı yükseldikçe test senaryosu üretmek, davranışı anlamak ve güvenle değişiklik yapmak zorlaşır.
``

Metrik, kodu bir **kontrol akış grafiği** olarak düşünür. Bu grafikte ifadeler düğüm, akış geçişleri ise kenardır. Temel formül şöyledir:

$$M = E - N + 2P$$

Burada $E$ kenar sayısını, $N$ düğüm sayısını, $P$ ise bağlantısız bileşen sayısını gösterir. Tek bir fonksiyon için genellikle $P=1$ kabul edilir. Pratikte daha kolay bir kural kullanılır: Başlangıç karmaşıklığı 1'dir; her `if`, `else if`, `for`, `while`, `case`, `catch` ve koşullu işlem (`&&`, `||`, `?:`) alternatif yol ekleyebilir. Araçların ayrıntılı sayım kuralları farklılık gösterebilir; ekip içinde seçilen aracın kuralına sadık kalmak önemlidir.

Örneğin aşağıdaki JavaScript fonksiyonunda başlangıç değeri 1'dir. `if`, `else if` ve `for` üç karar noktası oluşturur; dolayısıyla yaklaşık karmaşıklık $M=4$ olur.

```javascript
function indirimOrani(musteri, sepetTutari) {
  let oran = 0;

  if (musteri.premium) {
    oran = 0.20;
  } else if (sepetTutari > 1000) {
    oran = 0.10;
  }

  for (const kupon of musteri.kuponlar) {
    if (kupon.aktif) return oran + 0.05;
  }

  return oran;
}
```

Kodun görevi basittir: müşteri türü, sepet tutarı ve aktif kupona göre indirim üretir. Ancak her yeni koşul, sadece okunacak satır değil, test edilecek yeni bir yol anlamına gelir. $M=4$ olan bir fonksiyonun tüm bağımsız yollarını kapsamak için en az dört anlamlı test fikrine ihtiyaç duyulur. Bu, metrik ile test tasarımı arasındaki doğrudan bağlantıdır.

| Karmaşıklık | Genel yorum | Önerilen yaklaşım |
|---:|---|---|
| 1-5 | Düşük, genellikle kolay anlaşılır | Normal birim testleri yeterlidir |
| 6-10 | Yönetilebilir ama dikkat gerektirir | Sınır durumları ve dallar test edilmeli |
| 11-20 | Bakım riski belirgin | Parçalama ve sadeleştirme planlanmalı |
| 21+ | Yüksek hata ve değişiklik maliyeti | Acil refactor veya tasarım değişikliği düşünülmeli |

Yine de bu tablo bir mahkeme kararı değildir. Bir parser, karar motoru veya doğrulama kuralı doğal olarak çok sayıda dala sahip olabilir. Buradaki amaç “karmaşıklığı sıfırlamak” değil, karmaşıklığı görünür ve yönetilebilir hale getirmektir. Özellikle iç içe koşullar, aynı anda hem cognitive complexity'yi hem de hata olasılığını yükseltir.

Yüksek değeri düşürmenin en etkili yolu, koşulları küçük ve anlamlı fonksiyonlara ayırmaktır. Erken dönüşler (`guard clause`) gereksiz `else` bloklarını azaltır. Polimorfizm veya strateji deseni, müşteri türüne göre büyüyen `switch` yapılarını nesnelere taşıyabilir. Veri tabanlı kurallar ise uzun koşul zincirlerini bir eşleme tablosuna dönüştürebilir.

| Yaklaşım | Avantaj | Dikkat edilmesi gereken |
|---|---|---|
| Guard clause | İç içeliği azaltır | Çok fazla dönüş noktası izlemeyi zorlaştırabilir |
| Fonksiyona ayırma | Test edilebilirliği artırır | Anlamsız mikro fonksiyonlar üretmeyin |
| Strategy pattern | Değişen kuralları izole eder | Basit problemde gereksiz soyutlama olabilir |
| Kural tablosu | Koşulları veriye dönüştürür | Kural doğrulaması ayrıca tasarlanmalıdır |

Sonuç olarak Cyclomatic Complexity, kodun “kötü” olduğunu tek başına söylemez; nerede dikkat, test ve tasarım emeği gerektiğini işaret eder. CI sürecinde fonksiyon başına eşik koymak, yeni karmaşıklık artışlarını kod incelemesinde tartışmak ve metrik trendini izlemek, bakım maliyetini sürpriz olmaktan çıkarır. Kodunuzun kaç yolu olduğunu bilirseniz, hangi yolun sizi yorduğunu da daha erken görürsünüz.
