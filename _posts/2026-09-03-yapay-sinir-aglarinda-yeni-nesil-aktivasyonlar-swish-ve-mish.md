---
layout: post
title: "Yapay Sinir Ağlarında Yeni Nesil Aktivasyonlar: Swish ve Mish"
math: true
categories: 
  - Bilgi
tags: 
  - yapay sinir ağları
  - aktivasyon fonksiyonları
  - derin öğrenme
toc: true
---

ReLU yıllarca yapay sinir ağlarının çalışkan kahramanı oldu: basit, hızlı ve çoğu zaman yeterince başarılı. Ancak negatif değerleri tamamen silmesi ve türevinin bazı bölgelerde sıfıra düşmesi, araştırmacıları daha yumuşak alternatiflere yöneltti. Swish ve Mish bu arayışın öne çıkan sonuçlarıdır. Üstel fonksiyon içermelerine rağmen modern işlemcilerde vektörleştirme, çekirdek birleştirme ve yaklaşık hesaplama sayesinde oldukça verimli uygulanabilirler.

``

## Aktivasyon fonksiyonuna neden ihtiyaç var?

Bir sinir ağı katmanı temel olarak

$$z = Wx + b$$

hesabını yapar. Katmanlar yalnızca doğrusal işlemlerden oluşsaydı, yüzlerce katman bile tek bir doğrusal dönüşüme indirgenebilirdi. Aktivasyon fonksiyonu $f(z)$, modele doğrusal olmayan ilişkileri öğrenme gücü kazandırır.

Klasik ReLU şu şekilde tanımlanır:

$$\operatorname{ReLU}(x)=\max(0,x)$$

Hesabı ucuzdur; fakat $x<0$ bölgesinde çıktısı ve türevi sıfırdır. Bir nöron sürekli bu bölgede kalırsa güncellenemez. Buna çoğunlukla **ölen ReLU problemi** denir.

## Swish: Kapısını kendi kontrol eden fonksiyon

Swish, giriş değerini sigmoid ile yumuşak biçimde kapılar:

$$\operatorname{Swish}(x)=x\sigma(\beta x)$$

Burada

$$\sigma(x)=\frac{1}{1+e^{-x}}$$

ve $\beta$ sabit ya da öğrenilebilir bir parametredir. Genellikle $\beta=1$ seçilir; bu sürüm bazı kütüphanelerde **SiLU** adıyla bulunur.

Swish monoton değildir. Küçük negatif girdileri tamamen çöpe atmak yerine sınırlı ölçüde geçirir. Türevi

$$f'(x)=\sigma(x)+x\sigma(x)(1-\sigma(x))$$

olduğundan geçişler ReLU’ya göre daha yumuşaktır. Bu özellik gradyan tabanlı optimizasyonda daha istikrarlı bir yüzey sağlayabilir.

## Mish: Daha yumuşak, biraz daha pahalı

Mish fonksiyonu şöyledir:

$$\operatorname{Mish}(x)=x\tanh(\operatorname{softplus}(x))$$

Buradaki Softplus,

$$\operatorname{softplus}(x)=\ln(1+e^x)$$

olarak tanımlanır. Mish de negatif bölgede küçük çıktılara izin verir ve yukarıdan sınırsızdır. Yumuşak türev yapısı, özellikle derin ağlarda bilgi akışına yardımcı olabilir. Buna karşılık logaritma, üstel fonksiyon ve hiperbolik tanjant gerektirdiği için ham işlem maliyeti Swish ve ReLU’dan yüksektir.

| Fonksiyon | Negatif değerleri geçirir mi? | Düzgünlük | Teorik hesap maliyeti | Tipik kullanım |
|---|---:|---:|---:|---|
| ReLU | Hayır | Keskin geçişli | Çok düşük | Genel amaçlı ağlar |
| Swish/SiLU | Evet | Yumuşak | Orta | CNN ve Transformer modelleri |
| Mish | Evet | Çok yumuşak | Yüksek | Görüntü işleme, deneysel mimariler |
| Hard-Swish | Evet | Parçalı doğrusal | Düşük | Mobil ve gömülü sistemler |

## Donanım bunları nasıl hızlandırıyor?

Swish ve Mish doğrudan bir toplama kadar ucuz değildir. CPU ve GPU’lar `exp`, `log` ve `tanh` işlemlerini özel matematik birimleri, SIMD komutları veya hızlı polinom yaklaşımlarıyla hesaplar. Asıl kazanç çoğu zaman aktivasyonun önceki işlemle **fuse edilmesinden** gelir. Böylece ara sonuçlar belleğe yazılıp tekrar okunmaz.

Mobil donanımda Swish yerine sıkça şu yaklaşım kullanılır:

$$\operatorname{HardSwish}(x)=x\frac{\operatorname{ReLU6}(x+3)}{6}$$

Bu yaklaşık fonksiyon yalnızca toplama, çarpma ve kırpma gerektirir. Dolayısıyla düşük güçlü işlemciler için daha dost canlısıdır.

PyTorch üzerinde fonksiyonları karşılaştırmak oldukça kolaydır:

```python
import torch
import torch.nn.functional as F

x = torch.randn(1_000_000, device="cuda")

relu_result = F.relu(x)
swish_result = F.silu(x)   # x * sigmoid(x)
mish_result = F.mish(x)   # x * tanh(softplus(x))
```

Bu kod aynı tensöre üç aktivasyon uygular. Sağlıklı süre ölçümü için ısınma turları yapılmalı ve GPU işlemlerinden sonra `torch.cuda.synchronize()` çağrılmalıdır; aksi hâlde asenkron çalışma yanıltıcı sonuç üretir.

## Hangisini seçmeli?

Swish çoğu modern mimaride doğruluk ile maliyet arasında güçlü bir dengedir. Mish bazı veri kümelerinde küçük kazanımlar sağlayabilir, ancak sonucu mimariye ve donanıma bağlıdır. Gecikmenin kritik olduğu mobil projelerde ReLU veya Hard-Swish daha mantıklıdır. Kısacası en havalı formülü değil, doğrulama başarısı, enerji tüketimi ve gerçek cihaz gecikmesi birlikte en iyi olan aktivasyonu seçmek gerekir.
