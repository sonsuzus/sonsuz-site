---
layout: post
title: "Zaman Serilerinde LSTM mi, TCN mi? Tekrarlayan Hafıza ile Paralel Evrişimin Düellosu"
math: true
categories: 
  - Bilgi
tags: 
  - lstm
  - tcn
  - zaman serileri
  - derin öğrenme
  - pytorch
  - yapay zeka
toc: true
image: /img/zaman-serilerinde-lstm-42.png
---

Zaman serisi modellemek, geçmişteki ipuçlarına bakarak geleceği tahmin etmeye benzer. LSTM bu işi adım adım ilerleyen güçlü bir hafızayla yaparken Temporal Convolutional Network (TCN), zaman eksenine geniş bir evrişim penceresinden bakar. Peki üretim hattındaki sensör verileri, finansal fiyatlar veya trafik yoğunluğu için hangisini seçmeliyiz? Cevap yalnızca doğrulukta değil; veri uzunluğu, eğitim süresi ve donanım kullanımında saklıdır.
``

## LSTM: Geçmişi taşıyan zincir

LSTM, klasik RNN’lerde görülen gradyan kaybolması sorununu kapılarla azaltır. Her zaman adımında unutma, giriş ve çıkış kapıları hangi bilginin korunacağına karar verir. Basitleştirilmiş hücre güncellemesi şöyledir:

$$c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t$$

Burada $f_t$ unutma kapısı, $i_t$ giriş kapısı ve $c_t$ hücre belleğidir. Bu yapı uzun vadeli ilişkileri öğrenebilir; ancak $t$ anındaki hesaplama $t-1$ sonucuna bağlıdır. Dolayısıyla zaman adımları aynı anda işlenemez. Binlerce ölçüm içeren dizilerde GPU güçlü olsa bile model sırayla yürümek zorundadır: yetenekli ama her basamağa tek tek çıkan bir merdiven yolcusu gibi.

LSTM’nin gizli durumu aynı zamanda sabit boyutlu bir bilgi darboğazıdır. Çok uzun dizilerde geçmişteki ayrıntılar sıkışabilir. Buna karşılık değişken uzunluklu diziler ve adım adım çalışan çevrim içi sistemler için doğal bir çözümdür.

## TCN: Evrişimle zamanda sıçramak

TCN; nedensel, genişletilmiş ve çoğunlukla artık bağlantılı 1B evrişimlerden oluşur. **Nedensel evrişim**, modelin geleceği görmesini engeller. **Genişletme (dilation)** ise filtrenin ardışık noktalar yerine aralıklı örneklere ulaşmasını sağlar. Genişletme oranları $1, 2, 4, 8$ biçiminde artırıldığında alıcı alan hızla büyür.

Çekirdek boyutu $k$, katman sayısı $L$ ve iki katına çıkan genişletmeler için yaklaşık alıcı alan:

$$R = 1 + (k-1)(2^L-1)$$

Örneğin $k=3$ ve $L=6$ olduğunda model 127 zaman noktasını görebilir. Üstelik her konumdaki evrişim bağımsız hesaplanabildiğinden eğitim paralelleştirilebilir. Artık bağlantılar da derin ağlarda gradyan akışını kolaylaştırır.

| Özellik | LSTM | TCN |
|---|---|---|
| Hesaplama | Zaman boyunca sıralı | Büyük ölçüde paralel |
| Uzun bağımlılıklar | Kapılı bellekle | Geniş alıcı alanla |
| Eğitim hızı | Uzun dizilerde yavaş | GPU’da genellikle hızlı |
| Çevrim içi kullanım | Doğal ve durum saklayabilir | Girdi tamponu gerektirir |
| Yorumlanacak ayar | Gizli durum boyutu | Çekirdek, katman, dilation |
| Bellek kullanımı | Durum ve aktivasyonlar | Katman aktivasyonları |

## PyTorch ile küçük bir TCN bloğu

Aşağıdaki blok, geleceğe ait değerleri kullanmamak için evrişim sonucunun sağ tarafını kırpar. Artık bağlantı ise girdiyi çıktıya ekleyerek eğitimi dengeler:

```python
import torch.nn as nn

class TCNBlock(nn.Module):
    def __init__(self, channels, kernel_size, dilation):
        super().__init__()
        padding = (kernel_size - 1) * dilation
        self.padding = padding
        self.conv = nn.Conv1d(
            channels, channels, kernel_size,
            padding=padding, dilation=dilation
        )
        self.activation = nn.ReLU()

    def forward(self, x):
        y = self.conv(x)
        if self.padding:
            y = y[:, :, :-self.padding]
        return self.activation(y + x)
```

Girdi biçimi `(parti, kanal, zaman)` olmalıdır. Birden fazla blok kurarken dilation değerlerini `1, 2, 4, 8` şeklinde artırmak, modelin kısa ve uzun örüntüleri birlikte yakalamasını sağlar.

## Hangisini seçmeli?

Diziler kısa, veri miktarı sınırlı veya sistem her yeni ölçümle gizli durumunu güncelleyecekse LSTM hâlâ güçlü bir başlangıçtır. Çok uzun diziler, büyük mini-batch’ler ve hızlı eğitim hedefleniyorsa TCN çoğu zaman daha verimli olur. Yine de kazananı mimarinin şöhreti değil, zaman sırasını bozmayan doğrulama belirlemelidir. Modelleri aynı parametre bütçesiyle; MAE, RMSE ve gecikme üzerinden karşılaştırın. Kısacası LSTM geçmişi cebinde taşır, TCN ise geçmişe geniş açılı bir objektifle bakar.

![zaman-serilerinde-lstm-42](/img/zaman-serilerinde-lstm-42.svg)

