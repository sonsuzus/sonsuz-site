---
layout: post
title: "Veri Görselleştirme İlkeleri: Grafiklerle Dürüst ve Anlaşılır Hikâyeler Anlatmak"
math: true
categories: 
  - Bilgi
tags: 
  - veri görselleştirme
  - grafikler
  - istatistik
  - Python
  - tasarım
---

Karmaşık bir veri kümesi, doğru görselleştirildiğinde onlarca sütun ve binlerce satır yerine birkaç saniyede kavranabilen bir hikâyeye dönüşür. Ancak grafikler yalnızca estetik araçlar değildir: eksen seçimi, renk, ölçek ve bağlam kararları okuyucunun sonucu nasıl yorumlayacağını doğrudan etkiler. İyi bir görselleştirme, veriyi “daha güzel” değil; daha doğru, daha erişilebilir ve daha sorgulanabilir hâle getirir.

``

## Önce soruyu, sonra grafiği seçin

Bir grafik türü seçmeden önce cevaplamak istediğiniz soruyu netleştirin. “Satışlar arttı mı?”, “Hangi kategori öne çıkıyor?”, “İki değişken arasında ilişki var mı?” ve “Dağılımın uç noktaları nerede?” sorularının her biri farklı bir görsel dil ister. Grafik, verinin yerine geçmez; verideki örüntüyü görünür kılan bir arayüzdür.

| Analiz sorusu | Uygun grafik | Neden? |
|---|---|---|
| Zaman içindeki değişim | Çizgi grafik | Eğilimleri ve kırılmaları gösterir. |
| Kategorileri karşılaştırma | Sıralı çubuk grafik | Değer farklarını hızlı okutabilir. |
| İki sayısal değişkenin ilişkisi | Saçılım grafiği | Korelasyon, küme ve aykırı değerleri ortaya çıkarır. |
| Değerlerin yayılımı | Histogram veya kutu grafiği | Merkezi eğilim ve dağılımı birlikte gösterir. |
| Parça-bütün ilişkisi | Yığılmış çubuk grafik | Toplam içindeki payları karşılaştırmaya yardım eder. |

Örneğin pasta grafik, az sayıda ve birbirinden belirgin oranlar için kullanılabilir; fakat birbirine yakın on dilimi karşılaştırmak çoğu zaman gereksiz bir göz testine dönüşür. Bu durumda sıralı çubuk grafik daha dürüst ve okunabilirdir.

## Ölçek: Küçük karar, büyük algı

Yanıltıcı grafiklerin en yaygın kaynağı eksenlerdir. Çubuk grafiklerde dikey eksenin sıfırdan başlamaması, küçük farkları devasa görünür kılabilir. Çizgi grafiklerde ise daraltılmış bir eksen bazen değişimin ayrıntısını göstermek için meşrudur; kritik nokta bunun açıkça belirtilmesidir.

Bir değişimin yüzdesi şu şekilde hesaplanır:

$$\text{Yüzde değişim} = \frac{y_{son} - y_{ilk}}{y_{ilk}} \times 100$$

Fakat yüzde artış tek başına yeterli bağlam sunmaz. 10 kullanıcıdan 20 kullanıcıya çıkmak %100 artıştır, ancak mutlak fark yalnızca 10’dur. Bu nedenle mümkün olduğunda hem mutlak değeri hem de oranı gösterin. Örneklem büyüklüğü, veri toplama dönemi ve belirsizlik de grafiğin yakınında yer almalıdır.

## Renk, etiket ve erişilebilirlik

Renk dikkat yönlendirmek içindir, süsleme için değil. Nötr kategorilerde sakin tonlar kullanın; asıl mesajı taşıyan seriyi tek bir vurgu rengiyle öne çıkarın. Kırmızı-yeşil karşıtlığı renk körlüğü olan kullanıcılar için risklidir. Renge ek olarak doğrudan etiket, desen veya farklı çizgi tipi kullanmak daha kapsayıcıdır.

Başlık da bir veri bileşenidir. “Bölgelere Göre Satışlar” nötrdür; “Kuzey Bölgesi Açık Ara Lider” ise yorum içerir. Yorumlu başlık kullanacaksanız, grafiğin gerçekten bu sonucu desteklediğinden emin olun. Kaynağı, ölçü birimini ve tarih aralığını görünür tutmak güveni artırır.

## Python ile temel ve dürüst bir örnek

Aşağıdaki kod, aylık gelirleri sıralı bir çubuk grafikle gösterir. Sıfırdan başlayan eksen ve değer etiketleri karşılaştırmayı şeffaflaştırır.

```python
import matplotlib.pyplot as plt

aylar = ["Ocak", "Şubat", "Mart", "Nisan"]
gelir = [120, 135, 128, 160]

fig, ax = plt.subplots(figsize=(8, 4))
barlar = ax.bar(aylar, gelir, color="#4C78A8")

ax.set_title("Aylara Göre Gelir")
ax.set_ylabel("Gelir (bin TL)")
ax.set_ylim(0, 180)  # Çubuk boyları için dürüst başlangıç
ax.grid(axis="y", alpha=0.25)

for bar, deger in zip(barlar, gelir):
    ax.text(bar.get_x() + bar.get_width() / 2, deger + 3,
            f"{deger}", ha="center")

plt.tight_layout()
plt.show()
```

Son kontrol listesi basittir: Grafik hangi soruyu yanıtlıyor? Eksenler ve birimler açık mı? Renkler anlam taşıyor mu? Belirsizlik veya istisnalar saklanıyor mu? Bu soruların cevabı olumluysa, görseliniz yalnızca etkileyici değil, aynı zamanda güvenilir bir veri anlatısıdır.
