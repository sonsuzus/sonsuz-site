---
layout: post
title: "Bilgisayar Görüşüyle Gerçek Zamanlı Sanal Aksesuar Filtresi Geliştirme"
math: true
categories: 
  - Proje
tags: 
  - bilgisayar görüşü
  - artırılmış gerçeklik
  - opencv
image: /img/bilgisayar-gorusuyle-gercek-93.png
toc: true
---

![bilgisayar-gorusuyle-gercek-93](/img/bilgisayar-gorusuyle-gercek-93.svg)


Bir kameraya bakıp ekranda gözlüğü, şapkayı veya komik bir bıyığı yüzünüze kusursuzca oturtmak sihir gibi görünür. Aslında bu etki; yüz tespiti, yüz işaret noktaları (landmark), geometrik dönüşümler ve alfa harmanlama işlemlerinin hızlı bir orkestrasyonudur. Bu projede Python, OpenCV ve MediaPipe kullanarak kameradaki yüzü izleyen, üzerine gerçek zamanlı sanal aksesuar yerleştiren bir artırılmış gerçeklik filtresinin mantığını kuracağız.

``

## Filtrenin temel çalışma zinciri

Sistem her video karesinde aynı döngüyü yürütür: Kameradan görüntü alınır, yüz ve yüz üzerindeki referans noktaları bulunur, aksesuarın konumu ile boyutu hesaplanır ve son olarak saydam PNG görüntüsü kareye birleştirilir. Video saniyede yaklaşık 30 kare gösterdiğinde, bu hesapların her biri için yalnızca yaklaşık $33\,ms$ zamanımız vardır:

$$t_{frame} = \frac{1}{FPS} = \frac{1}{30} \approx 0.033\,s$$

Bu nedenle yalnızca yüzün dikdörtgenini bulmak yerine, göz köşeleri, burun ucu ve alın gibi stabil noktaları izlemek daha iyi sonuç üretir. MediaPipe Face Mesh, yüz üzerinde yüzlerce landmark sağlayarak gözlük gibi detaylı aksesuarların konumlandırılmasını kolaylaştırır.

| Aşama | Görevi | Gözlük filtresindeki karşılığı |
|---|---|---|
| Yüz tespiti | Yüzün olup olmadığını bulur | İşleme başlayacak bölgeyi belirler |
| Landmark tespiti | Yüzdeki referans noktalarını verir | İki gözün merkezi bulunur |
| Geometri | Ölçek, açı ve konumu hesaplar | Gözlük yüzle birlikte döner |
| Kompozitleme | Saydam görseli görüntüye karıştırır | PNG gözlük doğal görünür |

## Geometri: aksesuar neden eğilmeli?

Yüzünüzü sağa yatırdığınızda sabit yatay bir gözlük görüntüsü hemen sahte görünür. Bu yüzden iki göz arasındaki vektörden dönüş açısını hesaplarız. Sol ve sağ göz merkezleri sırasıyla $(x_L, y_L)$ ve $(x_R, y_R)$ ise açı şöyledir:

$$\theta = \operatorname{atan2}(y_R-y_L, x_R-x_L)$$

Gözler arası uzaklık da aksesuarın ölçeği için güçlü bir referanstır:

$$d = \sqrt{(x_R-x_L)^2 + (y_R-y_L)^2}$$

Örneğin gözlük PNG'sinin genişliğini $w = 2.2d$ seçmek, farklı uzaklıklardaki yüzlerde daha tutarlı sonuç verir. `2.2` değeri evrensel bir kural değil; kullandığınız görselin çerçeve genişliğine göre deneyerek ayarlanacak bir katsayıdır.

## Temel uygulama iskeleti

Önce `pip install opencv-python mediapipe numpy` ile bağımlılıkları kurun. Aşağıdaki örnek, landmark koordinatlarından gözler arası mesafeyi hesaplar. Gerçek projede bu değerle PNG'yi yeniden boyutlandırıp döndürmeniz gerekir.

```python
import cv2
import mediapipe as mp
import math

cap = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(
    max_num_faces=1, refine_landmarks=True
)

while cap.isOpened():
    ok, frame = cap.read()
    if not ok:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb)

    if result.multi_face_landmarks:
        h, w = frame.shape[:2]
        points = result.multi_face_landmarks[0].landmark
        left = points[33]   # Sol göz dış köşesi
        right = points[263] # Sağ göz dış köşesi

        x1, y1 = int(left.x * w), int(left.y * h)
        x2, y2 = int(right.x * w), int(right.y * h)
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        distance = math.hypot(x2 - x1, y2 - y1)

        cv2.putText(frame, f"aci={angle:.1f}, olcek={distance:.0f}",
                    (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("AR Filtre", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
```

## Alfa kanalı: siyah kutu sorununu çözmek

Aksesuar görselinizin şeffaf arka planlı RGBA PNG olması gerekir. RGB renk bilgisini, A ise saydamlığı taşır. Piksel bazında karışım şu formülle yapılır:

$$C_{sonuc} = \alpha C_{aksesuar} + (1-\alpha)C_{kamera}$$

| Yöntem | Avantajı | Sınırlaması |
|---|---|---|
| Dikdörtgen yapıştırma | Çok hızlıdır | Arka plan görünür, yapay durur |
| Maske ile kopyalama | Basit ve kullanışlıdır | Yarı saydam kenarlar zayıf kalabilir |
| Alfa harmanlama | Yumuşak ve doğal sonuç verir | Kanal ve boyut yönetimi gerekir |

Son aşamada aksesuarı `cv2.resize` ile ölçekleyin, `cv2.getRotationMatrix2D` ile döndürün ve gözlerin orta noktasına yerleştirin. Çerçevenin görüntü dışına taşmasını kırparak kontrol edin. Daha profesyonel bir sürüm için landmark koordinatlarına üstel hareketli ortalama uygulayın; böylece küçük tespit oynamaları titreşen gözlükler yerine sakin, ikna edici bir AR deneyimine dönüşür.
