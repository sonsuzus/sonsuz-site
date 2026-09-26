---
layout: post
title: "Yapay Sinir Ağlarında Dropout: Nöronları Tembellikten Kurtarmak"
math: true
categories: 
  - Bilgi
tags: 
  - yapay zeka
  - derin öğrenme
  - dropout
  - sinir ağları
  - makine öğrenmesi
  - overfitting
toc: true
image: /img/yapay-sinir-aglarinda-24.png
---

![yapay-sinir-aglarinda-24](/img/yapay-sinir-aglarinda-24.svg)


Bir yapay sinir ağı eğitim verisini ezberlemeye başladığında, sınıfın çalışkan öğrencisi gibi görünür; ancak sınav soruları değişince afallar. Dropout, eğitim sırasında bazı nöronları rastgele devre dışı bırakarak bu ezberciliğe müdahale eder. Böylece ağ, bütün yükü birkaç güçlü bağlantının üzerine yıkmak yerine farklı özelliklerden yararlanmayı öğrenir.
``

## Dropout tam olarak ne yapar?

Standart bir katmanda her nöron, önceki katmandan gelen bilgiyi işler ve sonucunu sonraki katmana aktarır. Dropout kullanıldığında ise eğitimde her nöron belirli bir olasılıkla geçici olarak kapatılır. Kapatılan nöron o ileri geçişte çıktı üretmez ve geri yayılım sırasında güncellenmez.

Bir nöronun normal çıktısı $h_i$ olsun. Dropout sonrasında kullanılan çıktı şöyle gösterilebilir:

$$
\tilde{h}_i = m_i h_i, \quad m_i \sim Bernoulli(1-p)
$$

Burada $p$, nöronun kapatılma olasılığıdır. Örneğin $p=0.5$ seçilirse nöronların yaklaşık yarısı her eğitim adımında uyku molasına çıkar. Fakat hangi nöronların kapatılacağı sürekli değiştiği için kimse kalıcı olarak işten kaçamaz.

Modern kütüphaneler genellikle **inverted dropout** uygular:

$$
\tilde{h}_i = \frac{m_i h_i}{1-p}
$$

Bu ölçekleme, eğitim sırasındaki beklenen aktivasyonu korur. Böylece tahmin aşamasında ayrıca çıktı düzeltmesi yapmak gerekmez.

## Ağdaki “tembellik” problemi

Bir ağdaki bazı nöronlar belirli özelliklere aşırı güvenebilir. Örneğin bir kedi sınıflandırıcısı kulak, göz ve gövde biçimini birlikte öğrenmek yerine yalnızca arka plandaki koltuğa odaklanabilir. Eğitim verisindeki kediler çoğunlukla koltuk üzerindeyse sonuç harika görünür; dışarıdaki bir kedi gösterildiğinde model şaşırır.

Dropout, koltuğu algılayan nöronun her zaman kullanılacağını garanti etmez. Bu nedenle diğer nöronlar kulak, bıyık ve pati gibi alternatif ipuçlarını öğrenmek zorunda kalır. Bu davranışa **eş-uyarlanmanın azaltılması** denir.

| Dropout olmadan | Dropout ile |
|---|---|
| Nöronlar birbirine aşırı bağımlı olabilir | Nöronlar daha bağımsız özellikler öğrenir |
| Eğitim başarısı çok hızlı yükselir | Eğitim daha zor ve dalgalı ilerleyebilir |
| Overfitting riski yüksektir | Genelleme performansı artabilir |
| Tek ve sabit bir ağ eğitilir | Çok sayıda alt ağ dolaylı biçimde eğitilir |

## Neden genellemeyi artırır?

Her rastgele dropout maskesi, ana ağın farklı bir alt ağını oluşturur. Eğitim boyunca çok sayıda alt ağ aynı parametreleri paylaşarak öğrenir. Tahmin sırasında bütün nöronlar etkinleştirildiğinde ise yaklaşık bir **model topluluğu** elde edilir. Binlerce modeli ayrı ayrı eğitmek yerine, tek ağ içinde ekonomik bir ensemble etkisi oluşur.

Dropout aynı zamanda gürültü ekleyen bir düzenlileştirme yöntemidir. Model, her adımda değişen iç temsillere rağmen doğru sonucu üretmeye zorlanır. Bu durum, küçük ayrıntılara aşırı uyum sağlamak yerine daha dayanıklı örüntüler keşfetmesine yardımcı olur.

## PyTorch ile kullanım

Aşağıdaki ağ, gizli katmandan sonra aktivasyonların yüzde 30’unu rastgele kapatır:

```python
import torch.nn as nn

class Siniflandirici(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(100, 64),
            nn.ReLU(),
            nn.Dropout(p=0.3),
            nn.Linear(64, 10)
        )

    def forward(self, x):
        return self.model(x)
```

`model.train()` çağrıldığında dropout aktiftir. Doğrulama veya tahmin öncesinde `model.eval()` kullanıldığında kapatılır. Bu ayrım unutulursa sonuçlar her çalıştırmada değişebilir.

## Dropout oranı nasıl seçilir?

| Oran | Olası sonuç |
|---|---|
| $0.1$–$0.2$ | Hafif düzenlileştirme |
| $0.3$–$0.5$ | Yoğun katmanlarda güçlü başlangıç noktası |
| $0.6$ ve üzeri | Öğrenmeyi ciddi biçimde zorlaştırabilir |

Dropout sihirli değnek değildir. Çok küçük veri kümelerinde faydalı olabilirken batch normalization, veri artırma ve ağırlık çürümesiyle birlikte etkisi değişebilir. Özellikle evrişimli ağlarda daha düşük oranlar tercih edilir; bazı modern transformer mimarilerinde ise attention ve bağlantı çıkışlarına uygulanır.

Özetle dropout, nöronları cezalandırmaz; onları takım arkadaşları olmadan da iş yapabilecek şekilde eğitir. Sonuç, tek bir ipucuna bağlanmayan, sürpriz veriler karşısında daha az paniğe kapılan ve gerçek dünyaya daha iyi uyum sağlayan bir modeldir.
