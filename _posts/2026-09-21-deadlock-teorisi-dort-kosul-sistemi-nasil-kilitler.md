---
layout: post
title: "Deadlock Teorisi: Dört Koşul Sistemi Nasıl Kilitler?"
math: true
categories: 
  - Bilgi
tags: 
  - deadlock
  - işletim sistemleri
  - eşzamanlılık
  - kaynak yönetimi
  - programlama
toc: true
---

Bir restoranda iki aşçı düşünün: Birinin tava, diğerinin bıçak tuttuğunu; fakat ikisinin de yemeği tamamlamak için diğer araç gerece ihtiyaç duyduğunu hayal edin. Kimse elindekini bırakmazsa mutfak sonsuza kadar bekler. İşletim sistemlerinde bu tatsız tabloya **deadlock**, yani kilitlenme denir.
``
## Deadlock tam olarak nedir?

Deadlock, bir süreç veya iş parçacığı grubunun, yalnızca gruptaki başka bir üyenin gerçekleştirebileceği olayları sonsuza kadar beklemesidir. İşlemci çalışıyor, programlar bellekte duruyor olabilir; ancak ilerleme yoktur. Sistem teknik olarak canlı, pratikte ise donmuştur.

Bir sistemi kaynak tahsis grafiğiyle modelleyebiliriz. Süreçleri $P_i$, kaynakları $R_j$ ile gösterelim. $P_i \rightarrow R_j$ işlemin kaynağı istediğini, $R_j \rightarrow P_i$ ise kaynağın işleme tahsis edildiğini belirtir. Grafikte bir çevrim bulunması, tek örnekli kaynaklarda deadlock anlamına gelir:

$$P_1 \rightarrow R_2 \rightarrow P_2 \rightarrow R_1 \rightarrow P_1$$

Ancak deadlock yalnızca “iki program aynı anda bir şey istedi” diye oluşmaz. Coffman koşulları olarak bilinen dört şartın **aynı anda** sağlanması gerekir.

## Dört gerekli koşul

| Koşul | Anlamı | Günlük hayat benzetmesi |
|---|---|---|
| Karşılıklı dışlama | Bir kaynak aynı anda yalnızca bir süreççe kullanılabilir. | Tek kişilik telefon kulübesi |
| Elde tut ve bekle | Süreç, elindeki kaynağı bırakmadan yenisini bekler. | Tava elindeyken bıçak beklemek |
| Zorla geri alamama | Kaynak süreçten zorla alınamaz. | Aşçının tavasına el koyamamak |
| Döngüsel bekleme | Her süreç, zincirdeki sonraki sürecin kaynağını bekler. | A, B’yi; B, C’yi; C, A’yı bekler |

Bu koşulları mantıksal olarak $M$, $H$, $N$ ve $C$ ile gösterirsek gerekli durum şöyledir:

$$Deadlock \Rightarrow M \land H \land N \land C$$

Başka bir ifadeyle koşullardan **en az birini bozmak**, deadlock oluşumunu engeller. Dördü tek tek masum görünebilir; tehlike, birlikte çalıştıklarında ortaya çıkar.

## Kod üzerinde kilitlenme

Aşağıdaki Python örneğinde iki iş parçacığı kilitleri farklı sırayla edinir:

```python
import threading
import time

kilit_a = threading.Lock()
kilit_b = threading.Lock()

def gorev_1():
    with kilit_a:
        time.sleep(0.1)
        with kilit_b:
            print("Görev 1 tamamlandı")

def gorev_2():
    with kilit_b:
        time.sleep(0.1)
        with kilit_a:
            print("Görev 2 tamamlandı")

threading.Thread(target=gorev_1).start()
threading.Thread(target=gorev_2).start()
```

`gorev_1`, `kilit_a` kaynağını tutup `kilit_b` için bekler. Aynı anda `gorev_2`, `kilit_b` kaynağını tutarak `kilit_a` ister. Kilitler özel kullanımlıdır, zorla geri alınamaz ve bekleme çevrimseldir. Böylece dört koşul da tamamlanır; adeta deadlock tombalasında bütün numaralar çekilmiştir.

## Kilitlenme nasıl önlenir?

En yaygın yöntem, tüm kilitleri **global ve tutarlı bir sırayla** almaktır. Her iki görev de önce `kilit_a`, ardından `kilit_b` edinirse döngüsel bekleme bozulur. Zaman aşımı kullanmak, kaynakları topluca istemek veya başarısız edinme durumunda eldeki kilitleri bırakmak da seçenekler arasındadır.

| Yaklaşım | Bozduğu koşul | Dezavantajı |
|---|---|---|
| Kilit sıralaması | Döngüsel bekleme | Büyük sistemlerde sıra yönetimi zorlaşır |
| Kaynakları baştan isteme | Elde tut ve bekle | Kaynak kullanımı verimsizleşebilir |
| Zaman aşımı ve geri alma | Zorla geri alamama | İşlemi yeniden başlatmak gerekebilir |
| Paylaşılabilir kaynaklar | Karşılıklı dışlama | Her kaynak paylaşılabilir değildir |

Deadlock önleme, kaçınma ve tespit birbirinden farklıdır. Önleme, koşullardan birini tasarım gereği yok eder. Banker algoritması gibi kaçınma yöntemleri sistemi yalnızca **güvenli durumlarda** tutar. Tespit yaklaşımı ise kilitlenmeye izin verir, bekleme grafiğini inceler ve gerekirse süreç sonlandırır.

Özetle deadlock tek bir kötü kilidin değil, dört koşulun kusursuz fakat talihsiz iş birliğinin sonucudur. Kaynak edinme sırasını belirlemek ve kilit kapsamını küçük tutmak, sisteminizin dijital bir bekleme salonuna dönüşmesini büyük ölçüde önler.
