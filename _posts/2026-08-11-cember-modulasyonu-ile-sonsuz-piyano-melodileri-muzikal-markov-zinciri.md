---
layout: post
title: "Çember Modülasyonu ile Sonsuz Piyano Melodileri: Müzikal Markov Zinciri"
math: true
categories: 
  - Proje
tags: 
  - python
  - markov zinciri
  - müzik teorisi
image: /img/cember-modulasyonu-ile-76.png
---

Rastgele nota seçmek kolaydır; kulağa müzik gibi gelmesini sağlamak ise bambaşka bir problemdir. Bu projede Markov zincirini, tonal müzikteki akor ilişkileriyle birleştirerek sürekli yeni piyano melodileri üreteceğiz. Sistem, yalnızca bir sonraki notayı değil, bulunduğu tonal merkezi ve bu merkezin çember üzerindeki komşularını da dikkate alacak. Sonuç: zar atan bir robot değil, küçük ama şaşırtıcı derecede terbiyeli bir besteci.
``
## Neden yalnızca rastgelelik yetmez?

Bir melodide notaların eşit olasılıkla seçildiğini düşünelim. 12 kromatik nota için bu yaklaşımın olasılığı şöyledir:

$$P(n_{t+1}=x)=\frac{1}{12}$$

Bu model teorik olarak her melodiyi üretebilir, fakat çoğunlukla tonal merkez, yön duygusu ve tekrar eden motifler kaybolur. Markov zinciri ise gelecek durumun yalnızca mevcut duruma bağlı olduğunu varsayar:

$$P(X_{t+1}\mid X_t, X_{t-1}, \ldots)=P(X_{t+1}\mid X_t)$$

Müzikte durumumuzu sadece `nota` olarak değil, `(tonalite, derece, oktav)` üçlüsü olarak kurmak daha verimlidir. Örneğin C majördeki `V` derecesi olan G, I derecesi C'ye dönmeye eğilimlidir. Böylece geçiş matrisi, müzikal beklentiyi sayısallaştırır.

| Yaklaşım | Avantajı | Sorunu |
|---|---|---|
| Tam rastgele nota | Çok çeşitli sonuçlar | Tonalite hızla kaybolur |
| Sabit gam içinde rastgelelik | Daha güvenli tınlar | Bir süre sonra mekanikleşir |
| Markov + modülasyon | Yön, tekrar ve sürpriz dengesi | Geçiş ağı tasarlanmalıdır |

## Çember modülasyonu: Tonaliteyi gezdiren pusula

Beşliler çemberinde komşu tonlar ortak notalar bakımından yakındır. C majörden G majöre geçmek, yalnızca bir diyez eklediği için kulağa doğal gelir. Aynı şekilde F majör de C'nin diğer yakın komşusudur. Modülasyon kararını küçük olasılıklarla verirsek melodi bir evde kalır, ama ara sıra komşu mahalleye yürüyüşe çıkar.

| Mevcut ton | Yakın hedefler | Müzikal etki |
|---|---|---|
| C majör | G majör, F majör | Yumuşak genişleme |
| A minör | E minör, D minör | Koyu ama akıcı geçiş |
| G majör | D majör, C majör | Parlaklık veya geri dönüş |

Pratik bir dağılımda tonun korunmasına %70, saat yönündeki komşuya %15, ters yöndeki komşuya %15 verilebilir. Kadans hissi için derece geçişlerine de ağırlık ekleriz: `V → I`, `IV → V` ve `ii → V` güçlü; `I → iii` ise daha yumuşak bir harekettir.

## Python ile çekirdek üretici

Aşağıdaki örnek, dereceler arasında ağırlıklı seçim yapar ve belirli aralıklarla beşliler çemberinde modülasyon dener. `mido` ile MIDI dosyasına dönüştürülebilecek nota adları üretir; ses motoru bağımsız tutulduğu için projeyi kolayca genişletebilirsiniz.

```python
import random

circle = ["C", "G", "D", "A", "E", "B", "F#", "C#", "Ab", "Eb", "Bb", "F"]
major = {
    "C": ["C", "D", "E", "F", "G", "A", "B"],
    "G": ["G", "A", "B", "C", "D", "E", "F#"],
    "F": ["F", "G", "A", "Bb", "C", "D", "E"]
}

transitions = {
    0: ([0, 2, 3, 4], [35, 15, 20, 30]),
    1: ([1, 3, 4],    [20, 35, 45]),
    2: ([1, 3, 4, 5], [20, 20, 40, 20]),
    3: ([0, 1, 4],    [25, 30, 45]),
    4: ([0, 2, 5],    [55, 20, 25])
}

def next_key(key):
    i = circle.index(key)
    return random.choices(
        [key, circle[(i + 1) % 12], circle[(i - 1) % 12]],
        weights=[70, 15, 15]
    )[0]

def melody(length=64):
    key, degree, notes = "C", 0, []
    for step in range(length):
        if step and step % 16 == 0:
            candidate = next_key(key)
            if candidate in major:  # Örnek gam sözlüğümüzün sınırı
                key = candidate
        choices, weights = transitions.get(degree, transitions[0])
        degree = random.choices(choices, weights=weights)[0]
        octave = 4 + random.choice([0, 0, 1])
        notes.append(f"{major[key][degree]}{octave}")
    return notes

print(melody())
```

Buradaki önemli ayrıntı, geçişlerin mutlak notalar yerine derecelerle tanımlanmasıdır. Böylece `V → I` davranışı C'de `G → C`, G'de `D → G` olarak otomatik uyarlanır. Gerçek bir uygulamada tüm 12 majör ve minör gamı ekleyin; ayrıca ritmi ikinci bir Markov zinciriyle üretin. Uzun notaları kadanslarda, kısa notaları geçişlerde daha olası yaparak sistemin piyano cümleleri nefes almasını sağlayabilirsiniz.

Sonsuzluk, tamamen başıboşluk anlamına gelmez. İyi üretici; kuralları yeterince sıkı tutarak tonal kimliği korur, yeterince esnek tutarak da aynı melodiyi iki kez söylemez.

![cember-modulasyonu-ile-76](/img/cember-modulasyonu-ile-76.svg)

