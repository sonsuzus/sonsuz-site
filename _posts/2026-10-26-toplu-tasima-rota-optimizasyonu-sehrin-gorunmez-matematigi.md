---
layout: post
title: "Toplu Taşıma Rota Optimizasyonu: Şehrin Görünmez Matematiği"
math: true
categories: 
  - Bilgi
tags: 
  - rota optimizasyonu
  - toplu taşıma
  - çizge teorisi
  - doğrusal programlama
  - veri bilimi
  - akıllı şehirler
image: /img/toplu-tasima-rota-48.png
---

Sabah işe giderken otobüsün tıklım tıklım, karşı yönden gelen aracın ise neredeyse boş olduğunu gördünüz mü? Bu dengesizlik yalnızca kötü şans değildir; yolcu talebi, araç kapasitesi ve sefer sıklığı arasındaki optimizasyon probleminin görünür sonucudur. Toplu taşıma planlaması, milyonlarca olası rota arasından hem yolcuyu hem işletmeciyi memnun edecek bir denge bulmaya çalışır.

![toplu-tasima-rota-48](/img/toplu-tasima-rota-48.svg)

``
Bir toplu taşıma ağı, **çizge teorisi** kullanılarak modellenebilir. Duraklar düğüm, duraklar arasındaki bağlantılar ise kenar olarak düşünülür. Her kenara seyahat süresi, mesafe, maliyet ve beklenen yoğunluk gibi ağırlıklar atanır. Böylece şehir haritası, algoritmaların üzerinde çalışabileceği matematiksel bir ağa dönüşür.

Yolcu talebi genellikle bir **başlangıç-varış matrisi** ile ifade edilir. $D_{ij}$ değeri, belirli bir zaman aralığında $i$ bölgesinden $j$ bölgesine gitmek isteyen yolcu sayısını gösterir. Sabah ve akşam değerleri farklı olacağından tek bir sabit matris yeterli değildir. Akıllı kart kayıtları, GPS verileri, mobil uygulama sorguları ve nüfus bilgileri kullanılarak saatlik talep tahminleri oluşturulur.

| Veri kaynağı | Sağladığı bilgi | Temel sınırlama |
|---|---|---|
| Akıllı kart | Biniş zamanı ve durağı | İniş noktası her zaman bilinmez |
| GPS | Araç konumu ve gecikme | Yolcu amacı hakkında bilgi vermez |
| Mobil uygulama | Aranan başlangıç ve varış | Her yolcuyu temsil etmez |
| Anket | Tercih ve memnuniyet | Pahalıdır ve çabuk eskiyebilir |

Optimizasyonun amaç fonksiyonu çoğunlukla yolcuların toplam seyahat ve bekleme süresini azaltırken işletme maliyetini kontrol altında tutar. Basitleştirilmiş bir model şöyle yazılabilir:

$$
\min Z = \alpha \sum_p T_p + \beta \sum_p W_p + \gamma \sum_r C_r x_r
$$

Burada $T_p$ yolcu $p$ için araç içindeki süreyi, $W_p$ bekleme süresini, $C_r$ ise $r$ rotasının işletme maliyetini gösterir. $x_r$, rotanın kullanılıp kullanılmadığını veya kaç araçla işletileceğini temsil eder. $\alpha$, $\beta$ ve $\gamma$ katsayıları hedeflerin önemini belirler. Beklemek psikolojik olarak daha yorucu algılandığı için çoğu modelde $\beta$, $\alpha$ değerinden büyük seçilebilir.

Elbette matematiğin keyfini kaçırmayı seven kısıtlar da vardır! Araç kapasitesi aşılmamalı, sürücü çalışma sürelerine uyulmalı, filo sayısı geçilmemeli ve her bölge asgari hizmet almalıdır:

$$
q_{r,t} \leq K_r \cdot f_{r,t}
$$

Bu eşitsizlikte $q_{r,t}$ ilgili rota ve saatteki talebi, $K_r$ araç kapasitesini, $f_{r,t}$ ise sefer sayısını belirtir.

| Yaklaşım | Güçlü yönü | Uygun olduğu durum |
|---|---|---|
| Dijkstra | En kısa yolu hızlı bulur | Tek yolcunun rota seçimi |
| Doğrusal programlama | Açıklanabilir ve ölçülebilir sonuç üretir | Sefer sıklığı ve filo dağıtımı |
| Genetik algoritma | Büyük arama uzaylarını keşfeder | Yeni hat tasarımı |
| Pekiştirmeli öğrenme | Değişen koşullara uyum sağlar | Gerçek zamanlı araç yönetimi |

Aşağıdaki Python örneği, talebe göre basit bir saatlik sefer sayısı hesaplar:

```python
import math

def gerekli_sefer(talep, kapasite, hedef_doluluk=0.85):
    etkin_kapasite = kapasite * hedef_doluluk
    return math.ceil(talep / etkin_kapasite)

saatlik_talep = 720
sefer = gerekli_sefer(saatlik_talep, kapasite=100)
print(f"Saatte en az {sefer} sefer planlanmalı.")
```

Buradaki hedef doluluk oranı, aracın tamamen doldurulmasını önleyerek konfor ve ani talep artışları için pay bırakır. Ancak gerçek sistemlerde aktarmalar, trafik, engelli erişimi, gecikme olasılığı ve bölgesel adalet de hesaba katılır.

Başarılı rota optimizasyonu yalnızca en kısa veya en ucuz ağı kurmak değildir. Amaç; erişilebilir, dayanıklı ve adil bir sistem tasarlamaktır. Kısacası iyi planlanmış bir metro hattı, yolcunun fark etmediği binlerce veri noktası ve matematiksel karar sayesinde “tam zamanında” gelir.
