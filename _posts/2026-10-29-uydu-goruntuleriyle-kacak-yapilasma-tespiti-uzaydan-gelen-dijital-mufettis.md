---
layout: post
title: "Uydu Görüntüleriyle Kaçak Yapılaşma Tespiti: Uzaydan Gelen Dijital Müfettiş"
math: true
categories: 
  - Proje
tags: 
  - uydu görüntüleri
  - görüntü işleme
  - yapay zeka
  - uzaktan algılama
  - python
  - değişim tespiti
toc: true
image: /img/uydu-goruntuleriyle-kacak-81.png
---

Bir arsada hafta sonu aniden yükselen bir yapı, yerdeki denetim ekiplerinin gözünden kaçabilir; fakat yüzlerce kilometre yukarıdaki uydular için durum farklıdır. Düzenli aralıklarla çekilen uydu görüntüleri, şehirlerin nasıl değiştiğini kaydeden dev bir zaman makinesi gibidir. Görüntü işleme algoritmaları bu kayıtları karşılaştırarak yeni çatıları, temel kazılarını ve bina genişlemelerini otomatik biçimde işaretleyebilir.
``

## Temel fikir: Önce ve sonra görüntülerini karşılaştırmak

Kaçak yapılaşma tespitinin merkezinde **değişim tespiti** bulunur. Aynı bölgeye ait farklı tarihlerde çekilmiş iki görüntü kullanılır. İlk görüntüyü $I_1(x,y)$, sonraki görüntüyü $I_2(x,y)$ ile gösterirsek en basit fark haritası şöyle hesaplanır:

$$D(x,y)=\vert I_2(x,y)-I_1(x,y)\vert $$

$D(x,y)$ değeri büyüdükçe ilgili pikselde önemli bir değişiklik yaşandığı düşünülür. Ancak uydu görüntüleri biraz huysuzdur: Güneş açısı, bulutlar, mevsim, gölgeler ve sensör farklılıkları da yüksek fark üretebilir. Bu nedenle doğrudan piksel çıkarmak tek başına güvenilir değildir.

İlk adım, görüntüleri coğrafi olarak aynı hizaya getiren **kayıt (registration)** işlemidir. Ardından parlaklık normalizasyonu, bulut maskeleme ve gürültü azaltma uygulanır. Birkaç piksellik hizalama hatası bile binaların kenarlarını sahte değişim olarak gösterebilir.

| Yöntem | Güçlü yanı | Zayıf yanı | Uygun senaryo |
|---|---|---|---|
| Piksel farkı | Hızlı ve basit | Işık değişiminden etkilenir | Küçük ve temiz veri kümeleri |
| Spektral indeks | Malzeme ayrımında başarılı | Sensör bantlarına bağımlıdır | Bitki ve yapı ayrımı |
| Nesne tabanlı analiz | Şekil ve alanı kullanır | Segmentasyon ayarı gerekir | Düzenli kent dokusu |
| Derin öğrenme | Karmaşık örüntüleri öğrenir | Etiketli veri ve GPU ister | Büyük ölçekli denetim |

## Beton mu, boş arsa mı?

Uydular yalnızca kırmızı, yeşil ve mavi renkleri görmez. Yakın kızılötesi gibi spektral bantlar sayesinde bitki, toprak ve beton daha kolay ayrılabilir. Örneğin yapılaşmış alanları vurgulamak için NDBI kullanılabilir:

$$NDBI=\frac{SWIR-NIR}{SWIR+NIR}$$

Burada $SWIR$ kısa dalga kızılötesi, $NIR$ ise yakın kızılötesi banttır. Yüksek NDBI değerleri yapılaşmış yüzeylere işaret edebilir. Yine de çıplak toprak benzer sonuç verebildiği için indeksler; doku, kenar ve geometrik özelliklerle desteklenmelidir.

Aşağıdaki Python örneği iki gri seviye görüntü arasındaki belirgin değişimleri çıkarır:

```python
import cv2

once = cv2.imread("once.png", cv2.IMREAD_GRAYSCALE)
sonra = cv2.imread("sonra.png", cv2.IMREAD_GRAYSCALE)

# Küçük sensör gürültülerini ve keskin ışık farklarını yumuşatır.
once = cv2.GaussianBlur(once, (5, 5), 0)
sonra = cv2.GaussianBlur(sonra, (5, 5), 0)

fark = cv2.absdiff(once, sonra)
_, maske = cv2.threshold(fark, 35, 255, cv2.THRESH_BINARY)

# Dağınık pikselleri temizleyip değişen bölgeleri birleştirir.
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
maske = cv2.morphologyEx(maske, cv2.MORPH_CLOSE, kernel)

cv2.imwrite("degisim_maskesi.png", maske)
```

Bu kod bir başlangıç prototipidir. Gerçek projede görüntüler önce ortorektifiye edilmeli, bulutlar elenmeli ve bulunan bölgeler bina biçimine göre filtrelenmelidir. Örneğin yalnızca belirli alandan büyük, köşeli ve kompakt bölgeler aday kabul edilebilir.

## Yapay zekâ sahneye çıkıyor

U-Net gibi segmentasyon ağları her pikseli **bina** veya **bina değil** şeklinde sınıflandırabilir. İki tarihin bina maskeleri karşılaştırıldığında yeni yapılar ortaya çıkar. Siamese ağlar ise görüntü çiftlerini birlikte değerlendirerek değişimi doğrudan öğrenir. Başarı; doğruluk yerine çoğunlukla precision, recall ve IoU ile ölçülür:

$$IoU=\frac{\vert Tahmin\cap Gerçek\vert }{\vert Tahmin\cup Gerçek\vert }$$

Yine de algoritmanın işaretlediği her yeni bina kaçak değildir. Sonuçların ruhsat kayıtları ve imar verileriyle karşılaştırılması gerekir. Sistem hüküm veren bir robot değil, denetçiye öncelikli bölgeleri gösteren dijital bir yardımcı olmalıdır. Mahremiyet, veri güncelliği ve itiraz mekanizmaları da tasarımın parçasıdır. Doğru kurulduğunda bu yaklaşım, kilometrelerce alanı tarayıp belediye ekiplerine adeta uzaydan bir büyüteç sunar.

![uydu-goruntuleriyle-kacak-81](/img/uydu-goruntuleriyle-kacak-81.svg)

