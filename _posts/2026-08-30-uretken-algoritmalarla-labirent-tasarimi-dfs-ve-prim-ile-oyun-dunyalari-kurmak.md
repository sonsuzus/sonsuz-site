---
layout: post
title: "Üretken Algoritmalarla Labirent Tasarımı: DFS ve Prim ile Oyun Dünyaları Kurmak"
math: true
categories: 
  - Proje
tags: 
  - algoritmalar
  - procedural-generation
  - python
---

Rastgele bir labirent üretmek, birkaç duvarı gelişigüzel yerleştirmekten çok daha fazlasıdır: oyuncuya keşif hissi veren, çözülebilir ve görsel olarak okunabilir bir topoloji tasarlamaktır. Üretken algoritmalar bu işi kurallı rastlantısallıkla yapar. Aynı kod, farklı bir tohumla her seferinde yeni bir dünya çıkarırken; her dünyada başlangıçtan çıkışa ulaşılabilmesini garanti eder.
``

Labirenti bir graf olarak düşünmek en sağlam teorik başlangıçtır. Her hücre bir düğüm, komşu hücreler arasındaki geçitler ise kenardır. İdeal bir labirent, bağlı ve döngüsüz bir graf olan **ağaçtır**. Hücre sayısı $V$ ise açılan geçit sayısı tam olarak $E = V - 1$ olur. Bu özellik sayesinde iki hücre arasında yalnızca bir tekil yol bulunur; oyuncu yanlış koridora girdiğinde gerçekten geri dönmek zorunda kalır.

## Derinlik öncelikli arama: Uzun koridorların mimarı

DFS (Depth-First Search), rastgele seçilen bir hücreden başlar ve ziyaret edilmemiş bir komşu buldukça derine iner. Çıkmaza ulaştığında geri izleme yapar. Bu davranış, uzun ve kıvrımlı koridorları doğal olarak üretir. Klasik DFS'yi oyun için değiştirmek adına komşu seçiminde tamamen eşit olasılık kullanmak zorunda değiliz: hedef yönüne küçük bir ağırlık vermek, giriş-çıkış arasındaki ana rotayı daha anlamlı kılar.

Aşağıdaki Python örneği, hücre duvarlarını kaldırarak DFS tabanlı bir labirent üretir. `seed` parametresi, hata ayıklama ve günlük mücadele labirentlerini yeniden üretmek için önemlidir.

```python
import random

def dfs_labirent(genislik, yukseklik, seed=None):
    rng = random.Random(seed)
    ziyaret = {(0, 0)}
    yigin = [(0, 0)]
    gecitler = set()

    def komsular(x, y):
        adaylar = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        return [(a, b) for a, b in adaylar if 0 <= a < genislik and 0 <= b < yukseklik]

    while yigin:
        x, y = yigin[-1]
        yeni = [n for n in komsular(x, y) if n not in ziyaret]
        if not yeni:
            yigin.pop()
            continue
        sonraki = rng.choice(yeni)
        ziyaret.add(sonraki)
        gecitler.add(tuple(sorted(((x, y), sonraki))))
        yigin.append(sonraki)

    return gecitler
```

Buradaki `gecitler`, görselleştirme katmanının hangi iki hücre arasındaki duvarı sileceğini söyler. Zaman karmaşıklığı $O(V+E)$'dir. Kare ızgarada her hücrenin en fazla dört komşusu olduğundan pratikte $O(V)$ gibi davranır.

## Prim yaklaşımı: Daha dengeli keşif alanları

Rastgeleleştirilmiş Prim algoritması, ziyaret edilmiş alanın sınırındaki aday duvarları tutar ve bunlardan birini seçerek yeni hücre ekler. Sonuç, DFS'nin “tek bir tünele dalan” karakterine göre daha dallı ve merkezî görünür. Oyuncunun görüş alanında birden fazla karar noktası görmek istediğiniz bulmaca oyunlarında bu fark değerlidir.

| Özellik | Rastgele DFS | Rastgele Prim |
|---|---|---|
| Baskın şekil | Uzun koridorlar | Sık kavşaklar |
| Geri izleme hissi | Yüksek | Orta |
| Oyuncu karar sayısı | Daha az, daha derin | Daha çok, daha erken |
| Uygun kullanım | Gerilim ve keşif | Hızlı bulmaca, açık alan hissi |

Prim'i modifiye etmenin eğlenceli yolu, sınır duvarlarına ağırlık vermektir. Örneğin çıkıştan uzak hücrelere $w = 1 + 0.05d$ ağırlığı tanımlanabilir; burada $d$, hücrenin çıkışa Manhattan uzaklığıdır. Böylece algoritma önce uzak bölgelere yayılmaya eğilim gösterir. Ters ağırlık ise çıkış çevresini daha karmaşık yapar.

## Mükemmel labirentten oyun labirentine

Ağaç yapısı adil ve çözülebilir olsa da her zaman en eğlenceli sonuç değildir. Kontrollü döngüler eklemek için, üretim sonrasında kapalı duvarların küçük bir yüzdesini açabilirsiniz. Örneğin $p = 0.03$ ile duvarların yüzde üçünü kaldırmak alternatif rotalar üretir. Ancak anahtarlar, kapılar veya düşman devriyeleri varsa döngü oranını düşük tutmak; oyuncunun zihinsel haritasını korur.

Son olarak kaliteyi yalnızca algoritmaya bırakmayın. BFS ile girişten çıkışa en kısa yolu hesaplayın, yol uzunluğunu ölçün ve çok kısa labirentleri yeniden üretin. Bir hedef metrik olarak $L / \sqrt{V}$ oranını kullanabilirsiniz: değer büyüdükçe oyuncunun kat edeceği yol, alan boyutuna göre uzar. Algoritma rastgele olabilir; fakat iyi üretken tasarım, rastlantıyı ölçen, sınırlayan ve oyuncu deneyimine dönüştüren tasarımdır.
