---
layout: post
title: "İstemci-Sunucu Senkronizasyonu: Çevrimiçi Oyunlarda Hile Nasıl Yakalanır?"
math: true
categories: 
  - Bilgi
tags: 
  - oyun geliştirme
  - hile önleme
  - istemci sunucu
  - siber güvenlik
  - ağ programlama
  - senkronizasyon
toc: true
image: /img/istemci-sunucu-senkronizasyonu-41.png
---

Çevrimiçi bir oyunda ekranda gördüğümüz dünya, aslında istemci ile sunucunun sürekli uzlaşmaya çalıştığı sayısal bir simülasyondur. Gecikme, paket kaybı ve farklı donanımlar bu uzlaşmayı zorlaştırırken hile yapan oyuncular da istemciden gönderilen verileri değiştirerek avantaj kazanmaya çalışır. Etkili bir hile önleme sistemi bu nedenle yalnızca “hile programı bulmak” değil, oyuncunun davranışını matematiksel ve mantıksal olarak doğrulamak anlamına gelir.

![istemci-sunucu-senkronizasyonu-41](/img/istemci-sunucu-senkronizasyonu-41.svg)

``

## Temel güven modeli: İstemciye güvenme

En önemli prensip şudur: **İstemci niyet bildirir, sonucu sunucu hesaplar.** Oyuncunun bilgisayarı “Rakibe 100 hasar verdim” dememeli; yalnızca “Şu yönde ateş ettim” bilgisini göndermelidir. Mermi yolu, çarpışma ve hasar sunucuda doğrulanmalıdır.

| Yaklaşım | İstemcinin gönderdiği bilgi | Avantaj | Risk |
|---|---|---|---|
| İstemci otoriter | Konum, hasar ve sonuç | Düşük sunucu maliyeti | Hileye çok açık |
| Sunucu otoriter | Girdi ve eylem niyeti | Güçlü doğrulama | Daha fazla işlem yükü |
| Hibrit model | Tahmin edilen durum ve girdiler | Akıcı oynanış | Karmaşık senkronizasyon |

Oyuncunun azami hızı $v_{max}$, iki güncelleme arasındaki süre $\Delta t$ ise izin verilen yaklaşık hareket mesafesi şu şekilde hesaplanabilir:

$$d_{max} = v_{max} \times \Delta t + \epsilon$$

Buradaki $\epsilon$, ağ gecikmesi ve kayan nokta hataları için bırakılan toleranstır. Bildirilen mesafe sürekli olarak $d_{max}$ değerini aşıyorsa hız hilesi, ışınlanma veya bozuk senkronizasyon şüphesi oluşur.

## Tahmin, uzlaştırma ve gecikme telafisi

Her tuş vuruşunda sunucuyu beklemek oyunu hantallaştırır. Bu yüzden istemci, **client-side prediction** ile girdinin sonucunu anında gösterir. Sunucu daha sonra gerçek durumu yollar. İki durum farklıysa istemci, onaylanmamış girdileri yeniden uygulayarak **server reconciliation** gerçekleştirir.

Nişancı oyunlarında sunucu ayrıca geçmiş konumların kısa bir kaydını tutabilir. Ateş paketinin zamanı geldiğinde dünya, oyuncunun gecikmesine göre geçmişteki hâline döndürülür. Buna **lag compensation** denir. Ancak istemcinin bildirdiği zaman sınırsız kabul edilirse saldırganlar geçmişte avantajlı bir ana ateş etmiş gibi davranabilir. Bu nedenle zaman damgaları makul bir pencere içinde sınırlandırılmalıdır.

```python
MAX_SPEED = 7.0
TOLERANCE = 0.35


def validate_movement(old_pos, new_pos, delta_time):
    distance = new_pos.distance_to(old_pos)
    allowed = MAX_SPEED * delta_time + TOLERANCE

    if distance > allowed:
        return False, "olağandışı hareket"

    return True, "geçerli"
```

Bu örnek tek başına kusursuz değildir; zıplama, araçlar, geri tepme ve sunucu takılması gibi durumlar için bağlamsal kurallar gerekir. Yine de sunucu tarafındaki temel doğrulama katmanını gösterir.

## Hile tespit yöntemleri

Hile önleme genellikle birden fazla sinyali birleştirir:

- **Kural tabanlı doğrulama:** İmkânsız hız, atış sıklığı, cephane veya görüş açısı aranır.
- **İstatistiksel analiz:** İsabet oranı, hedef değiştirme süresi ve fare hareketleri oyuncu geçmişiyle karşılaştırılır.
- **Davranışsal modeller:** Aimbot benzeri araçların aşırı düzgün ya da anlık dönüşleri sınıflandırılır.
- **Bütünlük kontrolleri:** Oyun dosyaları ve kritik kod bölümleri imza veya özet değerleriyle denetlenir.
- **Tekrar incelemesi:** Şüpheli karşılaşmalar kaydedilerek otomatik ya da insan destekli değerlendirme yapılır.

| Sinyal | Normal açıklama | Hile ihtimali |
|---|---|---|
| Ani konum değişimi | Paket kaybı, yeniden bağlanma | Teleport hilesi |
| Çok yüksek isabet | Yetenekli oyuncu | Aimbot |
| Duvar arkasına takip | Ses veya takım bilgisi | Wallhack |
| Kusursuz atış aralığı | Düzenli giriş | Makro kullanımı |

## Yanlış pozitiflerden kaçınmak

Tek bir anormallik yüzünden oyuncuyu yasaklamak tehlikelidir. Bunun yerine her sinyale ağırlık verilip bir risk puanı üretilebilir:

$$R = w_1s_1 + w_2s_2 + \dots + w_ns_n$$

Düşük puan yalnızca kayda alınabilir, orta puan ek doğrulama başlatabilir, yüksek ve tekrarlanan puan ise inceleme kuyruğuna gönderilebilir. Böylece kötü bağlantıya sahip masum oyuncular cezalandırılmaz.

Sonuç olarak güçlü koruma; sunucu otoritesi, hareket ve eylem doğrulaması, davranış analizi, güvenli telemetri ve kontrollü yaptırımların birleşimidir. Amaç istemciyi bütünüyle kontrol etmek değil, istemciden gelen hiçbir kritik iddiayı doğrulamadan kabul etmemektir.
