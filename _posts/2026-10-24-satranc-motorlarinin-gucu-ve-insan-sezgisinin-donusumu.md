---
layout: post
title: "Satranç Motorlarının Gücü ve İnsan Sezgisinin Dönüşümü"
math: true
categories: 
  - Bilgi
tags: 
  - satranç
  - yapay zeka
  - satranç motoru
  - algoritma
  - makine öğrenmesi
toc: true
image: /img/satranc-motorlarinin-gucu-55.png
---

![satranc-motorlarinin-gucu-55](/img/satranc-motorlarinin-gucu-55.svg)


Bir zamanlar satranç, insan zekâsının makineler karşısındaki son kalesi sayılıyordu. Bugün telefonlarımızdaki motorlar bile geçmişin dünya şampiyonlarından daha güçlü oynuyor. Bu değişim yalnızca maç sonuçlarını değil; oyuncuların hazırlanma biçimini, güzel hamle anlayışını ve hatta satranç sohbetlerinin kelime dağarcığını dönüştürdü.
``

## Motorlar hamleyi nasıl seçiyor?

Klasik bir satranç motorunun temelinde **arama ağacı** bulunur. Motor, mevcut konumdan oynanabilecek hamleleri dallandırır; rakibin en iyi cevabı vereceğini varsayarak gelecekteki konumları inceler. Bu yaklaşımın özünde minimax düşüncesi vardır:

$$V(s) = max_a min_b V(s_{a,b})$$

Burada $s$ mevcut konumu, $a$ motorun hamlesini, $b$ rakibin cevabını temsil eder. Motor, kendi kazancını artırırken rakibin bunu azaltmaya çalışacağını kabul eder. Ancak satrançtaki olası konumların sayısı astronomiktir. Her hattı oyunun sonuna kadar hesaplamak mümkün olmadığından arama belirli bir derinlikte durdurulur ve konum bir **değerlendirme fonksiyonuyla** puanlanır.

Basitleştirilmiş bir değerlendirme şöyle düşünülebilir:

$$E = 9Q + 5R + 3B + 3N + P + K_s + M$$

$Q$, $R$, $B$, $N$ ve $P$ taşların maddi değerlerini; $K_s$ şah güvenliğini, $M$ ise hareket alanını ifade eder. Gerçek motorlar elbette çok daha karmaşık ölçütler kullanır.

| Özellik | İnsan büyükusta | Modern motor |
|---|---|---|
| Hesaplama | Seçilmiş birkaç varyant | Saniyede milyonlarca konum |
| Değerlendirme | Deneyim ve örüntü tanıma | Arama ve sinir ağı puanlaması |
| Yorulma | Zamanla artar | Donanım elverdiğince sabit |
| Risk algısı | Psikolojiden etkilenir | Sayısal değerlendirmeye dayanır |
| Açıklama yeteneği | Fikrini sözel aktarabilir | Hamleyi verir, gerekçesi yorumlanmalıdır |

## Alfa-beta ve akıllı budama

Motorlar her dalı eşit biçimde araştırmaz. **Alfa-beta budaması**, sonucu değiştiremeyeceği anlaşılan varyantları erkenden terk eder. Aşağıdaki öğretici Python örneği, bu mantığın sadeleştirilmiş hâlidir:

```python
def alphabeta(node, depth, alpha, beta, maximizing):
    if depth == 0 or node.is_terminal():
        return node.evaluate()

    if maximizing:
        value = float('-inf')
        for child in node.children():
            value = max(value, alphabeta(
                child, depth - 1, alpha, beta, False
            ))
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # Bu dal artık sonucu değiştiremez.
        return value

    value = float('inf')
    for child in node.children():
        value = min(value, alphabeta(
            child, depth - 1, alpha, beta, True
        ))
        beta = min(beta, value)
        if alpha >= beta:
            break
    return value
```

Bu kod tam bir satranç motoru değildir; düğümlerin hamle üretme ve değerlendirme yeteneğine sahip olduğunu varsayar. Yine de güçlü motorların neden yalnızca kaba kuvvetten ibaret olmadığını gösterir: doğru sırada arama yapmak, gereksiz yolları elemek kadar önemlidir.

## Sinir ağları neyi değiştirdi?

Stockfish gibi modern motorlar, klasik aramayı **NNUE** adı verilen verimli sinir ağı değerlendirmeleriyle birleştirir. AlphaZero ve Leela Chess Zero yaklaşımında ise motor, çok sayıda oyun üzerinden hangi konumların umut verici olduğunu öğrenir. Böylece maddi kazancı geciktiren, uzun vadeli taş fedaları içeren ve eskiden yalnızca sezgisel görülen hamleler oynayabilir.

İlginç biçimde motorlar insan sezgisini yok etmedi; onu genişletti. Büyükustalar artık açılış hazırlığında motor kullanıyor, çevrim içi yayınlarda değerlendirme çubuğunu takip ediyor ve geçmişte şüpheli sayılan fikirleri yeniden inceliyor. Buna karşılık oyuncular bazen motorun ilk tercihini ezberleyip konumun mantığını kaçırabiliyor.

## Satranç kültüründeki yeni denge

Motor analizi hataları acımasızca görünür kıldı, fakat satrancı daha erişilebilir de yaptı. Amatörler birkaç saniye içinde oyunlarını inceleyebiliyor. Yayıncılar kritik anları sayısal olarak gösterebiliyor; araştırmacılar tarihî maçlara yeni gözle bakabiliyor.

Yine de insan satrancının cazibesi kusursuzluk değildir. Zaman baskısı, cesaret, blöf ve rakibi rahatsız eden pratik kararlar oyunun parçasıdır. Motor bize konumun gerçeğini yaklaşarak gösterir; insan ise o gerçeği sınırlı zamanda anlamlı bir plana dönüştürür. Geleceğin satranç kültürü, makine hesaplaması ile insan hikâyesinin rekabetinden çok iş birliği üzerine kurulacaktır.
