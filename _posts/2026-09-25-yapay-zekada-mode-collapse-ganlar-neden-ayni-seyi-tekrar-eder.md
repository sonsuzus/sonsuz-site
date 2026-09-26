---
layout: post
title: "Yapay Zekâda Mode Collapse: GAN’lar Neden Aynı Şeyi Tekrar Eder?"
math: true
categories: 
  - Bilgi
tags: 
  - yapay zeka
  - gan
  - mode collapse
  - derin öğrenme
  - üretici modeller
  - pytorch
toc: true
image: /img/yapay-zekada-mode-28.png
---

Bir GAN’dan bin farklı insan yüzü üretmesini beklersiniz; model ise aynı kişiye yalnızca farklı şapkalar takıp karşınıza çıkarır. Tebrikler, üreticiniz yaratıcı bir sanatçı olmak yerine tek numarası olan bir illüzyoniste dönüşmüştür! **Mode collapse**, üretici modelin veri dağılımındaki çeşitliliği öğrenmek yerine ayrımcıyı kandıran birkaç güvenli çıktıya saplanmasıdır.


![yapay-zekada-mode-28](/img/yapay-zekada-mode-28.svg)

``

## Önce GAN oyununu anlayalım

Generative Adversarial Network, iki sinir ağının rekabetine dayanır. **Üretici** $G$, rastgele gürültü $z$ üzerinden sahte örnek üretir. **Ayrımcı** $D$ ise gerçek ve sahte örnekleri ayırmaya çalışır. Klasik hedef şöyledir:

$$
\min_G \max_D V(D,G) = E_{x \sim p_{data}}[\log D(x)] + E_{z \sim p_z}[\log(1-D(G(z)))]
$$

İdeal dengede $G$, gerçek veri dağılımını bütünüyle taklit eder. Örneğin veri kümesinde kediler, köpekler ve kuşlar varsa bunların her biri dağılımın birer **modu** olarak düşünülebilir. Fakat üretici, yalnızca çok başarılı bir kedi çizerek ayrımcıyı kandırabildiğini keşfederse diğer modları görmezden gelebilir.

| Beklenen davranış | Mode collapse davranışı |
|---|---|
| Farklı $z$ değerleri farklı örnekler üretir | Farklı $z$ değerleri benzer çıktılara gider |
| Veri dağılımının birçok modu kapsanır | Bir veya birkaç güvenli mod seçilir |
| Kalite ve çeşitlilik birlikte artar | Kalite yüksek görünür, çeşitlilik düşer |
| Gradyanlar dengeli ilerler | Eğitim salınımlı ve kararsızdır |

## Üretici neden kolaya kaçar?

GAN eğitimi sıradan bir optimizasyon değil, hareketli hedeflere sahip iki oyunculu bir oyundur. Ayrımcı güncellendikçe üreticinin takip ettiği kayıp yüzeyi de değişir. Ayrımcı fazla güçlenirse üreticiye yararlı gradyan ulaşmayabilir; fazla zayıf kalırsa da düşük kaliteli örneklere onay verir.

İkinci neden, üreticinin kayıp fonksiyonunda çeşitlilik için doğrudan ödüllendirilmemesidir. On farklı gürültü vektörünü aynı başarılı görüntüye eşlemek ayrımcıyı kandırıyorsa matematiksel açıdan kısa vadeli bir zaferdir. Yüksek öğrenme oranı, küçük veya dengesiz veri kümeleri ve yetersiz ağ mimarileri de bu kestirme yolu cazip hâle getirir.

Collapse durumunu yalnızca görüntülere bakarak değerlendirmek yanıltıcı olabilir. **FID**, üretilen ve gerçek örneklerin özellik dağılımlarını karşılaştırır; **precision** kaliteyi, **recall** ise kapsanan çeşitliliği anlamaya yardım eder. Recall düşükken precision yüksekse model güzel fakat birbirine benzeyen örnekler üretiyor olabilir.

## Hangi çözümler işe yarar?

| Yöntem | Temel fikir | Olası bedel |
|---|---|---|
| Mini-batch discrimination | Ayrımcıya örnekler arası benzerliği gösterir | Ek hesaplama |
| Feature matching | Tek çıktıyı değil, özellik istatistiklerini eşleştirir | Ayrıntılar yumuşayabilir |
| WGAN-GP | Daha anlamlı gradyan ve Lipschitz kısıtı sağlar | Eğitim maliyeti artar |
| Unrolled GAN | Üretici, ayrımcının gelecek adımlarını hesaba katar | Bellek tüketimi yükselir |
| Spectral normalization | Ayrımcının aşırı keskinleşmesini sınırlar | Kapasiteyi kısıtlayabilir |

Basit bir çeşitlilik cezası, farklı gürültülerin farklı çıktılar üretmesini teşvik edebilir. Aşağıdaki PyTorch fonksiyonu, çıktı uzaklığının girdi uzaklığına göre aşırı küçülmesini cezalandırır:

```python
import torch

def diversity_loss(generator, z1, z2, epsilon=1e-8):
    x1 = generator(z1)
    x2 = generator(z2)

    input_distance = torch.mean(torch.abs(z1 - z2))
    output_distance = torch.mean(torch.abs(x1 - x2))

    ratio = output_distance / (input_distance + epsilon)
    return -ratio
```

Bu kayıp, ana üretici kaybına $L_G + \lambda L_{div}$ biçiminde eklenebilir. Negatif oranı küçültmek, çıktıların birbirinden uzaklaşmasını ödüllendirir. Ancak $\lambda$ çok büyük seçilirse model çeşitlilik uğruna anlamsız gürültüler üretebilir.

Sonuç olarak mode collapse tek bir hatadan değil; kayıp fonksiyonu, optimizasyon dengesi, veri dağılımı ve mimarinin etkileşiminden doğar. Çözüm yalnızca daha büyük model kurmak değildir. Kalite ile kapsama birlikte ölçülmeli, üretici ve ayrımcının öğrenme hızları dengelenmeli ve gerekirse WGAN-GP gibi daha kararlı hedefler kullanılmalıdır. Çünkü üretici modelin görevi aynı şaheseri durmadan fotokopilemek değil, dağılımın tamamını öğrenmektir.
