---
layout: post
title: "Birim, Entegrasyon ve Uçtan Uca Testler: Güvenilir Yazılımın Test Piramidi"
math: true
categories: 
  - Bilgi
tags: 
  - yazılım testi
  - test piramidi
  - birim testi
  - entegrasyon testi
  - uçtan uca test
---

Yazılım güvenilirliği, yalnızca uygulamanın bir kez çalışmasıyla ölçülmez; değişikliklerden sonra da doğru davranmasını sürdürebilmesiyle ölçülür. İşte test piramidi, ekiplerin sınırlı zaman ve kaynakla hangi testlere ne kadar yatırım yapması gerektiğini anlatan pratik bir modeldir. Piramidin tabanında hızlı ve bol miktarda birim testi, ortasında bileşenlerin birlikte çalışmasını doğrulayan entegrasyon testleri, tepesinde ise gerçek kullanıcı yolculuklarını sınayan az sayıda uçtan uca test bulunur.

``

Test piramidinin temel fikri, testlerin maliyet ve geri bildirim hızlarının eşit olmamasıdır. Bir fonksiyonun sonucunu kontrol etmek saniyeler sürerken, tarayıcı açıp veritabanı ve dış servislerle tam bir senaryo koşturmak dakikalar alabilir. Basitçe toplam geri bildirim süresini şöyle düşünebiliriz:

$$T_{toplam}=n_bT_b+n_eT_e+n_{u2u}T_{u2u}$$

Burada $n$ test sayısını, $T$ ise tek testin ortalama çalışma süresini temsil eder. Genellikle $T_b \ll T_e \ll T_{u2u}$ olduğundan, hızlı testlerin sayıca fazla olması hem ekonomik hem de sürdürülebilir bir tercihtir.

## Piramidin tabanı: Birim testleri

Birim testleri; fonksiyon, sınıf veya küçük bir iş kuralı gibi en küçük anlamlı parçayı dış bağımlılıklarından izole ederek test eder. Örneğin indirim hesaplama mantığı, veritabanına bağlanmadan doğrulanabilir. Hata bulunduğunda sebebi de çoğunlukla nettir: sorun test edilen birimdedir.

```javascript
function indirimliFiyat(fiyat, oran) {
  if (oran < 0 || oran > 100) throw new Error("Geçersiz oran");
  return fiyat * (1 - oran / 100);
}

test("%20 indirim doğru hesaplanır", () => {
  expect(indirimliFiyat(250, 20)).toBe(200);
});
```

Bu örnek, iş kuralının hem normal durumunu hem de ayrıca sınır durumlarını test etmeye uygundur. Mock ve stub araçları burada yararlıdır; ancak aşırı mock kullanımı, gerçekte birlikte çalışmayan parçaların testte başarılı görünmesine yol açabilir.

## Orta katman: Entegrasyon testleri

Entegrasyon testleri, ayrı ayrı doğru çalışan modüllerin birbirleriyle doğru konuşup konuşmadığını denetler. API'nin veritabanına kayıt atması, mesaj kuyruğuna olay göndermesi veya kimlik doğrulama servisinden gelen yanıtı işlemesi bu katmanın tipik konularıdır. Birim testinin kaçırabileceği veri biçimi, SQL sorgusu, seri hale getirme ve yapılandırma hataları burada görünür.

| Özellik | Birim testi | Entegrasyon testi | Uçtan uca test |
|---|---|---|---|
| Kapsam | Tek birim | Birden çok bileşen | Tüm kullanıcı akışı |
| Çalışma hızı | Çok hızlı | Orta | Yavaş |
| Hata teşhisi | Kolay | Orta | Daha zor |
| Dış bağımlılık | Genellikle taklit edilir | Sıklıkla gerçek/test ortamı | Gerçeğe çok yakın |

Örneğin bir sipariş API'si için entegrasyon testi, HTTP isteğini gönderip test veritabanındaki sipariş kaydını kontrol edebilir. Bu yaklaşım, yalnızca denetleyiciyi değil yönlendirme, doğrulama, ORM ve şema uyumunu da kapsar.

## Piramidin tepesi: Uçtan uca testler

Uçtan uca (E2E) testler, kullanıcının gördüğü dünyayı taklit eder: giriş yapma, ürün arama, sepete ekleme ve ödeme adımına ilerleme gibi senaryoları tarayıcı üzerinden çalıştırır. Playwright veya Cypress gibi araçlar bu iş için yaygındır. Bu testler yüksek güven sağlar; fakat kırılgan olabilir. Yavaş ağ, zamanlama sorunları veya değişen arayüz seçicileri test başarısızlığına neden olabilir.

Bu nedenle E2E testlerini her küçük ayrıntıya değil, iş açısından kritik akışlara ayırmak gerekir. Örneğin her buton rengini E2E ile denetlemek yerine, “kullanıcı ödeme sonrası sipariş onayı alır” davranışını test etmek daha değerlidir.

## Dengeli bir strateji kurmak

İdeal oran projeye göre değişse de mantık sabittir: çok sayıda hızlı birim testi, yeterli entegrasyon testi ve seçilmiş E2E senaryoları. Test başarısızlık oranı da kalite sinyali olarak izlenebilir:

$$Başarı\ Oranı=\frac{Başarılı\ Testler}{Toplam\ Testler}\times100$$

Ancak yüzde 100 başarı tek başına kalite garantisi değildir; yanlış şeyi test eden yüz test de yanıltıcıdır. Anlamlı iş kurallarına, gerçek entegrasyon risklerine ve kullanıcı için kritik yolculuklara odaklanan piramit, regresyonları erken yakalar. Sonuçta amaç test sayısını şişirmek değil, değişiklik yapma cesaretini artırmaktır.
