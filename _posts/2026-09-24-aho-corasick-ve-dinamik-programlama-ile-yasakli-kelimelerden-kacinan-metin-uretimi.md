---
layout: post
title: "Aho-Corasick ve Dinamik Programlama ile Yasaklı Kelimelerden Kaçınan Metin Üretimi"
math: true
categories: 
  - Bilgi
tags: 
  - aho-corasick
  - dinamik programlama
  - otomat
  - algoritma
  - metin işleme
  - kombinatorik
toc: true
image: /img/aho-corasick-ve-37.png
---

![aho-corasick-ve-37](/img/aho-corasick-ve-37.svg)


Bir alfabenin karakterlerini kullanarak belirli uzunlukta metinler üretmek kolaydır: alfabe boyutu $K$, metin uzunluğu $N$ ise toplam $K^N$ seçenek vardır. Ancak metnin içinde “abc”, “kedi” veya “virus” gibi yasaklı kelimelerin hiç geçmemesini istediğimizde işler karışır. Her dizgiyi tek tek üretip kontrol etmek astronomik derecede pahalıdır. Neyse ki Aho-Corasick otomatı ile dinamik programlamayı birleştirerek tüm geçerli dizgileri üretmeden sayabiliriz.

``

## Problemi neden bir otomat olarak düşünmeliyiz?

Yasaklı kelimeleri kontrol ederken geçmişin tamamını hatırlamamız gerekmez. Yalnızca şimdiye kadar yazdığımız metnin, yasaklı kelimelerden birinin öneki olabilecek en uzun son ekini bilmek yeterlidir.

Örneğin yasaklı kelimeler `aba` ve `bab` olsun. Üretilen metin `...ab` ile bitiyorsa yeni karakter önemlidir: `a` eklenirse `aba` tamamlanır ve durum geçersiz olur. Aho-Corasick, bu tür bilgileri trie düğümleri ve failure bağlantılarıyla temsil eder.

| Yapı | Görevi | Sağladığı avantaj |
|---|---|---|
| Trie kenarı | Bir karakterle sonraki öneke geçer | Kelimelerin ortak öneklerini birleştirir |
| Failure bağlantısı | Eşleşme bozulunca uygun son eke döner | Baştan aramayı önler |
| Terminal işareti | Yasaklı kelimenin tamamlandığını belirtir | Geçersiz durumları tanır |
| Otomat durumu | Metnin ilgili son ekini saklar | DP için kompakt hafıza oluşturur |

Bir düğüm terminalse veya failure zincirinde terminal bir düğüme ulaşıyorsa o durum “tehlikeli” kabul edilmelidir. Çünkü yasaklı kelime metnin sonunda zaten görülmüştür.

## Dinamik programlama modeli

$dp[i][s]$, uzunluğu $i$ olan ve Aho-Corasick otomatının $s$ durumunda biten geçerli dizgilerin sayısı olsun. Başlangıçta boş dizgi kök durumundadır:

$$dp[0][0] = 1$$

Her durumdan alfabedeki tüm karakterleri deneriz. Otomatın geçiş fonksiyonu $go(s,c)$ ile gösterilirse, hedef durum tehlikeli olmadığı sürece geçiş şöyledir:

$$dp[i+1][go(s,c)] += dp[i][s]$$

Sonuç, $N$ karakter işlendiğinde güvenli durumların toplamıdır:

$$C_N = \sum_{s \in Safe} dp[N][s]$$

Bu yaklaşımın zaman karmaşıklığı $O(N \cdot S \cdot K)$ olur. Burada $S$ otomat durumlarının, $K$ ise alfabenin büyüklüğüdür. Kaba kuvvetin $O(K^N)$ maliyetiyle karşılaştırıldığında fark oldukça dramatiktir.

## C++ ile örnek DP

Aşağıdaki bölüm, otomatın daha önce oluşturulduğunu varsayar. `nextState[s][c]` geçişleri, `bad[s]` ise yasaklı bir eşleşmeye ulaşan durumları tutar:

```cpp
const long long MOD = 1'000'000'007;

long long countValid(int n, int stateCount, int alphabetSize,
                     const vector<vector<int>>& nextState,
                     const vector<bool>& bad) {
    vector<long long> current(stateCount, 0), next(stateCount, 0);
    current[0] = 1; // Boş metin kök durumunda başlar.

    for (int length = 0; length < n; ++length) {
        fill(next.begin(), next.end(), 0);

        for (int state = 0; state < stateCount; ++state) {
            if (bad[state] || current[state] == 0) continue;

            for (int ch = 0; ch < alphabetSize; ++ch) {
                int target = nextState[state][ch];
                if (bad[target]) continue;

                next[target] = (next[target] + current[state]) % MOD;
            }
        }
        current.swap(next);
    }

    long long answer = 0;
    for (int state = 0; state < stateCount; ++state)
        if (!bad[state]) answer = (answer + current[state]) % MOD;

    return answer;
}
```

Kodda yalnızca önceki uzunluğun değerleri gerektiği için iki DP satırı kullanılır. Böylece bellek karmaşıklığı $O(N \cdot S)$ yerine $O(S)$ seviyesine iner.

## Dikkat edilmesi gereken ayrıntılar

Failure bağlantısından terminal bilgisini miras almak kritik önemdedir. Aksi hâlde otomat, daha uzun bir durumun son eki olarak tamamlanan yasaklı kelimeleri kaçırabilir. Ayrıca sonuçlar hızla büyüdüğünden çoğu yarışma probleminde modüler aritmetik kullanılır.

Çok büyük $N$ değerlerinde aynı model bir geçiş matrisi hâline getirilebilir ve matris hızlı üs alma ile yaklaşık $O(S^3 \log N)$ sürede çözülebilir. Böylece Aho-Corasick yalnızca kelime arayan bir algoritma olmaktan çıkar; güvenli metinlerin evrenini sayan güçlü bir kombinatorik makineye dönüşür.
