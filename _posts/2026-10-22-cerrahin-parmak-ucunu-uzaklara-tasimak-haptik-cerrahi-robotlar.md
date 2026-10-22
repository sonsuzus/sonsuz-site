---
layout: post
title: "Cerrahın Parmak Ucunu Uzaklara Taşımak: Haptik Cerrahi Robotlar"
math: true
categories: 
  - Bilgi
tags: 
  - robotik
  - haptik
  - cerrahi robotlar
  - biyomedikal
  - yapay zeka
  - sağlık teknolojileri
toc: true
image: /img/cerrahin-parmak-ucunu-27.png
---

Bir üzümü kabuğunu yırtmadan soymaya çalıştığınızı düşünün; şimdi bunu milimetrik damarların arasında, robot kollarıyla ve ekrana bakarak yaptığınızı hayal edin. Robotik cerrahi yüksek çözünürlüklü görüntü ve hassas hareket kontrolü sağlasa da cerrahın doğal bir yeteneğini sınırlayabilir: dokunmayı. Haptik geri bildirim, robotun karşılaştığı kuvvetleri cerrahın ellerine aktararak bu eksik halkayı tamamlamayı amaçlar.

``

## Haptik geri bildirim nasıl çalışır?

Haptik cerrahi sistem, temelde çift yönlü bir iletişim döngüsüdür. Cerrah ana kontrol kollarını hareket ettirir; robot bu komutları hastanın yanındaki aletlere iletir. Alet uçlarındaki kuvvet ve tork sensörleri dokuyla etkileşimi ölçer. Ölçülen veriler, motorlar aracılığıyla kontrol kollarında direnç veya titreşim olarak yeniden üretilir.

Bu süreç üç temel bileşene dayanır:

1. **Algılama:** Kuvvet, basınç, titreşim ve doku deformasyonu ölçülür.
2. **İletim:** Veriler düşük gecikmeyle kontrol konsoluna taşınır.
3. **Yeniden üretim:** Cerrahın eline kontrollü bir mekanik tepki uygulanır.

İdeal durumda cerrah, sert bir tümör dokusuyla yumuşak çevre dokusu arasındaki farkı yalnızca görüntüden değil, elindeki dirençten de anlayabilir. Sistem adeta robot koluna görünmez sinir uçları ekler.

## Kuvvet ölçekleme ve hareket filtreleme

Robotun hissettiği kuvvetin cerraha bire bir aktarılması her zaman güvenli değildir. Bunun yerine kuvvet ölçekleme uygulanır:

$$F_{el} = kF_{doku}$$

Burada $F_{doku}$ robot ucunun ölçtüğü kuvveti, $F_{el}$ cerraha uygulanan geri bildirimi, $k$ ise ölçekleme katsayısını gösterir. Örneğin $k=0.4$ seçildiğinde 5 newtonluk temas, cerraha 2 newton olarak hissettirilir. Böylece bilgi korunurken yorulma ve ani tepki riski azaltılabilir.

Aynı sistem cerrahın el titremesini de filtreleyebilir. İnsan elindeki küçük, istemsiz hareketler yazılımla bastırılırken bilinçli hareketler küçültülerek robot ucuna aktarılır. Cerrah kontrol kolunu 10 milimetre hareket ettirdiğinde aletin yalnızca 1 milimetre ilerlemesi mümkün olabilir.

| Özellik | Görsel geri bildirim | Haptik geri bildirim |
|---|---|---|
| Doku sertliğini algılama | Dolaylı | Doğrudan kuvvet hissiyle |
| Aşırı baskıyı fark etme | Görüntüde deformasyon gerekir | Direnç anında hissedilebilir |
| Öğrenme biçimi | Göz-el koordinasyonu | Göz-el-dokunma koordinasyonu |
| Temel sınırlama | Derinlik ve görüntü kalitesi | Sensör doğruluğu ve gecikme |

## Hassas operasyonlardaki rolü

Haptik geri bildirim özellikle mikrocerrahi, beyin cerrahisi, damar onarımı ve hassas dikiş işlemlerinde değerlidir. İnce bir damarı tutarken fazla kuvvet uygulamak dokuyu zedeleyebilir; yetersiz kuvvet ise iğnenin veya dokunun kaymasına neden olabilir. Ölçülebilir kuvvet sınırları, cerrahı tehlikeli bölgeye yaklaşırken uyarabilir.

Basitleştirilmiş bir güvenlik denetimi şöyle modellenebilir:

```python
def haptik_uyari(olculen_kuvvet, guvenli_sinir):
    oran = olculen_kuvvet / guvenli_sinir

    if oran >= 1.0:
        return 'hareketi durdur ve güçlü titreşim üret'
    elif oran >= 0.8:
        return 'kontrol kolundaki direnci artır'
    return 'normal geri bildirim uygula'

print(haptik_uyari(1.7, 2.0))
```

Bu örnek, ölçülen kuvvet güvenli sınırın yüzde 80’ine ulaştığında direnci artırır. Gerçek sistemlerde kararlar çok daha yüksek frekansta alınır; sensör birleştirme, mekanik modeller ve hata toleranslı kontrol algoritmaları kullanılır.

## Her dokunuş kusursuz mu?

Henüz değil. İletişim gecikmesi, sensör gürültüsü, sterilizasyon gereksinimleri ve çok küçük kuvvetlerin doğru ölçülmesi önemli mühendislik problemleridir. Gecikmiş geri bildirim, cerrahın gerçekte sona ermiş bir teması hâlâ hissediyormuş gibi tepki vermesine yol açabilir. Bu nedenle kararlı bir kontrol döngüsü, yalnızca güçlü motorlardan değil, doğru zamanlama ve güvenilir yazılımdan doğar.

Gelecekte yapay zekâ, farklı dokuların haptik imzalarını sınıflandırarak cerraha ek uyarılar sunabilir. Ancak amaç cerrahın kararını devralmak değil, görüşüne güvenilir bir dokunma kanalı eklemektir. Kısacası haptik cerrahi robotlar, robotu daha kuvvetli değil, daha ölçülü ve daha hissedebilir hâle getirir.

![cerrahin-parmak-ucunu-27](/img/cerrahin-parmak-ucunu-27.svg)

