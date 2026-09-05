---
layout: post
title: "Kod Akışını Korumak: IDE İçinde Pomodoro ve Odaklanma Psikolojisi"
math: true
categories: 
  - Bilgi
tags: 
  - pomodoro
  - üretkenlik
  - ıde
toc: true
---

Bir geliştirici için dikkat dağınıklığı yalnızca telefona bakmak değildir; açık sekmeler, derleme bildirimleri, Slack mesajları ve “şu fonksiyonu da düzelteyim” dürtüsü aynı zihinsel kaynakları tüketir. Pomodoro tekniğini doğrudan IDE içerisine taşımak, zamanı ölçmekten çok çalışma sınırlarını görünür hâle getirir. Böylece zamanlayıcı, kod yazarken sürekli pazarlık yaptığımız beynimize küçük ama etkili bir çalışma sözleşmesi sunar.
``

## Pomodoro neden işe yarar?

Klasik Pomodoro döngüsü, 25 dakikalık odaklanma ve 5 dakikalık mola bölümlerinden oluşur. Dört döngüden sonra daha uzun bir mola verilir. Ancak yöntemin asıl gücü, sihirli bir “25” sayısından değil, belirsiz işi sınırlı bir zaman kutusuna dönüştürmesinden gelir.

Bir görevin gözümüzdeki zihinsel maliyetini basitçe şöyle düşünebiliriz:

$$
Algılanan\ Yük = İşin\ Karmaşıklığı \times Belirsizlik
$$

“Kimlik doğrulama modülünü tamamla” büyük ve belirsizdir. “Önümüzdeki 25 dakikada başarısız giriş testlerini yaz” ise somuttur. Zaman kutulama, işin gerçek karmaşıklığını azaltmasa da belirsizlik bileşenini küçültür.

Pomodoro ayrıca **Zeigarnik etkisinden** yararlanır: Beyin, yarım kalan görevleri hatırlama eğilimindedir. Mola verdiğinizde çözüm tamamen kaybolmaz; zihniniz arka planda bağlantılar kurmayı sürdürebilir. Buna karşılık sürekli bildirim almak, her geçişte “dikkat kalıntısı” oluşturur. Önceki işin bir bölümü zihinde kaldığı için yeni göreve tam kapasiteyle geçilemez.

## IDE zamanlayıcısı neden ayrı bir uygulamadan iyidir?

Zamanlayıcının IDE içinde bulunması, çalışma bağlamını terk etme ihtiyacını azaltır. Telefon uygulamasını kontrol etmek masum görünür; fakat birkaç saniye içinde mesajlara veya sosyal medyaya geçmek şaşırtıcı derecede kolaydır.

| Yaklaşım | Avantaj | Risk |
|---|---|---|
| Telefon zamanlayıcısı | Kurulumu kolaydır | Telefon yeni dikkat dağıtıcılar açar |
| Masaüstü uygulaması | Ayrıntılı rapor sunar | Pencere geçişi gerektirir |
| IDE eklentisi | Kod bağlamını korur | Çok fazla bildirim üretebilir |
| Manuel saat takibi | Tamamen özelleştirilebilir | Disiplin ve hatırlama gerektirir |

İyi bir IDE entegrasyonu yalnızca geri sayım göstermelidir. Her saniye yanıp sönen sayaç, odak aracı olmaktan çıkıp kaygı aracına dönüşebilir. Durum çubuğunda sakin bir gösterge, döngü sonunda tek bildirim ve isteğe bağlı ses çoğu geliştirici için yeterlidir.

## Basit bir zamanlayıcının mantığı

Aşağıdaki JavaScript örneği, bir IDE eklentisinin temel çalışma döngüsünü temsil eder. Gerçek bir eklentide bildirim API’si ve durum çubuğu bileşeni kullanılabilir:

```javascript
const focusMinutes = 25;
let remaining = focusMinutes * 60;

const timer = setInterval(() => {
  remaining--;

  const minutes = Math.floor(remaining / 60);
  const seconds = remaining % 60;
  updateStatusBar(`Odak: ${minutes}:${String(seconds).padStart(2, "0")}`);

  if (remaining <= 0) {
    clearInterval(timer);
    showNotification("Odak döngüsü tamamlandı. Beş dakika mola!");
  }
}, 1000);
```

Burada `remaining`, toplam süreyi saniye cinsinden tutar. `setInterval` her saniye değeri azaltır; `updateStatusBar` IDE içinde kalan süreyi gösterir. Süre bittiğinde sayaç durdurulur ve mola bildirimi gönderilir. Üretim ortamında IDE kapanması, zamanlayıcının duraklatılması ve sistem uykusu gibi durumlar için başlangıç zamanını kaydetmek daha güvenilirdir.

## Döngüyü geliştiriciye uyarlamak

Her görev 25 dakikaya uygun değildir. Hata ayıklama sırasında bağlamı kurmak uzun sürüyorsa $50+10$ döngüsü daha verimli olabilir. Küçük bakım görevlerinde ise $15+3$ yaklaşımı başlangıç direncini azaltabilir.

Önemli olan molayı yeni bir ekran etkinliğiyle doldurmamaktır. Ayağa kalkmak, uzağa bakmak ve su içmek bilişsel yenilenmeyi destekler. Döngü sonunda kısa bir not bırakmak da dönüş maliyetini azaltır: “Test başarısız; sıradaki adım token süresini kontrol etmek.” Böylece mola sonrasında beyniniz yeniden dedektiflik yapmak zorunda kalmaz.

Pomodoro bir performans yarışması değil, dikkati koruyan bir ritimdir. IDE içindeki sade bir zamanlayıcı; başlama direncini düşürür, bağlam geçişlerini sınırlar ve çalışma ile dinlenme arasındaki çizgiyi belirginleştirir. En iyi ayar ise en fazla döngüyü tamamladığınız değil, gün sonunda hâlâ berrak düşünebildiğiniz ayardır.
