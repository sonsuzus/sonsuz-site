---
layout: post
title: "Satranç Turnuva Sistemleri: Swiss-Manager, Tornelo ve Lichess Nasıl Çalışır?"
math: true
categories: 
  - Bilgi
tags: 
  - satranç
  - turnuva
  - swiss-manager
  - tornelo
  - lichess
  - eşlendirme
  - yazılım
toc: true
image: /img/satranc-turnuva-sistemleri-88.png
---

Bir satranç turnuvasında taşları oyuncular hareket ettirir; fakat arka planda skorları hesaplayan, rakipleri eşlendiren ve sonuçları yayımlayan görünmez bir hakem daha vardır: turnuva yazılımı. Swiss-Manager, Tornelo ve Lichess bu işi farklı yaklaşımlarla çözer. Biri geleneksel turnuva yönetiminde uzmanlaşırken, diğeri bulut tabanlı organizasyon sunar; Lichess ise oyun platformuyla turnuva motorunu aynı çatı altında birleştirir.


![satranc-turnuva-sistemleri-88](/img/satranc-turnuva-sistemleri-88.svg)

``

## Turnuva motorunun temel görevi

Bir turnuva sistemi yalnızca kimin kazandığını kaydetmez. Oyuncu kayıtlarını yönetir, turları oluşturur, renk dağılımını dengeler, hükmen sonuçları işler ve eşit puanlı oyuncuları sıralar.

Standart puanlama sisteminde oyuncunun toplam skoru şöyle ifade edilebilir:

$$S = 1 \times G + 0.5 \times B + 0 \times M$$

Burada $G$ galibiyet, $B$ beraberlik ve $M$ mağlubiyet sayısıdır. Ancak iki oyuncu aynı puana ulaştığında ek ölçütler gerekir. Örneğin Buchholz puanı, karşılaşılan rakiplerin skorlarının toplamıdır:

$$B_i = \sum_{j \in R_i} S_j$$

Yani güçlü rakiplerle oynayan oyuncu, eşitlik bozma sırasında avantaj kazanabilir. Sonneborn-Berger, kümülatif skor ve doğrudan karşılaşma da kullanılabilen diğer ölçütlerdir.

## Swiss sistemi neden popüler?

İsviçre sistemi, herkesin herkesle oynamasını gerektirmeden çok sayıda oyuncuyu sıralayabilir. Her turda benzer puana sahip oyuncular karşılaştırılır. Bununla birlikte aynı iki oyuncunun tekrar eşleşmemesi, renklerin mümkün olduğunca dengeli dağıtılması ve takım ya da kulüp kısıtlarının gözetilmesi gerekir.

Yaklaşık olarak $N$ oyuncudan tek bir lider çıkarmak için gereken tur sayısı $\lceil \log_2 N \rceil$ civarında düşünülebilir. Ancak güvenilir bir sıralama için organizatörler genellikle daha fazla tur planlar. Örneğin 128 oyunculu bir etkinlikte 7 tur teorik bir başlangıç noktasıdır; 9 tur daha ayırt edici sonuçlar üretir.

## Üç sistemin karşılaştırması

| Özellik | Swiss-Manager | Tornelo | Lichess |
|---|---|---|---|
| Çalışma biçimi | Masaüstü ağırlıklı | Bulut tabanlı | Tamamen çevrim içi |
| Ana kullanım | Resmî yüz yüze turnuvalar | Hibrit ve çevrim içi etkinlikler | Hızlı çevrim içi organizasyonlar |
| Eşlendirme | Gelişmiş Swiss seçenekleri | Otomatik ve web tabanlı | Swiss ve Arena |
| Sonuç girişi | Hakem veya operatör | Hakem ve oyuncu iş akışları | Oyun bitince otomatik |
| Öğrenme eğrisi | Daha yüksek | Orta | Düşük |
| Yayınlama | Haricî sayfalarla güçlü | Dahili canlı sayfalar | Anında platform üzerinde |

**Swiss-Manager**, FIDE turnuvalarında sık kullanılan güçlü bir masaüstü aracıdır. Çok sayıda eşitlik bozma seçeneği, rating raporları ve resmî çıktı üretimi sunar. Buna karşılık arayüzü yeni başlayanlara biraz “hakem kokpiti” gibi gelebilir.

**Tornelo**, tarayıcı üzerinden kayıt, eşlendirme, sonuç ve yayın yönetimini bir araya getirir. Kurulum gerektirmemesi özellikle farklı şehirlerden çalışan ekipler için avantajdır. Hibrit etkinliklerde fiziksel masalar ile çevrim içi süreçler arasında köprü kurabilir.

**Lichess** iki önemli model sunar. Swiss turnuvalarında oyuncular tur usulü eşleşir ve turun bitmesini bekler. Arena modelinde ise oyuncular süre boyunca mümkün olduğunca çok oyun oynar; hızlı galibiyet serileri ve “Berserk” gibi özellikler puanlamayı daha eğlenceli hâle getirir.

## Basitleştirilmiş eşlendirme mantığı

Aşağıdaki Python örneği oyuncuları puana göre sıralayıp komşu oyuncuları eşleştirir:

```python
def eslendir(oyuncular):
    sirali = sorted(
        oyuncular,
        key=lambda oyuncu: (-oyuncu["puan"], -oyuncu["rating"])
    )

    eslesmeler = []
    for i in range(0, len(sirali) - 1, 2):
        eslesmeler.append((sirali[i], sirali[i + 1]))

    bye = sirali[-1] if len(sirali) % 2 else None
    return eslesmeler, bye
```

Kod önce puanı, ardından ratingi yüksek oyuncuları öne alır ve ikili gruplar oluşturur. Tek sayıda katılımcı varsa son oyuncuya “bye” verir. Gerçek sistemler ise geçmiş rakipleri, renk geçmişini, puan grubu geçişlerini ve yasak eşleşmeleri de denetler; dolayısıyla üretim düzeyindeki algoritmalar çok daha karmaşıktır.

Sonuç olarak resmî ve ayrıntılı raporlama için Swiss-Manager, kolay paylaşılabilir bulut yönetimi için Tornelo, hızlı çevrim içi etkinlikler için Lichess öne çıkar. En iyi araç, turnuvanın çevrim içi mi yüz yüze mi olduğuna, hakem gereksinimlerine ve katılımcı sayısına göre seçilmelidir.
