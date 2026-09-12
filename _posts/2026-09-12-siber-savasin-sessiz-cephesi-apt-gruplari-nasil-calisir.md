---
layout: post
title: "Siber Savaşın Sessiz Cephesi: APT Grupları Nasıl Çalışır?"
math: true
categories: 
  - Bilgi
tags: 
  - siber güvenlik
  - apt
  - tehdit istihbaratı
toc: true
---

Bir siber saldırının mutlaka ekranda beliren kırmızı uyarılarla veya aniden duran sunucularla başlaması gerekmez. Gelişmiş Sürekli Tehditler, yani APT’ler, dijital dünyanın sabırlı casuslarıdır. Ulus devletlerle ilişkilendirilebilen bu aktörler; stratejik bilgi toplamak, kritik altyapılara erişmek veya gelecekte kullanılabilecek kalıcı bir pozisyon elde etmek için hedef ağlarda aylarca, hatta yıllarca saklanabilir.

``

## APT kavramının üç temel bileşeni

APT, İngilizce *Advanced Persistent Threat* ifadesinin kısaltmasıdır. İsim, çalışma modelini oldukça iyi özetler:

- **Advanced:** Özel araçlar, çok aşamalı operasyonlar ve güçlü teknik uzmanlık kullanılır.
- **Persistent:** Aktör, tek seferlik kazanç yerine uzun vadeli erişim peşindedir.
- **Threat:** Operasyonun arkasında belirli hedefleri, kaynakları ve koordinasyonu olan bir ekip bulunur.

Sıradan saldırgan çoğu zaman kolay hedef ararken APT aktörü belirli bir kurumu seçer. Savunma sistemlerini inceler, başarısız olduğunda yöntem değiştirir ve mümkün olduğunca az iz bırakmaya çalışır.

| Özellik | Fırsatçı saldırı | APT operasyonu |
|---|---|---|
| Hedef seçimi | Geniş ve rastgele | Stratejik ve önceden belirlenmiş |
| Süre | Saatler veya günler | Aylar veya yıllar |
| Temel amaç | Hızlı kazanç | Casusluk, etki veya hazırlık |
| Altyapı | Hazır araçlar | Katmanlı ve özelleştirilmiş sistemler |
| Gizlilik | İkincil önemde | Operasyonun merkezinde |

## Teknik çalışma modeli

APT operasyonları doğrusal bir senaryodan çok döngüsel bir kampanyaya benzer. İlk aşamada hedef kurumun çalışanları, tedarikçileri ve internete açık sistemleri araştırılır. Ardından kimlik bilgileri, güven ilişkileri veya teknik zafiyetler üzerinden ilk erişim denenir.

Erişim sağlandıktan sonra aktör, ele geçirilen sistemi hemen gürültülü biçimde kullanmak yerine ortamı tanımaya çalışır. Yetki yapısı, ağ bölümleri, güvenlik araçları ve değerli veri konumları haritalandırılır. Sonraki aşamalarda kalıcılık, yanal hareket ve komuta-kontrol iletişimi görülebilir. Kritik nokta şudur: Her şüpheli işlem zararlı değildir; anlamlı olan, olayların birlikte oluşturduğu davranış zinciridir.

Bir gözlemin risk puanı basitçe şöyle modellenebilir:

$$R = w_aA + w_iI + w_cC + w_tT$$

Burada $A$ davranış anormalliğini, $I$ kimlik riskini, $C$ iletişim şüphesini ve $T$ tehdit istihbaratı eşleşmesini temsil eder. $w$ katsayıları ise kurumun önceliklerine göre belirlenen ağırlıklardır. Tek bir yüksek değer alarm üretmeyebilir; birleşik skor savunma ekibine bağlam sağlar.

## Gizlilik neden bu kadar etkilidir?

APT aktörleri genellikle normal yönetim faaliyetlerine benzeyen hareketleri tercih eder. Geçerli hesapların kullanılması, işlemlerin mesai saatlerine dağıtılması ve iletişimin seyrek tutulması klasik imza tabanlı ürünleri zorlayabilir. Örneğin düzenli aralıklarla dış bağlantı kuran bir cihaz, otomatik komuta-kontrol davranışı gösteriyor olabilir.

Aşağıdaki savunma odaklı Python örneği, bağlantı zamanları arasındaki aralıkların ne kadar düzenli olduğunu ölçer:

```python
from statistics import mean, pstdev

def beacon_score(timestamps):
    """Düzenli bağlantı aralıkları için 0-1 arasında puan üretir."""
    intervals = [b - a for a, b in zip(timestamps, timestamps[1:])]
    if len(intervals) < 3 or mean(intervals) == 0:
        return 0.0

    variation = pstdev(intervals) / mean(intervals)
    return max(0.0, min(1.0, 1 - variation))

print(beacon_score([0, 60, 121, 180, 240]))
```

Yüksek puan tek başına ihlal kanıtı değildir; güncelleme servisleri de düzenli bağlantılar kurabilir. Sonuç, hedef alan adı, süreç bilgisi ve cihaz rolüyle birlikte değerlendirilmelidir.

## Savunmanın anahtarı: Katmanlar ve görünürlük

APT savunması yalnızca daha fazla güvenlik ürünü satın almak değildir. Güçlü kimlik doğrulama, en az ayrıcalık ilkesi, ağ segmentasyonu, merkezi günlük toplama ve düzenli tehdit avcılığı birlikte uygulanmalıdır. Ayrıca tedarik zinciri erişimleri de kurum içi hesaplar kadar dikkatle izlenmelidir.

| Savunma katmanı | Sağladığı değer |
|---|---|
| MFA ve koşullu erişim | Çalınan parolanın etkisini azaltır |
| EDR ve günlük korelasyonu | Davranış zincirlerini görünür kılar |
| Ağ segmentasyonu | Yanal hareketi sınırlar |
| Olay müdahale planı | Kriz anındaki belirsizliği azaltır |

Sonuç olarak APT’lerle mücadele, “kötü dosyayı bul ve sil” yaklaşımından daha kapsamlıdır. Asıl hedef; saldırganın kimlik, cihaz ve ağ üzerindeki davranışlarını ilişkilendirmek, kalma süresini azaltmak ve kritik sistemlere ulaşmadan operasyon zincirini kırmaktır. Siber savaşın sessiz cephesinde en güçlü silah, sürekli ve bağlamlı görünürlüktür.
