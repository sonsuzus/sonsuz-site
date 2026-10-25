---
layout: post
title: "Ağ Teorisiyle Şehrin Röntgenini Çekmek: Yol Ağlarında Zayıf Nokta Analizi"
math: true
categories: 
  - Bilgi
tags: 
  - graf teorisi
  - ağ analizi
  - python
  - şehir planlama
  - networkx
  - veri bilimi
toc: true
image: /img/ag-teorisiyle-sehrin-49.png
---

Bir şehir haritasına baktığınızda yalnızca yollar, kavşaklar ve döner kavşakta çıkışı kaçıran sürücüler görmeyin. Aynı harita, matematiksel olarak incelenebilen dev bir ağdır. Graf teorisi sayesinde hangi kavşağın kritik olduğunu, bir köprü kapandığında ulaşımın ne kadar etkileneceğini ve alternatif güzergâhların gerçekten işe yarayıp yaramadığını ölçebiliriz.
``
## Şehri bir grafa dönüştürmek

Graf, düğümlerden ve bu düğümleri bağlayan kenarlardan oluşur. Yol ağı modelinde kavşaklar veya yol başlangıçları **düğüm**, yollar ise **kenar** olarak temsil edilir. Matematiksel gösterimle bir graf:

$$G = (V, E)$$

şeklinde tanımlanır. Burada $V$ düğüm kümesini, $E$ ise yol bağlantılarını ifade eder. Tek yönlü yolların bulunduğu şehirlerde yönlü graf; bütün yolların iki yönde kullanılabildiği basitleştirilmiş modellerde yönsüz graf tercih edilir.

Kenarlar yalnızca bağlantı anlamına gelmek zorunda değildir. Her yola uzunluk, seyahat süresi veya kapasite gibi bir ağırlık atanabilir:

$$w(u,v) = \text{seyahat süresi}$$

| Model öğesi | Şehirdeki karşılığı | Örnek özellik |
|---|---|---|
| Düğüm | Kavşak, durak, yol sonu | Konum, trafik yoğunluğu |
| Kenar | Yol veya köprü | Uzunluk, hız, kapasite |
| Ağırlık | Geçiş maliyeti | Süre, mesafe, yakıt |
| Yön | İzin verilen hareket | Tek yönlü cadde |

## Zayıf nokta ne demektir?

Bir yolun kalabalık olması, onun mutlaka yapısal bir zayıflık olduğu anlamına gelmez. Zayıf nokta; devre dışı kaldığında ağın parçalanmasına, seyahat sürelerinin ciddi biçimde artmasına veya alternatif yolların aşırı yüklenmesine neden olan bileşendir.

Bu noktaları belirlemek için çeşitli merkezilik ölçüleri kullanılır:

- **Derece merkeziliği:** Bir kavşağın kaç doğrudan bağlantısı bulunduğunu ölçer.
- **Aradalık merkeziliği:** En kısa rotaların ne kadarının ilgili düğümden geçtiğini gösterir.
- **Yakınlık merkeziliği:** Bir düğümden diğer noktalara ortalama erişim kolaylığını ölçer.
- **Özvektör merkeziliği:** Önemli kavşaklara bağlı olan kavşakları öne çıkarır.

Aradalık merkeziliği kabaca şöyle hesaplanır:

$$C_B(v) = \sum_{s \neq v \neq t} \frac{\sigma_{st}(v)}{\sigma_{st}}$$

Burada $\sigma_{st}$, $s$ ile $t$ arasındaki en kısa yolların sayısı; $\sigma_{st}(v)$ ise bunlardan $v$ düğümünden geçenlerin sayısıdır. Değeri yüksek bir kavşak, şehrin trafik dünyasındaki “herkesin tanıdığı aracı kişi” gibidir.

| Ölçüm | Yanıtladığı soru | Olası kullanım |
|---|---|---|
| Derece | Kaç yola bağlı? | Yoğun kavşak tespiti |
| Aradalık | Kaç rota buradan geçiyor? | Kritik geçiş analizi |
| Yakınlık | Diğer noktalara ne kadar yakın? | Acil servis konumu |
| Köprü kenar | Kapanırsa ağ bölünür mü? | Köprü ve tünel riski |

## Python ve NetworkX ile küçük bir deney

Aşağıdaki kod örnek bir yol ağı oluşturur, aradalık merkeziliğini hesaplar ve kaldırıldığında ağı bölen kritik yolları bulur:

```python
import networkx as nx

G = nx.Graph()
G.add_weighted_edges_from([
    ('A', 'B', 4),
    ('B', 'C', 2),
    ('C', 'D', 3),
    ('B', 'D', 6),
    ('D', 'E', 2),
    ('E', 'F', 3)
])

centrality = nx.betweenness_centrality(G, weight='weight')
critical_nodes = sorted(
    centrality.items(),
    key=lambda item: item[1],
    reverse=True
)

print('Kritik kavşaklar:', critical_nodes)
print('Kritik yollar:', list(nx.bridges(G)))
```

`betweenness_centrality`, kısa rotalarda sık kullanılan kavşakları sıralar. `bridges` ise kaldırıldığında ağın bağlı bileşen sayısını artıran kenarları döndürür. Gerçek bir projede yol verileri OpenStreetMap üzerinden alınabilir; `osmnx` kütüphanesiyle indirilen ağ doğrudan NetworkX grafına dönüştürülebilir.

## Dayanıklılığı sınamak

Analizin en eğlenceli kısmı kontrollü kaostur: Kritik bir düğümü silip sonuçları yeniden hesaplayın. Ortalama en kısa yol uzuyor mu? Bazı mahalleler tamamen kopuyor mu? Alternatif yollar kapasiteyi karşılıyor mu?

Rastgele kapanmalar ile yüksek merkezilikli yolların hedefli kapanmalarını karşılaştırmak da önemlidir. Ağ rastgele arızalara dayanırken tek bir stratejik köprüye bağımlı olabilir. Böylece yeni bağlantıların nereye yapılacağı, acil durum rotalarının nasıl tasarlanacağı ve bakım önceliğinin hangi yollara verileceği sezgiyle değil, ölçülebilir verilerle belirlenir. Kısacası graf teorisi, şehir haritasını sadece göstermez; haritanın nereden çatlayabileceğini de anlatır.

![ag-teorisiyle-sehrin-49](/img/ag-teorisiyle-sehrin-49.svg)

