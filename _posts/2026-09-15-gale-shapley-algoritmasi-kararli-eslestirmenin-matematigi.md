---
layout: post
title: "Gale-Shapley Algoritması: Kararlı Eşleştirmenin Matematiği"
math: true
categories: 
  - Bilgi
tags: 
  - gale-shapley
  - kararlı eşleştirme
  - algoritma
  - python
  - ayrık matematik
toc: true
---

Bir grup doktoru hastanelere, öğrencileri üniversitelere veya kullanıcıları tercihlerine göre oyun sunucularına yerleştirdiğimizi düşünelim. Herkesin bir tercih listesi var ve bazı eşleşmeler diğerlerinden daha cazip. Rastgele seçim yapmak kolaydır; zor olan, kimsenin mevcut eşini bırakıp başka biriyle karşılıklı olarak eşleşmek istemediği **kararlı** bir sonuç bulmaktır. İşte Gale-Shapley algoritması bu sosyal dramayı düzenli, kanıtlanabilir ve verimli bir sürece dönüştürür.
``

## Kararlı eşleştirme nedir?

Problemde genellikle eşit büyüklükte iki küme bulunur: $A$ ve $B$. Her katılımcı, karşı kümedeki kişileri en çok tercih edilenden en aza doğru sıralar. Amaç, her elemanın tam bir kişiyle eşleştirildiği bir sonuç üretmektir.

Bir eşleştirmede $a \in A$ ve $b \in B$, mevcut eşlerinden daha çok birbirlerini tercih ediyorsa bu ikiliye **engelleyici çift** denir. Kararlı eşleştirmede böyle bir çift bulunmaz.

$$
\text{Kararlı}(M) \iff \nexists(a,b): b \succ_a M(a) \land a \succ_b M(b)
$$

Burada $M(a)$, $a$ katılımcısının mevcut eşini; $\succ_a$ ise $a$ açısından “daha çok tercih edilir” ilişkisini gösterir.

| Kavram | Anlamı | Sonuca etkisi |
|---|---|---|
| Tam eşleştirme | Herkesin bir eşi vardır | Kimse açıkta kalmaz |
| Engelleyici çift | Birbirlerini mevcut eşlerinden çok isteyen ikili | Kararlılığı bozar |
| Kararlı eşleştirme | Engelleyici çift içermeyen sonuç | Tarafların kaçıp yeni çift kurmasını önler |
| Optimal eşleştirme | Bir taraf için mümkün olan en iyi kararlı sonuç | Teklif yapan tarafı avantajlı kılar |

## Algoritma nasıl çalışır?

Gale-Shapley, **ertelenmiş kabul** yaklaşımını kullanır. $A$ tarafının teklif verdiğini düşünelim:

1. Eşi olmayan bir $A$ katılımcısı, henüz teklif etmediği en yüksek tercihine gider.
2. Teklifi alan $B$ katılımcısı boşsa teklifi geçici olarak kabul eder.
3. Zaten bir teklifi tutuyorsa iki adayı karşılaştırır; daha çok tercih ettiğini tutup diğerini reddeder.
4. Reddedilen kişi sıradaki tercihine teklif verir.
5. Eşleşmemiş teklif sahibi kalmayana kadar süreç devam eder.

“Geçici kabul” kritik ayrıntıdır. Bir katılımcı iyi bir teklifi tutabilir, ancak daha iyisi gelirse fikrini değiştirebilir. Romantik komedi gibi görünse de süreç kesinlikle sona erer: Her teklif sahibi karşı taraftaki herkese en fazla bir kez teklif eder. $n$ kişilik iki grup için en fazla $n^2$ teklif yapılır; dolayısıyla zaman karmaşıklığı $O(n^2)$ olur.

## Python ile uygulama

Aşağıdaki kod, teklif alanların tercih sıralarını sözlük biçiminde önceden hesaplar. Böylece iki adayı karşılaştırmak $O(1)$ zamanda gerçekleştirilebilir.

```python
def gale_shapley(proposers, receivers):
    free = list(proposers)
    next_choice = {p: 0 for p in proposers}
    engaged = {}

    # Küçük sıra değeri, daha yüksek tercih anlamına gelir.
    rank = {
        r: {p: i for i, p in enumerate(order)}
        for r, order in receivers.items()
    }

    while free:
        p = free.pop(0)
        r = proposers[p][next_choice[p]]
        next_choice[p] += 1

        if r not in engaged:
            engaged[r] = p
        else:
            current = engaged[r]
            if rank[r][p] < rank[r][current]:
                engaged[r] = p
                free.append(current)
            else:
                free.append(p)

    return {p: r for r, p in engaged.items()}

students = {
    "Ada": ["X", "Y", "Z"],
    "Bora": ["Y", "X", "Z"],
    "Cem": ["Y", "Z", "X"]
}

schools = {
    "X": ["Bora", "Ada", "Cem"],
    "Y": ["Ada", "Cem", "Bora"],
    "Z": ["Cem", "Bora", "Ada"]
}

print(gale_shapley(students, schools))
```

## Neden sonuç garanti edilir?

Algoritma sonlandığında reddedilmiş bir teklif sahibi, onu reddeden kişinin mevcut veya daha çok tercih ettiği bir adayı tuttuğunu bilir. Bu nedenle sonradan engelleyici çift oluşturamaz. Ayrıca teklifler sonlu olduğu için algoritma sonsuz döngüye girmez.

Önemli bir nüans vardır: Kararlı sonuç her zaman herkes için eşit derecede iyi değildir. Teklif yapan taraf, tüm kararlı eşleştirmeler arasındaki kendisi için en iyi sonucu alırken diğer taraf açısından sonuç daha az avantajlı olabilir. Tercihlerde eşitlikler, eksik listeler veya farklı kapasiteler bulunduğunda model genişletilmelidir. Yine de temel fikir değişmez: Yerel tercihler dikkatlice yönetildiğinde küresel bir kararlılık elde edilebilir.
