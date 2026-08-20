---
layout: post
title: "GAN’ler: Sahtekâr ile Dedektifin Yapay Zekâ Düellosu"
math: true
categories: 
  - Bilgi
tags: 
  - gan
  - derin öğrenme
  - yapay zeka
image: /img/ganler-sahtekar-ile-88.png
---

Bir sanatçının sürekli yeni sahte tablolar yaptığını, karşısında ise bu tabloların gerçek olup olmadığını anlamaya çalışan keskin gözlü bir uzmanın bulunduğunu düşünün. Üretici Çekişmeli Ağlar (Generative Adversarial Networks, GAN), tam olarak bu rekabet fikrini makine öğrenmesine taşır. Bir ağ yeni veri üretirken, diğeri verinin gerçek mi yoksa üretilmiş mi olduğunu ayırt etmeye çalışır. Yarış ilerledikçe üretici daha ikna edici örnekler hazırlamayı, denetleyici ise daha zor kandırılmayı öğrenir.

![ganler-sahtekar-ile-88](/img/ganler-sahtekar-ile-88.svg)

``

GAN mimarisi 2014’te Ian Goodfellow ve çalışma arkadaşları tarafından önerildi. Klasik sınıflandırma modellerinin aksine GAN’in temel amacı bir etiketi tahmin etmek değildir; eğitim verisinin altında yatan dağılıma benzeyen yeni örnekler oluşturmaktır. Örneğin model binlerce kedi fotoğrafı görür, ardından eğitim setindeki belirli bir kediyi kopyalamadan “daha önce var olmamış”, fakat kedi gibi görünen bir görsel üretebilir.

## İki oyuncu, tek hedef

**Generator (G)**, rastgele bir gürültü vektörünü $z$ alır ve bunu sahte bir örneğe dönüştürür: $G(z)$. Bu gürültü, üreticinin ham maddesidir; farklı $z$ değerleri farklı yüzler, manzaralar veya ses parçaları üretebilir. **Discriminator (D)** ise bir örneğin gerçek veri dağılımından mı geldiğine, yoksa generator tarafından mı üretildiğine dair $0$ ile $1$ arasında bir olasılık verir.

| Bileşen | Girdi | Çıktı | Öğrenme amacı |
|---|---|---|---|
| Generator | Rastgele gürültü $z$ | Sentetik veri $G(z)$ | Discriminator’ı kandırmak |
| Discriminator | Gerçek veya sentetik örnek | Gerçeklik olasılığı | Sahte ve gerçeği ayırmak |

Bu oyunun klasik hedef fonksiyonu şöyledir:

$$\min_G \max_D V(D,G)=\mathbb{E}_{x \sim p_{data}}[\log D(x)] + \mathbb{E}_{z \sim p_z}[\log(1-D(G(z)))]$$

Burada discriminator, gerçek örneklerde $D(x)$ değerini 1’e; sahte örneklerde ise $D(G(z))$ değerini 0’a yaklaştırmak ister. Generator bunun tersine çalışır: Ürettiklerinin gerçek kabul edilmesini hedefler. İdeal dengede discriminator, örneğin gerçek mi sahte mi olduğunu ayırt edemez ve yaklaşık $0.5$ olasılık verir.

## Eğitim döngüsü nasıl işler?

Eğitim sırayla yapılır. Önce discriminator gerçek ve sahte örneklerle eğitilir. Ardından discriminator’ın parametreleri geçici olarak sabitlenir; generator, aldığı geri bildirime göre daha inandırıcı örnek üretmek üzere güncellenir. Basitleştirilmiş PyTorch akışı şöyledir:

```python
# 1) Discriminator: gerçeği 1, sahteleri 0 olarak öğrenir
real_loss = criterion(discriminator(real_images), torch.ones(batch_size, 1))
z = torch.randn(batch_size, latent_dim)
fake_images = generator(z)
fake_loss = criterion(discriminator(fake_images.detach()), torch.zeros(batch_size, 1))
(real_loss + fake_loss).backward()
d_optimizer.step()

# 2) Generator: sahte görsellerin gerçek sanılmasını ister
g_optimizer.zero_grad()
g_loss = criterion(discriminator(fake_images), torch.ones(batch_size, 1))
g_loss.backward()
g_optimizer.step()
```

Kodda `detach()` kritik bir ayrıntıdır: Discriminator güncellenirken hata generator’a geri yayılmaz. Generator aşamasında ise hedef etiketi bilinçli biçimde `1` verilir; yani üretici, dedektife “Bunu gerçek san!” baskısı yapar.

## GAN neden hem etkileyici hem huysuzdur?

GAN’ler yüksek kaliteli görüntü sentezi, stil dönüşümü, süper çözünürlük, veri artırma ve sentetik ses üretimi gibi alanlarda güçlüdür. Ancak eğitimleri hassastır. En ünlü problem **mode collapse** durumudur: Generator, veri çeşitliliğini öğrenmek yerine discriminator’ı kandıran birkaç benzer örnek üretmeye takılır.

| Sorun | Belirti | Yaygın yaklaşım |
|---|---|---|
| Mode collapse | Birbirine çok benzeyen çıktılar | WGAN, minibatch discrimination |
| Dengesiz eğitim | Kayıpların kararsız salınımı | Öğrenme oranı ve mimari ayarı |
| Aşırı güçlü discriminator | Generator’ın öğrenememesi | Etiket yumuşatma, düzenlileştirme |

Sonuçta GAN, yalnızca “sahte görsel üreten araç” değildir. Olasılık dağılımlarını rekabet yoluyla öğrenen yaratıcı bir sistemdir. Başarılı bir GAN eğitmek, iki rakibi eşit derecede hırslı ama birbirini tamamen ezmeyecek kadar dengeli tutma sanatıdır.

