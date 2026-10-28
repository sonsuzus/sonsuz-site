---
layout: post
title: "Akıllı Ev Ağlarında Mahremiyet ve Veri Güvenliği: Eviniz Sizi Dinliyor mu?"
math: true
categories: 
  - Bilgi
tags: 
  - akıllı ev
  - siber güvenlik
  - mahremiyet
  - nesnelerin interneti
  - veri güvenliği
  - iot
toc: true
image: /img/akilli-ev-aglarinda-39.png
---

Akıllı hoparlörlerden güvenlik kameralarına, robot süpürgelerden internete bağlı ampullere kadar evlerimiz giderek daha fazla veri üretiyor. Bu cihazlar yaşamı kolaylaştırırken ses kayıtları, görüntüler, hareket bilgileri ve günlük alışkanlıklar gibi oldukça kişisel verileri de işliyor. Dolayısıyla ev ağındaki güvenlik açığı yalnızca internetin yavaşlaması değil, özel hayatın görünür hâle gelmesi anlamına gelebilir.


![akilli-ev-aglarinda-39](/img/akilli-ev-aglarinda-39.svg)

``

## Akıllı ev cihazları hangi verileri toplar?

Bir cihazın topladığı veri, sunduğu özellikle doğrudan ilişkilidir. Akıllı termostat sıcaklık tercihlerini öğrenirken robot süpürge evin haritasını çıkarabilir. Kapı sensörleri ise evde bulunulan saatlerin tahmin edilmesine yardımcı olabilir. Tek başına önemsiz görünen bu kayıtlar birleştirildiğinde ayrıntılı bir davranış profili ortaya çıkar.

| Cihaz | Toplanan veri | Olası risk |
|---|---|---|
| Akıllı kamera | Görüntü, ses, hareket | İzinsiz gözetleme |
| Akıllı hoparlör | Sesli komutlar, arama geçmişi | Konuşmaların ifşası |
| Robot süpürge | Oda haritası, çalışma saatleri | Ev düzeninin öğrenilmesi |
| Akıllı priz | Enerji kullanımı, zaman bilgisi | Günlük rutinin tahmini |
| Akıllı kilit | Giriş-çıkış kayıtları | Fiziksel güvenlik riski |

Mahremiyet riski basitçe şu modelle düşünülebilir:

$$R = P \times E \times V$$

Burada $P$ saldırının gerçekleşme olasılığını, $E$ açığa çıkacak verinin miktarını, $V$ ise verinin hassasiyetini temsil eder. Çok güçlü şifrelenen bir sistemde $P$ azalır; cihaz gereksiz veri toplamıyorsa $E$ küçülür. Sağlık veya kamera verileri söz konusu olduğunda ise $V$ doğal olarak yüksektir.

## Veriler nasıl kötüye kullanılabilir?

En yaygın tehlikelerden biri varsayılan parolaların değiştirilmemesidir. Saldırganlar internete açık cihazları tarayarak bilinen kullanıcı adı ve parola kombinasyonlarını deneyebilir. Güncellenmeyen yazılımlar, güvensiz bulut servisleri ve şifrelenmemiş bağlantılar da diğer giriş kapılarıdır.

Tehlike her zaman dışarıdan gelmez. Üretici firmalar kullanım verilerini reklam, analiz veya ürün geliştirme amacıyla üçüncü taraflarla paylaşabilir. Kullanıcı sözleşmesindeki belirsiz ifadeler, teknik olarak izin verilmiş fakat kullanıcı açısından beklenmeyen veri kullanımlarına yol açabilir.

## Temel koruma katmanları

Güvenli bir akıllı ev, tek bir sihirli ayar yerine katmanlı savunma yaklaşımıyla kurulur.

1. **Varsayılan parolaları değiştirin:** Her cihaz için uzun ve benzersiz parola kullanın.
2. **Çok faktörlü doğrulamayı açın:** Hesap parolası sızsa bile ikinci bir kontrol katmanı oluşturur.
3. **Cihazları ayrı ağa alın:** IoT cihazlarını bilgisayar ve telefonlardan ayıran misafir ağı veya VLAN kullanın.
4. **Güncellemeleri izleyin:** Otomatik güncellemeyi açın; desteği sona ermiş cihazları değiştirin.
5. **Gereksiz özellikleri kapatın:** Kullanılmayan mikrofonu, uzaktan erişimi ve konum takibini devre dışı bırakın.
6. **Gizlilik politikasını okuyun:** Verinin nerede saklandığını ve nasıl silinebildiğini kontrol edin.

| Zayıf yaklaşım | Daha güvenli yaklaşım |
|---|---|
| Tüm cihazları aynı Wi-Fi ağına bağlamak | IoT cihazlarını ayrı ağda tutmak |
| Aynı parolayı tekrar kullanmak | Parola yöneticisiyle benzersiz parola üretmek |
| Güncellemeleri ertelemek | Güvenlik yamalarını otomatik yüklemek |
| Sürekli bulut kaydı | Mümkünse yerel ve şifreli kayıt |

## Ağınızdaki cihazları kontrol edin

Teknik kullanıcılar, yönlendirici kayıtlarını incelemenin yanında yerel ağdaki aktif cihazları Python ile listeleyebilir. Aşağıdaki örnek, sistemdeki ARP tablosunu göstererek ağa yakın zamanda bağlanmış cihazların IP ve MAC adreslerini görmeye yardımcı olur:

```python
import subprocess

result = subprocess.run(
    ["arp", "-a"],
    capture_output=True,
    text=True,
    check=True
)

print("Ağda görülen cihazlar:")
print(result.stdout)
```

Bu kod bir güvenlik tarayıcısı değildir; yalnızca envanter çıkarmanın basit başlangıcıdır. Tanımadığınız bir cihaz görürseniz yönlendirici panelinden bağlantıyı engelleyebilir ve Wi-Fi parolanızı yenileyebilirsiniz.

Sonuç olarak akıllı ev güvenliği, cihaz satın alınırken başlamalıdır. Düzenli güncelleme sunan, açık gizlilik politikası bulunan ve yerel veri işleme seçenekleri sağlayan üreticiler tercih edilmelidir. Evinizi akıllandırırken temel ilke şu olmalı: Toplanmayan veri sızdırılamaz, erişilemeyen cihaz kolayca ele geçirilemez.
