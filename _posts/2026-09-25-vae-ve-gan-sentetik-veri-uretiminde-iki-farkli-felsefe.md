---
layout: post
title: "VAE ve GAN: Sentetik Veri Üretiminde İki Farklı Felsefe"
math: true
categories: 
  - Bilgi
tags: 
  - vae
  - gan
  - sentetik veri
  - üretken yapay zeka
  - derin öğrenme
  - olasılıksal modelleme
toc: true
image: /img/vae-ve-gan-65.png
---

Bir yapay zekâdan daha önce var olmamış bir yüz, ürün tasarımı veya el yazısı rakam üretmesini istediğimizde perde arkasında ilginç bir soru belirir: Model, verinin dünyasını nasıl öğrenmelidir? VAE bu dünyayı düzenli bir olasılık haritasına dönüştürmeye çalışırken GAN, bir sahtekâr ile dedektifi karşı karşıya getirir. İkisi de sentetik veri üretir; fakat gerçekliğe ulaşma felsefeleri oldukça farklıdır.

``

## Ortak hedef, farklı yollar

Elimizde bilinmeyen bir $p_{data}(x)$ gerçek veri dağılımı bulunsun. Üretken modelin amacı, bu dağılıma benzeyen örnekler sağlayan bir $p_{model}(x)$ öğrenmektir. Başka bir deyişle rastgele seçilen gizli değişken $z$, anlamlı bir $x$ örneğine dönüştürülmelidir:

$$z \sim p(z), \qquad x \sim p_{model}(x\vert z)$$

VAE ve GAN arasındaki temel ayrım, bu dönüşümün nasıl öğrenildiğinde yatar. VAE olasılıkları açıkça modelleyip düzenli bir gizli uzay kurar. GAN ise dağılımın formülünü çıkarmak yerine, üretilen örneklerin gerçeklerinden ayırt edilememesini hedefler.

## VAE: Dünyanın olasılıksal haritası

Variational Autoencoder, klasik bir otoenkodere belirsizlik ekler. Kodlayıcı, girdiyi tek bir noktaya sıkıştırmak yerine gizli uzaydaki bir dağılımın ortalamasını ve varyansını öğrenir:

$$q_\phi(z\vert x)=\mathcal{N}(\mu(x),\sigma^2(x))$$

Ardından $z=\mu+\sigma\odot\epsilon$ ve $\epsilon\sim\mathcal{N}(0,I)$ kullanılarak örnekleme yapılır. Bu yeniden parametreleştirme hilesi, rastgele örnekleme varken bile gradyanların ağ boyunca ilerlemesini sağlar.

VAE kaybı iki amacı dengeler:

$$L_{VAE}=L_{reconstruction}+D_{KL}(q_\phi(z\vert x)\\vert p(z))$$

Yeniden oluşturma kaybı çıktının girdiye benzemesini, KL ayrışımı ise gizli uzayın düzenli kalmasını sağlar. Sonuç olarak iki nokta arasında yürüdüğümüzde ara örnekler genellikle anlamlıdır. Bunun bedeli, görsellerin bazen bulanık veya fazla ortalama görünmesidir.

## GAN: Sahtekâr ve dedektif oyunu

GAN mimarisinde üretici $G$, rastgele gürültüden sahte örnek üretir. Ayırt edici $D$ ise örneğin gerçek mi sahte mi olduğunu tahmin eder. İki ağ şu minimax oyununu oynar:

$$\min_G\max_D\;E_{x\sim p_{data}}[\log D(x)]+E_{z\sim p(z)}[\log(1-D(G(z)))]$$

Üretici başarılı oldukça dedektifi kandırır; dedektif geliştikçe üretici daha gerçekçi ayrıntılar öğrenmek zorunda kalır. GAN'ların keskin görseller üretmesinin sırrı budur. Ancak eğitim hassastır. Ayırt edici fazla güçlenirse üretici öğrenemez; üretici birkaç güvenli örneğe saplanırsa mode collapse oluşur.

## Hızlı karşılaştırma

| Özellik | VAE | GAN |
|---|---|---|
| Temel yaklaşım | Olasılıksal kodlama | Rekabetçi öğrenme |
| Gizli uzay | Düzenli ve yorumlanabilir | Daha düzensiz olabilir |
| Görsel kalite | Daha yumuşak | Genellikle daha keskin |
| Eğitim | Görece kararlı | Hassas ve değişken |
| Veri çeşitliliği | Dağılımı kapsama eğilimli | Modları kaçırabilir |
| Uygun kullanım | Temsil öğrenme, anomali tespiti | Fotogerçekçi üretim |

![vae-ve-gan-65](/img/vae-ve-gan-65.svg)


## Kod düzeyinde fark

Aşağıdaki PyTorch benzeri kod, iki yöntemin eğitim zihniyetini özetler:

```python
# VAE: yeniden oluşturma ile düzenliliği birlikte optimize eder.
mu, log_var = encoder(x)
z = mu + (0.5 * log_var).exp() * torch.randn_like(mu)
x_hat = decoder(z)

reconstruction = F.mse_loss(x_hat, x)
kl = -0.5 * torch.mean(1 + log_var - mu.pow(2) - log_var.exp())
vae_loss = reconstruction + kl
vae_loss.backward()

# GAN: üretici, ayırt edicinin sahte örneğe gerçek demesini ister.
z = torch.randn(batch_size, latent_size)
fake = generator(z)
generator_loss = F.binary_cross_entropy(
    discriminator(fake), torch.ones(batch_size, 1)
)
generator_loss.backward()
```

Gerçek uygulamada GAN için ayırt edici ayrıca gerçek ve sahte örneklerle ayrı ayrı güncellenir. Bu nedenle GAN eğitimi, VAE'nin tek birleşik hedefinden daha koreografik bir süreçtir.

## Hangisini seçmeli?

Kontrollü gizli temsiller, veri sıkıştırma veya anomali tespiti gerekiyorsa VAE güçlü bir başlangıçtır. Öncelik yüksek görsel gerçekçilikse GAN daha caziptir. Felsefi olarak VAE, gerçekliği açıklanabilir bir olasılık coğrafyası gibi görür; GAN ise gerçekliği başarılı bir taklit sınavı olarak tanımlar. Biri harita çizer, diğeri kalpazan yetiştirir.
