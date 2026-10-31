---
layout: post
title: "Oyun İçi Ekonomiler: Altın Yağmuru Neden Enflasyona Dönüşür?"
math: true
categories: 
  - Bilgi
tags: 
  - oyun tasarımı
  - sanal ekonomi
  - enflasyon
  - ekonomi dengesi
  - python
  - oyun geliştirme
toc: true
image: /img/oyun-ici-ekonomiler-38.png
---

Bir ejderhayı kestiniz, sandıktan bin altın çıktı ve kendinizi zengin hissettiniz. Fakat pazardaki sıradan kılıç geçen hafta beş yüz altınken bugün iki bin altın! Tebrikler: Ejderhadan kurtuldunuz, enflasyona yakalandınız. Oyun içi ekonomiler, gerçek ekonominin bazı mekanizmalarını şaşırtıcı biçimde tekrarlar; üstelik merkez bankasının yerinde çoğunlukla birkaç geliştirici oturur.

``

## Altın çoğalınca neden herkes zenginleşmez?

Paranın değeri, yalnızca sahip olduğunuz miktardan değil, onunla satın alabildiğiniz şeylerden gelir. Oyuncuların cüzdanları büyürken ticarete konu olan ürünlerin miktarı aynı hızda artmıyorsa fiyatlar üzerinde yükseliş baskısı oluşabilir.

Bu ilişkiyi düşünmek için klasik miktar denklemi yararlıdır:

$$MV = PY$$

Burada $M$ para miktarı, $V$ paranın dolaşım hızı, $P$ fiyat düzeyi ve $Y$ işlem gören reel mal ve hizmet hacmidir. Denklem tek başına bir tahmin makinesi değildir. Oyuncular altını biriktirirse dolaşım yavaşlayabilir; üretim artarsa fiyat baskısı hafifleyebilir. Ayrıca yalnızca nadir bir kılıcın pahalanması, genel enflasyon anlamına gelmez.

## Gerçek ekonomiyle akrabalık ilişkisi

| Mekanizma | Gerçek ekonomi | Oyun ekonomisi |
|---|---|---|
| Para yaratımı | Bankacılık ve para politikası | Görev ödülleri, yaratık ganimetleri |
| Üretim | İş gücü ve üretim kapasitesi | Toplama, üretim tarifleri, düşme oranları |
| Para çıkışı | Vergiler ve diğer mekanizmalar | Sistemden silinen ücretler |
| Beklentiler | Gelecekteki fiyat beklentileri | Güncelleme öncesi eşya stoklama |
| Dış şoklar | Tedarik kesintileri | Açıklar, botlar, içerik güncellemeleri |

![oyun-ici-ekonomiler-38](/img/oyun-ici-ekonomiler-38.svg)


Benzetmenin sınırı önemlidir: Gerçek hayatta vergilendirilen para yeniden harcanabilir. Oyunda ise bir onarım ücreti gerçekten siliniyorsa para arzını azaltır. Geliştirici ayrıca bir eşyanın bulunma ihtimalini tek satırla değiştirebilir; gerçek ekonomide bakır madenine böyle bir yama gönderemezsiniz.

## Kaynaklar ve giderler: Musluk ile lavabo

Ekonomi tasarımında para yaratan mekanizmalara **kaynak**, parayı dolaşımdan kaldıran mekanizmalara **gider** denir. Basit bilanço şöyledir:

$$M_{t+1} = M_t + F_t - S_t$$

$F_t$ dönemde yaratılan, $S_t$ ise silinen paradır. Oyuncular arasındaki normal alışveriş parayı yok etmez; yalnızca sahibini değiştirir. Pazar komisyonu ancak sistem tarafından siliniyorsa gider sayılır.

Denge, her gün kaynaklarla giderleri eşitlemek değildir. Oyuncu sayısı ve üretim büyürken daha fazla para gerekebilir. Buna karşılık sınırsız tekrarlanabilen görevler, botlarla birleşince ekonomiye yangın hortumuyla altın püskürtebilir.

İyi giderler oyuncuya değer sunar: kozmetik seçenekler, isteğe bağlı hizmetler veya anlamlı üretim maliyetleri. Sürekli yükselen zorunlu onarım ücretleri ise ekonomiyi düzeltirken eğlenceyi bozabilir. Lavaboyu açmak için oyuncunun evini su altında bırakmayın.

## Python ile küçük bir erken uyarı sistemi

Aşağıdaki örnek, sabit bir referans sepetindeki piyasa fiyatlarını karşılaştırır. Ağırlıklar başlangıç dönemindeki harcama paylarını temsil eder. Fiyat artışı ve pozitif net para üretimi birlikte görülürse inceleme için küçük bir ödül ayarlaması önerilir.

```python
BASE = {
    "iksir": (10, 0.40),
    "demir": (20, 0.35),
    "ekmek": (5, 0.25),
}


def economic_signal(prices, net_flow):
    if any(prices[item] <= 0 for item in BASE):
        raise ValueError("Fiyatlar pozitif olmalı")

    index = sum(
        weight * prices[item] / baseline
        for item, (baseline, weight) in BASE.items()
    )
    multiplier = 0.97 if index > 1.08 and net_flow > 0 else 1.0
    return {"index": round(index, 3), "reward_multiplier": multiplier}


prices = {"iksir": 12, "demir": 22, "ekmek": 5}
print(economic_signal(prices, net_flow=5000))
```

Sonuçtaki `1.115`, referans sepete göre yüzde 11,5 fiyat artışıdır. Önerilen `0.97`, ödüllerde yüzde üç azaltma anlamına gelir. Ancak yüzde sekizlik eşik örnektir; bu kod otomatik merkez bankası değil, gösterge panelinin başlangıcıdır. Gerçek uygulamada eksik veri kontrolü ve yeterli işlem hacmi de gerekir.

## Dengeyi ölç, oyuncuyu unutma

Tek günlük fiyatlara tepki vermek yerine haftalık eğilimleri, işlem hacmini ve manipülasyona dayanıklı fiyat istatistiklerini izleyin. Yeni başlayanlarla deneyimli oyuncuları ayrı değerlendirin: Ortalama servet artarken yeni oyuncunun ilk ekipmanına ulaşma süresi uzayabilir.

Birden fazla para birimi varsa her birinin kaynaklarını, giderlerini ve dönüşüm yollarını takip edin. Açıkları kapatmak çoğu zaman herkesten daha fazla ücret almaktan daha etkilidir. Değişiklikleri küçük uygulayın, sonuçlarını karşılaştırın ve gerekçelerini açıklayın.

Başarılı oyun ekonomisi, fiyatların sonsuza kadar sabit kaldığı ekonomi değildir. Oyuncunun emeğinin anlamlı kaldığı, ticaretin canlı olduğu ve yeni gelenlerin yarışa katılabildiği ekonomidir. Sonuçta amaç kusursuz bir hesap tablosu değil, yarın da giriş yapmak isteyeceğiniz bir dünyadır.
