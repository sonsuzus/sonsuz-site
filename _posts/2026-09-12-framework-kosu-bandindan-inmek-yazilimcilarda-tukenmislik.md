---
layout: post
title: "Framework Koşu Bandından İnmek: Yazılımcılarda Tükenmişlik"
math: true
categories: 
  - Bilgi
tags: 
  - tükenmişlik
  - zihinsel sağlık
  - yazılım geliştirme
toc: true
---

Yeni bir JavaScript kütüphanesini öğrenirken sosyal medyada onun yerine geçen üç araçla karşılaşmak, yazılım dünyasının pek de komik olmayan şakasıdır. Buna yetişmesi gereken sprintler, gece gelen üretim alarmları ve sürekli değişen gereksinimler eklendiğinde geliştirici yalnızca kod değil, yoğun bir zihinsel yük de taşır. Uzun süre yönetilemeyen bu yük; tükenmişlik, motivasyon kaybı ve işlevsellikte belirgin düşüşle sonuçlanabilir.

``

## Tükenmişlik yalnızca yorulmak değildir

Dünya Sağlık Örgütü tükenmişliği, başarıyla yönetilemeyen kronik iş yeri stresinden kaynaklanan mesleki bir olgu olarak ele alır. Üç temel boyutu vardır: enerji tükenmesi, işe karşı zihinsel uzaklaşma veya sinizm ve mesleki yeterlilik hissinde azalma.

Normal yorgunluk çoğu zaman dinlenmeyle azalır. Tükenmişlikte ise hafta sonu uykusu sistemi yeniden başlatmaya yetmeyebilir; çünkü sorun yalnızca harcanan enerji değil, talep ile kaynak arasındaki kalıcı dengesizliktir.

| Durum | Geçici yorgunluk | Tükenmişlik riski |
|---|---|---|
| Dinlenme sonrası | Belirgin iyileşme | Sınırlı iyileşme |
| Koda yaklaşım | Kısa süreli isteksizlik | Sürekli kaçınma veya sinizm |
| Hata algısı | Öğrenme fırsatı | Kişisel başarısızlık hissi |
| Zaman ölçeği | Saatler veya günler | Haftalar veya aylar |

## Zihinsel yük nasıl birikir?

Basitleştirilmiş bir modelde geliştiricinin günlük yükünü şöyle düşünebiliriz:

$$L = T + C + I + U - R$$

Burada $T$ görev yoğunluğunu, $C$ bağlam değiştirme maliyetini, $I$ kesintileri, $U$ belirsizliği ve $R$ dinlenme ile kurumsal desteği temsil eder. Uzun süre boyunca $L > 0$ kalırsa zihinsel rezerv azalır.

Yeni araç öğrenmek tek başına zararlı değildir. Sorun, öğrenmenin meraktan çıkıp sürekli bir yetersizlik sınavına dönüşmesidir. “Bu kütüphaneyi bilmiyorsam geride kaldım” düşüncesi; seçici öğrenmenin yerini panik hâlinde dokümantasyon tüketimine bırakır. Üstelik yoğun projelerde toplantıdan hata ayıklamaya, oradan kod incelemesine geçmek çalışma belleğini zorlar. İnsan beyni sekmeleri bilgisayar kadar ucuza değiştiremez.

## Erken sinyalleri görünür kılmak

Aşağıdaki Python örneği, haftalık çalışma düzenini kaba biçimde gözlemlemek için kullanılabilir. Bu bir tıbbi tanı aracı değildir; yalnızca yükü konuşulabilir hâle getirir.

```python
def yuk_puani(fazla_mesai, kesinti, ogrenme_baskisi, mola):
    ham_yuk = fazla_mesai * 2 + kesinti + ogrenme_baskisi * 1.5
    return max(0, ham_yuk - mola * 2)

puan = yuk_puani(
    fazla_mesai=6,
    kesinti=12,
    ogrenme_baskisi=7,
    mola=4
)

if puan > 25:
    print("Yüksek yük: iş kapsamını ve desteği ekipçe değerlendirin.")
```

Buradaki amaç insan ruh hâlini sayıya indirgemek değil; fazla mesai, kesinti ve plansız öğrenme gibi etkenlerin maliyetsiz olmadığını göstermektir.

## Framework FOMO’suna karşı sürdürülebilir öğrenme

Her aracı öğrenmek yerine kavramları merkeze almak daha dayanıklıdır. Bir geliştirici HTTP, veri modelleme, eşzamanlılık, test stratejileri ve güvenlik temellerini biliyorsa yeni kütüphaneleri daha hızlı anlamlandırır.

| Baskı odaklı yaklaşım | Sürdürülebilir yaklaşım |
|---|---|
| Her yeni aracı hemen denemek | İhtiyaca göre araç seçmek |
| Mesai dışında zorunlu öğrenmek | Çalışma saatinde öğrenme bütçesi ayırmak |
| Sürekli çevrim içi kalmak | Bildirim ve nöbet sınırları koymak |
| Bireysel kahramanlık | Bilgi paylaşımı ve ekip sahipliği |

Ekipler gerçekçi sprint kapasitesi belirlemeli, odak zamanını korumalı ve teknik borcu planlara dâhil etmelidir. Yöneticiler “dayanıklılığı” daha fazla işi sessizce taşıma becerisi olarak görmemelidir. Bireysel tarafta ise düzenli mola, izin kullanımı, iş dışı kimliği besleyen uğraşlar ve öğrenilecekler listesine bilinçli biçimde “hayır” demek koruyucudur.

Belirtiler uzun sürüyor, günlük yaşamı bozuyor veya yoğun umutsuzluk yaratıyorsa bir psikolog, psikiyatrist ya da uygun sağlık uzmanından destek almak önemlidir. Hiçbir teslim tarihi zihinsel sağlıktan değerli değildir; teknoloji maratonunda en kritik bağımlılık hâlâ insandır.
