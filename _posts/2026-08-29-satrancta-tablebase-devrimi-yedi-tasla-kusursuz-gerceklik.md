---
layout: post
title: "Satrançta Tablebase Devrimi: Yedi Taşla Kusursuz Gerçeklik"
math: true
categories: 
  - Bilgi
tags: 
  - satranç
  - tablebase
  - algoritmalar
---

Satranç motorları çoğu zaman milyonlarca hamleyi değerlendirerek güçlü tahminler yapar; ancak taşlar iyice azaldığında tahmine gerek kalmaz. **Oyun sonu tabloları** ya da tablebase'ler, yedi taşa kadar her yasal konumun sonucunu önceden hesaplayan devasa veritabanlarıdır. Bir konum için cevap nettir: beyaz kazanır, siyah kazanır ya da oyun beraberedir. Dahası, doğru hamle de bellidir. Bu nedenle tablebase kullanan bir motor, kapsanan oyun sonunda “çok iyi” değil, matematiksel olarak kusursuz oynar.

``

Tablebase fikrinin temelinde konum uzayı bulunur. Bir satranç konumu yalnızca taşların karelerinden ibaret değildir; sıra kimde, rok hakkı var mı, en passant hedefi oluşmuş mu gibi bilgiler de önem taşır. Yine de oyun sonlarında bu ayrıntılar azalır ve problem geriye doğru çözülebilir. Örneğin iki şah ve bir vezir içeren bir konumda, mat olmuş durumlar başlangıç noktasıdır. Ardından bu mat konumlara zorla ulaşabilen konumlar işaretlenir. Bu işlem, tüm konumlar sınıflandırılana kadar sürer.

Matematiksel açıdan bir konumun değeri şöyle ifade edilebilir:

$$V(p) \in \{\text{Kazanış}, \text{Beraberlik}, \text{Kayıp}\}$$

Burada $p$ konumdur. Sırası gelen oyuncu, kazanışa götüren en az bir hamle varsa kazanır; bütün yasal hamleler rakibin kazanışına gidiyorsa kaybeder. Döngüsel konumlar ve zorunlu ilerleme kuralları ise beraberlik analizinin en ilginç kısmını oluşturur.

| Motorun normal araması | Tablebase sorgusu |
|---|---|
| Değerlendirme fonksiyonuna dayanır | Kesin sonuca dayanır |
| Derinlik sınırlı olabilir | Kapsanan konum bütünüyle çözülmüştür |
| “+0.80” gibi yaklaşık skor üretir | Kazanış, kayıp veya beraberlik verir |
| Hata yapma ihtimali vardır | Doğru veriyle hata yapmaz |

Bu veritabanları genellikle **retrograd analiz** ile üretilir. Önce daha az taşlı bitişler çözülür, sonra bir taşın alınmasıyla o bitişlere geçebilen daha büyük pozisyonlar hesaplanır. Örneğin altı taşlı bir konumun sonucunu bulurken, taş alışından sonra oluşabilecek beş taşlı konumların bilgisi kullanılabilir. Böylece çözüm, küçükten büyüğe inşa edilir.

Yedi taş sınırı kulağa mütevazı gelse de konum sayısı baş döndürücüdür. Taş türleri, kare kombinasyonları, şahların yasallığı ve hamle sırası birleştiğinde milyarlarca durum ortaya çıkar. Bu yüzden Syzygy gibi yaygın tablebase setleri sıkıştırılmış dosyalar hâlinde onlarca, hatta yüzlerce gigabayt alan kaplayabilir. Motorlar bu dosyaları RAM'e tamamen almak zorunda değildir; diskten sorgulama veya çevrim içi servis kullanabilir.

Aşağıdaki örnek, Python ile bir UCI motoruna tablebase yolu tanımlama fikrini gösterir. Kod doğrudan hamle hesaplamaz; motorun Syzygy dosyalarından yararlanabileceği ortamı hazırlar:

```python
import chess.engine

engine = chess.engine.SimpleEngine.popen_uci("stockfish")
engine.configure({"SyzygyPath": "/veri/syzygy"})

# Motor, yedi veya daha az taşlı uygun konumlarda
# arama yerine tablebase sonucunu kullanabilir.
engine.quit()
```

Tablebase'lerin şaşırtıcı yönü, insan sezgisine aykırı hamleler önerebilmesidir. Bazen taş kazanmak yerine uzak bir şah hamlesi gerekir; çünkü alınan taş, teorik beraberlik kuralını tetikleyebilir. Burada **DTZ** (sıfır piyon hamlesi ya da taş alma hamlesine uzaklık) ve **DTM** (mata uzaklık) ölçüleri devreye girer.

| Ölçüt | Anlamı | Pratik önemi |
|---|---|---|
| DTM | Mata kalan hamle sayısı | En kısa zorunlu matı gösterir |
| DTZ | Sıfırlayıcı hamleye uzaklık | 50 hamle kuralını yönetmeye yardım eder |
| WDL | Kazanış/beraberlik/kayıp | Sonucun ana sınıfıdır |

Sonuç olarak tablebase, satrancın küçük evrenlerinde eksiksiz bir hakemdir. Açılışta strateji, orta oyunda hesap gücü önemini korur; fakat taşlar yediye düştüğünde oyun, devasa bir önceden çözülmüş bulmacaya dönüşür. İnsan oyuncu içinse bu veriler yalnızca “en iyi hamle” kaynağı değil, oyun sonlarının neden bazen bu kadar tuhaf ve büyüleyici olduğunu anlatan eşsiz bir laboratuvardır.
