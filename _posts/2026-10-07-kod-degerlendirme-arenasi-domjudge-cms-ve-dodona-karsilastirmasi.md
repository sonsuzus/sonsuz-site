---
layout: post
title: "Kod Değerlendirme Arenası: DOMjudge, CMS ve Dodona Karşılaştırması"
math: true
categories: 
  - Bilgi
tags: 
  - domjudge
  - cms
  - dodona
  - otomatik değerlendirme
  - programlama yarışmaları
  - kod analizi
toc: true
image: /img/kod-degerlendirme-arenasi-71.png
---

Bir programın bilgisayarınızda çalışması, onun doğru olduğu anlamına gelmez. Gizli testler, süre sınırları ve sıra dışı girdiler devreye girdiğinde masum görünen bir çözüm saniyeler içinde “Wrong Answer” olabilir. DOMjudge, CMS ve Dodona; gönderilen kodu derleyip kontrollü biçimde çalıştıran ve sonucunu ölçen sistemlerdir. Ancak aynı işi yapıyor gibi görünseler de yarışma modeli, puanlama yaklaşımı ve eğitim araçları bakımından farklı dünyalara hitap ederler.


![kod-degerlendirme-arenasi-71](/img/kod-degerlendirme-arenasi-71.svg)

``

## Otomatik değerlendirme nasıl çalışır?

Temel süreç bir üretim hattına benzer: Kaynak kod alınır, uygun derleyiciyle derlenir, izole bir ortamda test girdileriyle çalıştırılır ve üretilen çıktı beklenen sonuçla karşılaştırılır. Genel başarı koşulu şöyle gösterilebilir:

$$
\text{Kabul} = \bigwedge_{i=1}^{n}(O_i = E_i) \land (t_i \leq T) \land (m_i \leq M)
$$

Burada $O_i$ programın çıktısını, $E_i$ beklenen çıktıyı, $T$ süre sınırını ve $M$ bellek sınırını temsil eder. Tek bir testte hata oluşması, klasik ICPC modelinde çözümün reddedilmesi için yeterlidir.

Değerlendirme yalnızca metin eşitliği değildir. Ondalıklı sonuçlarda tolerans kullanan özel denetleyiciler, birden fazla doğru cevabı kabul eden checker’lar ve çalışan programla anlık iletişim kuran etkileşimli değerlendiriciler bulunabilir.

## Üç sistemin karakteri

| Sistem | Ana kullanım alanı | Puanlama yaklaşımı | Güçlü tarafı |
|---|---|---|---|
| DOMjudge | ICPC tarzı yarışmalar | Kabul/red ve ceza süresi | Canlı yarışma yönetimi |
| CMS | IOI tarzı yarışmalar | Alt görev ve kısmi puan | Esnek puanlama modelleri |
| Dodona | Eğitim ve alıştırmalar | Test, geri bildirim ve ilerleme | Öğrenci odaklı öğrenme deneyimi |

**DOMjudge**, takım yarışmaları için tasarlanmıştır. Yarışma süresi, yanlış gönderim cezaları, skor tablosu dondurma ve clarification yönetimi gibi özellikleriyle dijital bir hakem masası gibidir. Kurum içi algoritma yarışmalarında da sıkça tercih edilir.

**CMS**, yani Contest Management System, özellikle IOI modeline uygundur. Bir sorunun kolay alt görevinden puan alıp zor kısmında başarısız olmak mümkündür. Alt görev puanları $w_j$ ile gösterilirse toplam sonuç şu şekilde modellenebilir:

$$
S = \sum_{j=1}^{k} w_j \cdot p_j, \qquad 0 \leq p_j \leq 1
$$

**Dodona** ise yarıştan çok öğrenmeye odaklanır. Öğretmenler alıştırma serileri oluşturabilir, öğrencilerin ilerlemesini izleyebilir ve daha açıklayıcı geri bildirimler sunabilir. Böylece sistem yalnızca “yanlış” demez; hatanın hangi kavramla ilişkili olabileceğini göstermeye çalışır.

## Basit bir çıktı denetleyicisi

Aşağıdaki Python fonksiyonu, satır sonlarındaki gereksiz boşlukları yok sayarak iki çıktıyı karşılaştırır:

```python
def normalize(text):
    return [line.rstrip() for line in text.strip().splitlines()]


def check_output(expected, actual):
    expected_lines = normalize(expected)
    actual_lines = normalize(actual)

    if expected_lines == actual_lines:
        return True, "Accepted"

    return False, "Wrong Answer: satırlar eşleşmiyor"
```

`normalize` fonksiyonu platform farklarından veya gereksiz boşluklardan kaynaklanan sahte hataları azaltır. Gerçek sistemlerde buna süre ölçümü, çıkış kodu kontrolü, sinyal yakalama ve ayrıntılı hata raporları da eklenir.

## Güvenlik neden kritik?

Gönderilen kod güvenilir kabul edilmez. Bir çözüm sonsuz döngüye girebilir, aşırı bellek tüketebilir ya da dosya sistemine erişmeye çalışabilir. Bu nedenle değerlendirme işçileri container, cgroup, namespace veya benzeri sandbox teknikleriyle sınırlandırılır. Ağ erişimi kapatılır; işlem sayısı, CPU süresi ve bellek kullanımı denetlenir.

| İhtiyaç | Daha uygun seçim |
|---|---|
| ICPC benzeri takım yarışması | DOMjudge |
| Alt görevli olimpiyat soruları | CMS |
| Ders, ödev ve sürekli geri bildirim | Dodona |

Sonuç olarak “en iyi sistem” yoktur; doğru probleme uygun sistem vardır. Hızlı ve rekabetçi bir yarışma için DOMjudge, ayrıntılı puanlama için CMS, öğrenciyi süreç boyunca yönlendirmek için Dodona öne çıkar. Seçim yaparken yalnızca kurulum kolaylığına değil, puanlama modeline, güvenli çalıştırma altyapısına ve beklenen geri bildirim düzeyine bakmak gerekir.
