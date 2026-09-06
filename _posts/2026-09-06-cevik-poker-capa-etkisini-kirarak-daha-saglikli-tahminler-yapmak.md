---
layout: post
title: "Çevik Poker: Çapa Etkisini Kırarak Daha Sağlıklı Tahminler Yapmak"
math: true
categories: 
  - Bilgi
tags: 
  - agile
  - planning poker
  - yazılım tahminleme
toc: true
---

Bir geliştirici “Bu iş iki gün sürer” dediğinde odadaki herkes farkında olmadan iki gün çevresinde düşünmeye başlayabilir. İlk söylenen sayı, teknik bir hesaplamadan çok zihinsel bir mıknatısa dönüşür. Çevik Poker veya yaygın adıyla Planning Poker, tahminleri aynı anda ve gizlice açıklatarak bu **çapa etkisini** azaltan ekip tabanlı bir yöntemdir.

``

## Sorun: İlk sayı neden bu kadar güçlü?

Çapa etkisi, insanların belirsiz bir konuda karar verirken karşılaştıkları ilk değere gereğinden fazla ağırlık vermesidir. Örneğin kıdemli geliştirici göreve “3 puan” derse diğer ekip üyeleri başlangıçta 8 düşünmüş olsalar bile görüşlerini 3 veya 5 yönüne çekebilir.

Bu davranışı basitçe şöyle gösterebiliriz:

$$T_{son} = \alpha T_{ilk} + (1-\alpha)T_{kişisel}$$

Burada $T_{ilk}$ duyulan ilk tahmin, $T_{kişisel}$ kişinin bağımsız değerlendirmesi, $T_{son}$ ise açıkladığı tahmindir. $\alpha$ büyüdükçe çapanın etkisi artar. Çevik Poker’in amacı, ilk turda herkesin kartını aynı anda açmasını sağlayarak $\alpha$ değerini mümkün olduğunca sıfıra yaklaştırmaktır.

## Çevik Poker nasıl oynanır?

Ekip önce kullanıcı hikâyesini ve kabul kriterlerini inceler. Ardından herkes görevin karmaşıklığını, belirsizliğini ve iş yükünü bağımsız olarak değerlendirir. Oyuncular genellikle Fibonacci benzeri bir ölçekten kart seçer:

`1, 2, 3, 5, 8, 13, 21`

Kartlar kapalı tutulur ve aynı anda açılır. Tahminler yakınsa ekip hızlıca uzlaşır. Büyük fark varsa en düşük ve en yüksek kartı seçen kişiler gerekçelerini anlatır. Yeni bilgiler ortaya çıktıktan sonra oylama tekrarlanır.

| Geleneksel açık tahmin | Çevik Poker |
|---|---|
| İlk konuşan kişiye bağımlıdır | Tahminler eş zamanlı açıklanır |
| Kıdem ve otorite baskısı oluşabilir | Her katılımcının görüşü görünür olur |
| Tartışma sayı etrafında döner | Tartışma varsayımlar etrafında döner |
| Sessiz anlaşmazlıklar saklı kalabilir | Farklı zihinsel modeller ortaya çıkar |

## Neden saat yerine puan?

Hikâye puanı doğrudan süre değildir; görevin **göreli büyüklüğünü** temsil eder. Ekip bir işi 3, diğerini 6 saat olarak tahmin etmeye çalışmak yerine ikinci işin yaklaşık iki kat daha zor olup olmadığını tartışır.

Kabaca şu model düşünülebilir:

$$Puan \propto Efor \times Karmaşıklık \times Belirsizlik$$

Fibonacci aralıklarının giderek büyümesi de bilinçli bir tercihtir. Küçük görevlerde 2 ile 3 arasındaki fark anlamlı olabilirken devasa ve belirsiz bir iş için 20 ile 21 arasındaki hassasiyet çoğunlukla sahtedir. Tahmin büyüdükçe hata payı da büyür.

## Basit bir dijital oylama örneği

Aşağıdaki Python kodu, kartları gizlice toplar ve herkes oy verdikten sonra sonuçları açar:

```python
votes = {}
team = ["Ada", "Ece", "Mert", "Can"]
valid_cards = {1, 2, 3, 5, 8, 13, 21}

for member in team:
    vote = int(input(f"{member}, kartını seç: "))
    if vote not in valid_cards:
        raise ValueError("Geçersiz Planning Poker kartı")
    votes[member] = vote

print("\nKartlar açılıyor!")
for member, vote in votes.items():
    print(f"{member}: {vote}")

spread = max(votes.values()) - min(votes.values())
print(f"Tahmin aralığı: {spread}")
```

Kod, oyları açıklamadan önce tüm ekip üyelerinden toplar. Böylece sonraki katılımcılar önceki seçimlerden etkilenmez. `spread` değeri yüksekse amaç hemen ortalama almak değil, farkın nedenini konuşmaktır. Belki biri güvenlik gereksinimini, diğeri veri taşıma riskini fark etmiştir.

## Sağlıklı uygulama için küçük kurallar

Planning Poker bir pazarlık veya performans ölçme aracı değildir. Ürün sahibi gereksinimleri açıklayabilir ancak ekibe belirli bir kartı dayatmamalıdır. Görev 13 ya da 21 puana çıkıyorsa daha küçük parçalara bölünmesi düşünülmelidir. Ayrıca ekiplerin puanları birbirleriyle karşılaştırılmamalıdır; bir ekibin 5 puanı başka bir ekibin 8 puanına denk gelebilir.

En değerli çıktı kartın üzerindeki sayı değil, sayı farklarının başlattığı konuşmadır. Çevik Poker geleceği kusursuz biçimde tahmin etmez; fakat bağımsız düşünmeyi korur, gizli varsayımları görünür kılar ve ekibin belirsizlik hakkında ortak bir dil geliştirmesine yardımcı olur.
