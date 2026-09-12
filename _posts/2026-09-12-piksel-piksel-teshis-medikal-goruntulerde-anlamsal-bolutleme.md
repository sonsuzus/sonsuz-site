---
layout: post
title: "Piksel Piksel Teşhis: Medikal Görüntülerde Anlamsal Bölütleme"
math: true
categories: 
  - Bilgi
tags: 
  - anlamsal bölütleme
  - görüntü işleme
  - medikal yapay zekâ
toc: true
---

Bir röntgen görüntüsünde hastalık bulunduğunu söylemek değerlidir; fakat doktorun asıl sorusu çoğu zaman “Tam olarak nerede ve ne kadar büyük?” olur. Anlamsal bölütleme, görüntüdeki her piksele bir sınıf etiketi atayarak bu soruyu yanıtlar. Böylece tümör, organ, lezyon veya sağlıklı doku sınırları adeta dijital bir boya fırçasıyla işaretlenir.

``

## Sınıflandırmadan bölütlemeye

Klasik görüntü sınıflandırma, bir görüntüyü “tümör var” veya “tümör yok” şeklinde etiketler. Nesne tespiti şüpheli alanı dikdörtgen kutuyla çevreler. Anlamsal bölütleme ise çok daha ayrıntılıdır: Her piksel için tahmin üretir.

Bir görüntüyü $X \in \mathbb{R}^{H \times W \times C}$ ile gösterelim. Burada $H$ yükseklik, $W$ genişlik, $C$ ise kanal sayısıdır. Modelin görevi şu dönüşümü öğrenmektir:

$$f_\theta(X) = \hat{Y}, \qquad \hat{Y} \in \{1,2,\ldots,K\}^{H \times W}$$

$K$, arka plan, organ ve anormallik gibi sınıfların sayısıdır. Sonuçta görüntünün boyutlarını koruyan bir etiket haritası elde edilir.

| Yaklaşım | Çıktı | Medikal kullanım örneği |
|---|---|---|
| Sınıflandırma | Tek etiket | Akciğerde hastalık var mı? |
| Nesne tespiti | Sınırlayıcı kutu | Nodül hangi bölgede? |
| Anlamsal bölütleme | Piksel maskesi | Tümörün kesin sınırı nedir? |

## Model görüntüyü nasıl boyuyor?

U-Net, medikal bölütlemenin en tanınmış mimarilerindendir. Kodlayıcı bölüm görüntünün kenar, doku ve biçim özelliklerini öğrenirken çözümleyici bölüm küçülen özellik haritalarını tekrar özgün çözünürlüğe taşır. Aynı seviyeler arasındaki **skip connection** bağlantıları, küçültme sırasında kaybolabilecek konum bilgisini geri getirir. Kısacası model hem “Bu yapı nedir?” hem de “Hangi pikselde bulunuyor?” sorularını birlikte çözer.

Her piksel için üretilen skorlar softmax ile olasılığa dönüştürülür:

$$P(y_{ij}=k)=\frac{e^{z_{ijk}}}{\sum_{c=1}^{K}e^{z_{ijc}}}$$

Medikal görüntülerde anormal alan genellikle çok küçüktür. Bu nedenle yalnızca piksel doğruluğuna bakmak yanıltıcı olabilir; model her yere “sağlıklı” diyerek yüksek doğruluk yakalayabilir. Bunun yerine Dice katsayısı sık kullanılır:

$$Dice=\frac{2\vert P \cap G\vert }{\vert P\vert +\vert G\vert }$$

Burada $P$ tahmin maskesi, $G$ ise uzman tarafından çizilen gerçek maskedir. Değer $1$’e yaklaştıkça örtüşme iyileşir.

| Ölçüt | Güçlü yönü | Dikkat edilmesi gereken |
|---|---|---|
| Accuracy | Kolay yorumlanır | Sınıf dengesizliğinde yanıltıcıdır |
| IoU | Kesişim ve birleşimi ölçer | Küçük sınır hatalarına duyarlıdır |
| Dice | Küçük lezyonlarda etkilidir | Sınır biçimini tek başına anlatmaz |

## Basit bir maske üretimi

Aşağıdaki PyTorch kodu, modelin ürettiği sınıf skorlarını piksel maskesine dönüştürür:

```python
import torch

model.eval()
with torch.no_grad():
    logits = model(image)          # [1, K, H, W] sınıf skorları
    probabilities = torch.softmax(logits, dim=1)
    mask = probabilities.argmax(dim=1)  # Her pikselin en olası sınıfı

print(mask.shape)  # [1, H, W]
```

`softmax`, sınıf skorlarını olasılıklara çevirir; `argmax` ise her piksel için en yüksek olasılığa sahip sınıfı seçer. Klinik sistemlerde maske doğrudan kabul edilmeden önce düşük güvenli bölgeler işaretlenebilir ve doktor incelemesine sunulabilir.

## Yüksek hassasiyet neden zor?

MR, BT ve ultrason cihazları farklı kontrastlar üretebilir. Hareket artefaktları, belirsiz lezyon sınırları ve uzmanlar arasındaki yorum farkları modeli zorlar. Veri artırma, çok merkezli veri kümeleri, sınıf ağırlıklı kayıplar ve Dice tabanlı kayıp fonksiyonları dayanıklılığı artırır. Üç boyutlu modeller ayrıca komşu kesitlerden yararlanarak anatomik sürekliliği öğrenebilir.

Anlamsal bölütleme doktorun yerine geçen sihirli bir kalem değil, dikkatli kullanılması gereken güçlü bir yardımcıdır. Doğru doğrulama, belirsizlik analizi ve uzman denetimiyle birleştiğinde anormalliklerin hacmini ölçebilir, tedavi planını destekleyebilir ve zaman içindeki değişimi piksel hassasiyetinde izleyebilir.
