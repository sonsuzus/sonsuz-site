---
layout: post
title: "Bit Manipülasyonu ve Olimpiyat Soruları: XOR, AND, OR ile Yaratıcı Çözümler"
math: true
categories: 
  - Bilgi
tags: 
  - bit manipülasyonu
  - algoritmalar
  - xor
  - olimpiyat soruları
  - c++
toc: true
image: /img/bit-manipulasyonu-ve-57.png
---

Olimpiyat tipi algoritma sorularında bit operatörleri, yalnızca sayıları ikili tabanda kurcalamak için değil, büyük durum uzaylarını küçük maskelere sıkıştırmak için kullanılır. XOR, AND ve OR; kümeleri, pariteleri, alt kümeleri ve izin verilen seçimleri tek bir makine kelimesinde temsil edebilir. Doğru yerde kullanıldıklarında hem çözümü zarifleştirir hem de karmaşıklığı dramatik biçimde düşürür.

![bit-manipulasyonu-ve-57](/img/bit-manipulasyonu-ve-57.svg)

``

## Önce ikili düşünme alışkanlığı

Bir tamsayıyı bitlerden oluşan bir dizi gibi ele alalım. Örneğin $13=(1101)_2$ sayısında 0., 2. ve 3. bitler aktiftir. Bir bit maskesi, genellikle bir kümenin üyelik bilgisini taşır: $i$. bit 1 ise $i$ elemanı kümededir. Böylece klasik küme işlemleri doğrudan işlemci komutlarına dönüşür.

| Operatör | Bit düzeyindeki anlamı | Küme yorumlaması | Tipik olimpiyat kullanımı |
|---|---|---|---|
| `a & b` | İki bit de 1 ise 1 | Kesişim | Ortak izinleri bulma |
| `a | b` | En az biri 1 ise 1 | Birleşim | Seçenekleri birleştirme |
| `a ^ b` | Bitler farklıysa 1 | Simetrik fark | Parite ve eşleşmemiş elemanlar |

Bir biti test etmek için `mask & (1 << i)` kullanılır. Bit eklemek `mask | (1 << i)`, bit kaldırmak ise `mask & ~(1 << i)` ile yapılır. Bu işlemler, özellikle $n \leq 20$ civarında olan alt-küme DP sorularında vazgeçilmezdir; çünkü tüm durum sayısı $2^n$ olsa da her durum kompakt biçimde saklanır.

## XOR: paritenin süper gücü

XOR'un en değerli özelliği bir elemanın kendisini yok etmesidir: $x \oplus x=0$ ve $x \oplus 0=x$. Ayrıca işlem değişmelidir; yani sıralama önemsizdir. Bu yüzden çift sayıda görünen değerler birbirini götürür. Dizide yalnızca bir sayının tek sayıda geçtiği klasik problemde tüm elemanların XOR'u doğrudan cevaptır.

Daha yaratıcı versiyonlarda her düğüm veya kenar için rastgele bir etiket atanır. Bir yol üzerindeki etiketler XOR'lanarak yolun “parmak izi” üretilir. Ağaç sorularında kökten düğüme kadar olan XOR değerleri saklanırsa, $u$ ile $v$ arasındaki yolun değeri şu olur:

$$P(u,v)=pref[u] \oplus pref[v] \oplus value[LCA(u,v)]$$

Buradaki iptal mekanizması, ortak kök yolundaki parçaları temizler. Bu fikir, yol sorgularında toplam tutmak kadar doğal ama çoğu zaman daha hızlıdır.

```cpp
int uniqueValue(const vector<int>& a) {
    int answer = 0;
    for (int x : a) answer ^= x;
    return answer;
}
```

Bu kod, diğer tüm değerler çift sayıda görünüyorsa tek kalan değeri $O(n)$ zamanda ve $O(1)$ ek bellekle bulur. Ancak dikkat: İki farklı değer tek sayıda görünüyorsa sonuç onların XOR'udur; ek bir bit ayırma tekniği gerekir.

## AND ve OR: mümkün olanı filtrelemek

AND, “herkesin kabul ettiği” bitleri bulur. Örneğin bir takımın tüm üyelerinde bulunan yetenekler, yetenek maskelerinin AND'i ile elde edilir. Bir alt dizinin AND değeri büyütülemez: yeni eleman eklemek yalnızca 1 bitlerini kapatabilir. Bu monotonluk, iki işaretçi veya sparse table çözümlerinin temelidir.

OR ise kapsama sorularında parlar. Her proje bir beceri maskesi taşısın; hedef, tüm becerileri kapsayan en az sayıda projeyi seçmek olsun. Durum `dp[mask]`, elde edilen beceri kümesi `mask` iken minimum proje sayısı olabilir. Yeni proje için geçiş şöyledir:

$$dp[mask \; \vert \; project] = \min(dp[mask \; \vert \; project], dp[mask]+1)$$

```cpp
for (int mask = 0; mask < (1 << skills); ++mask)
    for (int project : projects)
        dp[mask | project] = min(dp[mask | project], dp[mask] + 1);
```

Bu yaklaşımın maliyeti $O(m2^n)$'dir; burada $m$ proje, $n$ beceri sayısıdır. Büyük $n$ için uygun değildir, fakat küçük evrenli olimpiyat sorularında son derece etkilidir.

Bit manipülasyonunda asıl sihir operatörü ezberlemek değildir. Sorudaki “var/yok”, “tek/çift”, “ortak/tüm” ifadelerini fark edip onları maske, parite ve küme işlemine çevirmektir. Bir kez bu çeviriyi yaptığınızda, karmaşık görünen problem çoğu zaman birkaç bitlik bir dansa dönüşür.
