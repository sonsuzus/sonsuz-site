---
layout: post
title: "Flashcard Arenasında Üç Rakip: Anki, Mnemosyne ve Mochi"
math: true
categories: 
  - Program
tags: 
  - flashcard
  - anki
  - mnemosyne
  - mochi
  - aralıklı tekrar
  - öğrenme
toc: true
image: /img/flashcard-arenasinda-uc-93.png
---

Bir bilgiyi öğrenmek kolay, onu üç ay sonra hatırlamak ise bambaşka bir oyundur. Flashcard uygulamaları bu oyunda beynimize küçük ama düzenli paslar atar. Anki, Mnemosyne ve Mochi aynı temel fikri, yani **aralıklı tekrarı**, farklı arayüzler ve çalışma modelleriyle uygular. Gelin bu üç aracı karşılaştıralım ve kartların neden doğru zamanda karşımıza çıktığını anlayalım.

![flashcard-arenasinda-uc-93](/img/flashcard-arenasinda-uc-93.svg)

``

## Aralıklı tekrar neden işe yarar?

İnsan belleği, kullanılmayan bilgiyi zamanla silikleştirir. Basitleştirilmiş bir unutma eğrisi şu şekilde gösterilebilir:

$$R(t)=e^{-t/S}$$

Burada $R(t)$ bilgiyi hatırlama olasılığı, $t$ son tekrardan beri geçen süre, $S$ ise belleğin dayanıklılığıdır. Bir kartı başarıyla hatırladığımızda $S$ büyür; böylece bir sonraki tekrar daha ileri bir tarihe taşınabilir.

Basit bir planlayıcı, yeni aralığı yaklaşık olarak şöyle hesaplayabilir:

$$I_{yeni}=I_{eski}\times E\times P$$

$I$ tekrar aralığını, $E$ kartın kolaylık katsayısını, $P$ ise kullanıcının verdiği performans puanını temsil eder. Gerçek uygulamalar başarısızlıkları, gecikmiş tekrarları ve öğrenme geçmişini hesaba katan daha gelişmiş modeller kullanır. Dolayısıyla amaç her kartı her gün göstermek değil, **unutmaya yaklaşırken** göstermektir.

## Üç uygulama, üç farklı karakter

| Özellik | Anki | Mnemosyne | Mochi |
|---|---|---|---|
| Temel yaklaşım | Güçlü planlama ve özelleştirme | Sade, akademik odaklı tekrar | Notlar ile kartları birleştirme |
| Kullanım hissi | Ayrıntılı fakat öğrenme eğrisi yüksek | Geleneksel ve doğrudan | Modern ve görsel |
| Kart yapısı | Şablonlar, alanlar ve eklentiler | Soru-cevap merkezli kartlar | Markdown tabanlı bağlantılı notlar |
| Uygun kullanıcı | Kontrolü seven yoğun öğrenci | Dikkat dağıtmayan araç arayan kişi | Not ağı kurmak isteyen kullanıcı |
| Öne çıkan yön | Geniş ekosistem ve gelişmiş zamanlama | Açık kaynaklı, yalın deneyim | Kartlar arasında bağlantı kurabilme |

### Anki: Ayar panelini sevenlerin laboratuvarı

Anki; kart şablonları, etiketler, medya desteği ve eklentileriyle oldukça esnektir. Modern sürümlerde FSRS gibi, geçmiş tekrar verilerinden yararlanarak daha verimli aralıklar üretmeyi amaçlayan zamanlama seçenekleri bulunur. Buna karşılık ilk deste hazırlamak, alanlarla şablonların farkını anlamak ve ayarları düzenlemek başlangıçta yorucu olabilir.

Dil öğrenenler, tıp öğrencileri ve binlerce kart yöneten kullanıcılar için güçlü bir seçenektir. Fakat her ayarı değiştirmek zorunda değilsiniz; varsayılanlarla başlayıp gerçek ihtiyaca göre ilerlemek daha sağlıklıdır.

### Mnemosyne: Gösterişsiz ama disiplinli

Adını Yunan mitolojisindeki hafıza tanrıçasından alan Mnemosyne, aralıklı tekrar dünyasının köklü araçlarındandır. Arayüzü modern uygulamalar kadar parlak görünmeyebilir; buna karşın kart oluşturma ve puanlama akışı nettir. Açık kaynak yaklaşımı ve araştırma odaklı geçmişi önemli avantajlarıdır.

“Not sistemi değil, yalnızca düzgün çalışan bir tekrar aracı istiyorum” diyorsanız Mnemosyne mantıklı bir adaydır. Daha küçük eklenti ekosistemi ve sınırlı görsel cilası ise bazı kullanıcıları Anki veya Mochi’ye yöneltebilir.

### Mochi: Not alırken kart üretmek

Mochi, Markdown notları ile flashcard sistemini aynı ortamda buluşturur. Kartlar arasında bağlantı kurabilmek, tek tek gerçekleri ezberlemek yerine kavram ağı oluşturmayı kolaylaştırır. Özellikle yazılım, tarih veya felsefe gibi ilişkisel konularda bu yaklaşım değerlidir.

Ancak zengin bağlantılar kurmak, otomatik olarak iyi öğrenme anlamına gelmez. Kartlar kısa, açık ve tek bir bilgiyi ölçer durumda olmalıdır. Ayrıca çevrim içi özellikler ve ücretlendirme seçenekleri zamanla değişebileceğinden güncel planlar kontrol edilmelidir.

## Mini bir zamanlayıcı nasıl çalışır?

Aşağıdaki Python kodu, doğru yanıtta aralığı büyüten, yanlış yanıtta kartı ertesi güne döndüren basitleştirilmiş bir modeldir:

```python
def sonraki_aralik(mevcut_gun, puan, kolaylik=2.2):
    # 0-2 başarısız, 3-5 başarılı kabul edilir.
    if puan < 3:
        return 1

    performans = 0.8 + (puan - 3) * 0.2
    yeni_aralik = mevcut_gun * kolaylik * performans
    return max(1, round(yeni_aralik))

print(sonraki_aralik(7, 4))  # Yaklaşık 15 gün
```

Bu örnek öğreticidir; gerçek planlayıcılar çok daha fazla veri kullanır. Yine de temel fikir açıktır: başarı aralığı büyütür, başarısızlık kartı yaklaştırır.

## Hangisini seçmeli?

Maksimum özelleştirme ve büyük deste yönetimi için **Anki**, sade ve açık kaynaklı bir çalışma düzeni için **Mnemosyne**, bağlantılı Markdown notlarıyla öğrenmek için **Mochi** öne çıkar. En iyi sistem, en gelişmiş algoritmaya sahip olan değil, her gün açmayı sürdürebildiğiniz sistemdir. Önce 20 kartlık küçük bir deste hazırlayın, bir hafta deneyin ve kararınızı gerçek çalışma alışkanlığınıza göre verin.
