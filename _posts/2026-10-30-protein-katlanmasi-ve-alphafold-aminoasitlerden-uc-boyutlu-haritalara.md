---
layout: post
title: "Protein Katlanması ve AlphaFold: Aminoasitlerden Üç Boyutlu Haritalara"
math: true
categories: 
  - Bilgi
tags: 
  - alphafold
  - protein-katlanması
  - biyoinformatik
  - yapay-zeka
  - python
  - yapısal-biyoloji
toc: true
image: /img/protein-katlanmasi-ve-15.png
---

Bir proteinin aminoasit dizisini okumak, katlanmış bir origaminin yapım talimatlarını görmek gibidir: Harfler elinizdedir, ama ortaya çıkacak şekil henüz görünmez. AlphaFold, bu harflerden üç boyutlu yapıya uzanan köprüyü kurar. Peki bilgisayar, biyolojinin bu zorlu bulmacasını nasıl çözer ve tahminlerine ne kadar güvenebiliriz?
``

## Önce mesele: Katlanmak neden zor?

Proteinler, aminoasitlerin peptit bağlarıyla birleştiği zincirlerdir. Ancak görevlerini yalnızca dizileriyle değil, uzaydaki şekilleriyle yerine getirirler. Bir enzimin aktif bölgesi, doğru geometri oluşmadığında anahtarı olmayan kilide benzeyebilir.

Zincirin omurgası dönebilir; yan zincirler, hidrojen bağları, elektrostatik etkileşimler ve hidrofobik etki olası yapıları belirler. Yüz aminoasitli bir zincirde her aminoasit için yalnızca üç seçenek varsaysak bile $3^{100}$ kombinasyon çıkar. Bu, gerçek konformasyon uzayının basitleştirilmiş bir benzetimidir; yine de neden bütün seçenekleri deneyemediğimizi gösterir.

Termodinamik açıdan önemli büyüklük Gibbs serbest enerjisidir: $G = H - TS$. Burada $H$ entalpi, $T$ sıcaklık, $S$ entropidir. Ancak proteinler çözücüleriyle birlikte değerlendirilir; düşük serbest enerji fikri, tek başına pratik bir katlanma algoritması sağlamaz.

## AlphaFold hangi kestirme yolu kullanıyor?

AlphaFold, bütün fiziksel hareketleri sırayla simüle etmek yerine, bilinen yapılardan öğrenilmiş ilişkilerle yapısal tahmin üretir. Özellikle AlphaFold 2, aminoasit dizisini çoklu dizi hizalamalarıyla birlikte işler. Evrim boyunca beraber değişen konumlar, uzayda yakınlık veya işlevsel bağlantı hakkında ipuçları taşıyabilir.

Sinir ağı, dizi ve aminoasit çiftleri arasındaki ilişkileri işler; ardından geometrik modüller üç boyutlu koordinatlar üretir. Tahminin tekrar ağa verilmesi, yani geri besleme, yapının iyileştirilmesine yardımcı olur. Bu süreç, proteinin gerçek zamanda nasıl katlandığını gösteren bir film değildir.

AlphaFold 3 ise difüzyon temelli yaklaşımıyla proteinlerin yanında nükleik asitler ve çeşitli ligandlarla oluşan komplekslerin modellenmesini genişletir. Yine de bir kompleks tahmini, gerçek bağlanmanın deneysel kanıtı sayılmaz.

## Güven puanı: Model nerede tereddüt ediyor?

Bir yapı dosyası güzel görünüyor diye bütünüyle doğru kabul edilmemelidir. AlphaFold 2 çıktılarındaki pLDDT, aminoasit başına yerel güveni özetler. Aşağıdaki sınırlar, kesin doğruluk garantileri değil, pratik yorumlama rehberleridir.

| pLDDT aralığı | Genel yorum | Pratik yaklaşım |
|---|---|---|
| 90–100 | Çok yüksek yerel güven | Yerel yapıyı ayrıntılı incele |
| 70–90 | Genellikle güvenilir | İnce ayrıntılarda dikkatli ol |
| 50–70 | Düşük güven | Güçlü sonuç çıkarmaktan kaçın |
| 0–50 | Çok düşük güven | Düzensizlik olasılığını değerlendir |

Düşük güven mutlaka yanlış tahmin anlamına gelmez; bölge gerçekten esnek veya düzensiz olabilir. Ayrıca iki alanın kendi içindeki yapısı güvenilirken birbirlerine göre konumları belirsiz kalabilir. PAE, bu göreli konum belirsizliğini değerlendirmeye yardımcı olur.

## Python ile tahmini sorgulayalım

Şimdi modeli çalıştırmak yerine çıktısını analiz edelim. [AlphaFold Protein Structure Database](https://alphafold.ebi.ac.uk/) üzerinden PDB biçiminde bir yapı indirip `model.pdb` olarak kaydedin. Bağımlılığı kurun:

```bash
pip install biopython
```

Aşağıdaki kod, her zincirde standart aminoasitlerin alfa karbonlarını bulur, ortalama pLDDT değerini hesaplar ve düşük güvenli konumları listeler:

```python
from statistics import mean
from Bio.PDB import PDBParser, is_aa

structure = PDBParser(QUIET=True).get_structure('af', 'model.pdb')
model = structure[0]

for chain in model:
    scores = []
    uncertain = []

    for residue in chain:
        if not is_aa(residue, standard=True) or 'CA' not in residue:
            continue

        score = residue['CA'].get_bfactor()
        scores.append(score)
        if score < 70:
            uncertain.append(residue.id[1:])

    if scores:
        print(f'Zincir {chain.id}: ortalama pLDDT={mean(scores):.1f}')
        print(f'Düşük güvenli konumlar: {uncertain}')
```

Buradaki kritik ayrıntı, AlphaFold veritabanından indirilen bu PDB dosyalarında pLDDT değerlerinin B-faktörü alanında saklanmasıdır. Deneysel PDB dosyalarında aynı alan farklı anlam taşır; kodu rastgele bir dosyaya uygulamak güven puanı üretmez. Konumlar, ekleme kodlarını da koruyacak şekilde gösterilir. Ortalama puan ise birkaç sorunlu bölgeyi gizleyebilir; listeyi ayrıca inceleyin.

## Tahminden bilimsel sonuca geçerken

Proteinler tek bir donmuş heykel değildir. Ortam, bağlanma ortakları ve kimyasal değişiklikler yapılarını etkileyebilir. Bir tahmin, alternatif konformasyonları veya hastalıkla ilişkili bir mutasyonun bütün sonuçlarını otomatik olarak açıklamaz. Özellikle ilaç tasarımında, güvenilir görünen bir cep bile molekülün gerçekten bağlanacağını garanti etmez.

İyi bir çalışma akışı; doğru diziyi seçmek, güven ölçülerini incelemek, bilinen deneysel verilerle karşılaştırmak ve gerektiğinde laboratuvar doğrulaması planlamaktır. AlphaFold deneyleri gereksiz kılmaz; daha hedefli deneyler tasarlamamızı sağlar. Bilgisayar haritayı çizer, biyoloji ise arazinin hâlâ sürprizlerle dolu olduğunu hatırlatır.

![protein-katlanmasi-ve-15](/img/protein-katlanmasi-ve-15.svg)

