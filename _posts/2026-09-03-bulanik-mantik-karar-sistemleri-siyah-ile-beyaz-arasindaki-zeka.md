---
layout: post
title: "Bulanık Mantık Karar Sistemleri: Siyah ile Beyaz Arasındaki Zekâ"
math: true
categories: 
  - Bilgi
tags: 
  - bulanık mantık
  - yapay zeka
  - karar sistemleri
toc: true
---

Klasik mantık dünyasında bir önerme ya doğrudur ya da yanlıştır; başka seçenek yoktur. Gerçek hayat ise bu kadar keskin davranmaz. Bir odanın 24 °C olması kimine göre sıcak, kimine göre ılık olabilir. Bulanık mantık, sıcak-soğuk veya hızlı-yavaş gibi dereceli kavramları matematiksel üyelik değerleriyle temsil ederek bilgisayarlara bu belirsizliği yönetme becerisi kazandırır.

``

## Kesin kümeler neden yetersiz kalır?

Klasik, yani kesin bir kümede eleman ya kümeye aittir ya da değildir. Örneğin 25 °C ve üzerini “sıcak” kabul eden basit bir sistemde 24,9 °C sıcak değilken 25 °C sıcaktır. Aradaki yalnızca 0,1 derecelik farkın karar üzerinde uçurum oluşturması pek doğal görünmez.

Bulanık kümelerde üyelik, $0$ ile $1$ arasında değişir:

$$
\mu_A(x): X \rightarrow [0,1]
$$

Buradaki $\mu_A(x)$, $x$ değerinin $A$ bulanık kümesine ne ölçüde ait olduğunu gösterir. Örneğin 24 °C için “sıcak” üyeliği $0.6$, “ılık” üyeliği ise $0.8$ olabilir. Bu değerler olasılık değildir; kavrama uygunluk dereceleridir.

| Özellik | Klasik mantık | Bulanık mantık |
|---|---|---|
| Doğruluk değeri | Yalnızca 0 veya 1 | 0 ile 1 arasında |
| Sınırlar | Keskin | Kademeli |
| Örnek karar | Sıcak / sıcak değil | Biraz sıcak / oldukça sıcak |
| Kullanım alanı | Net kurallar | Belirsiz ve sözel durumlar |

## Üyelik fonksiyonları

Bir kavramın derecelerini belirlemek için üyelik fonksiyonları kullanılır. Üçgensel üyelik fonksiyonu, basitliği nedeniyle oldukça popülerdir:

$$
\mu(x)=\max\left(\min\left(\frac{x-a}{b-a},\frac{c-x}{c-b}\right),0\right)
$$

Burada $a$ ve $c$ üyeliğin sıfır olduğu sınırları, $b$ ise üyeliğin $1$ olduğu tepe noktasını belirtir. Örneğin “ılık” kavramı için $(a,b,c)=(15,22,29)$ seçilebilir.

| Sıcaklık | Soğuk üyeliği | Ilık üyeliği | Sıcak üyeliği |
|---:|---:|---:|---:|
| 10 °C | 1.0 | 0.0 | 0.0 |
| 20 °C | 0.3 | 0.8 | 0.0 |
| 26 °C | 0.0 | 0.4 | 0.7 |
| 35 °C | 0.0 | 0.0 | 1.0 |

## Bir karar sistemi nasıl çalışır?

Yaygın Mamdani yaklaşımı dört temel aşamadan oluşur:

1. **Bulanıklaştırma:** Sensörden gelen kesin değerler üyelik derecelerine çevrilir.
2. **Kural değerlendirme:** “Eğer sıcaklık yüksekse fan hızlı çalışsın” gibi kurallar uygulanır.
3. **Birleştirme:** Etkinleşen kuralların sonuçları tek bir bulanık çıktı hâline getirilir.
4. **Durulaştırma:** Bulanık sonuç, fan hızının yüzde değeri gibi kesin bir sayıya dönüştürülür.

Örnek bir kural tabanı şöyle olabilir:

- Eğer sıcaklık **soğuk** ise fan **yavaş** çalışsın.
- Eğer sıcaklık **ılık** ise fan **orta** hızda çalışsın.
- Eğer sıcaklık **sıcak** ise fan **hızlı** çalışsın.

Bir giriş aynı anda birden fazla kuralı etkinleştirebilir. Sıcaklık hem $0.4$ derecesinde ılık hem de $0.7$ derecesinde sıcaksa, iki kural birlikte sonuca katkıda bulunur. Ağırlıklı ortalama ile basitleştirilmiş çıktı şöyle hesaplanabilir:

$$
y=\frac{0.4\cdot50+0.7\cdot90}{0.4+0.7}\approx75.45
$$

Yani fan yaklaşık yüzde 75 hızla çalıştırılır.

## Python ile küçük bir örnek

Aşağıdaki kod, sıcak üyeliğini hesaplayıp basit bir fan kararı üretir:

```python
def triangular(x, a, b, c):
    return max(min((x - a) / (b - a),
                   (c - x) / (c - b)), 0)

temperature = 27
warm = triangular(temperature, 20, 25, 30)
hot = triangular(temperature, 24, 32, 40)

# Kuralların önerdiği hızları üyeliklerle ağırlıklandırır.
weights = warm + hot
fan_speed = (warm * 50 + hot * 90) / weights if weights else 0

print(f'Ilık üyeliği: {warm:.2f}')
print(f'Sıcak üyeliği: {hot:.2f}')
print(f'Fan hızı: %{fan_speed:.1f}')
```

Bulanık mantık; klima kontrolü, otomatik frenleme, kamera odaklama, risk değerlendirme ve tıbbi destek sistemlerinde kullanılır. En büyük avantajı, uzmanların sözel bilgisini anlaşılır kurallara dönüştürmesidir. Ancak üyelik fonksiyonları ve kurallar genellikle uzmanlarca tasarlandığından, kötü seçimler kötü sonuçlar üretir. Yine de dünya gri tonlarla doluyken yalnızca sıfır ve birle düşünmek yerine “ne kadar?” sorusunu sormak, çoğu karar sistemini daha insansı ve esnek hâle getirir.
