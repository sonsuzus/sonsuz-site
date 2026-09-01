---
layout: post
title: "Kombinatoryal Oyunlarda XOR: Kazananı Tek Sayıyla Bulmak"
math: true
categories: 
  - Bilgi
tags: 
  - kombinatoryal oyunlar
  - xor
  - rekabetçi programlama
toc: true
---

İki oyuncunun sırayla hamle yaptığı bir oyunda bütün olasılıkları gezmek ilk bakışta doğal görünür. Fakat taş yığınları büyüdüğünde oyun ağacı küçük bir çalı olmaktan çıkıp dijital bir ormana dönüşür. Kombinatoryal oyun teorisi, uygun koşullardaki bir oyunun durumunu XOR işlemiyle tek bir sayıya indirerek kazananı belirlememizi sağlar.

``

## Önce oyun modelini tanıyalım

Klasik teorinin doğrudan uygulanabilmesi için oyun genellikle **tarafsız** olmalıdır: Bir konumda yapılabilecek hamleler, sıranın hangi oyuncuda olduğuna göre değişmemelidir. Ayrıca şans unsuru bulunmaz, oyuncular tüm bilgiyi görür ve oyun sonlu sayıda hamlede biter. Normal oyun kuralında hamle yapamayan oyuncu kaybeder.

Bir konumu iki sınıftan birine ayırabiliriz:

| Konum türü | Anlamı | Temel özellik |
|---|---|---|
| P-konumu | Önceki oyuncu için kazançlı | Sıradaki oyuncu optimum oyunda kaybeder |
| N-konumu | Sıradaki oyuncu için kazançlı | Kazandıran en az bir hamle vardır |

P-konumundan yalnızca N-konumlarına gidilir. N-konumunda ise en az bir P-konumuna geçiş vardır. Bu küçük gözlem, tüm teorinin motorudur.

## Nim ve XOR sürprizi

Nim oyununda birkaç taş yığını bulunur. Oyuncu sırası geldiğinde yalnızca bir yığından istediği kadar taş alır. Son taşı alan kazanır. Yığın boyutları $a_1,a_2,\ldots,a_n$ ise oyunun özeti olan **Nim toplamı** şöyledir:

$$S=a_1\oplus a_2\oplus\cdots\oplus a_n$$

Buradaki $\oplus$, bit düzeyinde XOR işlemidir. Sonuç $S=0$ ise konum kaybeden, $S\neq 0$ ise kazanan konumdur.

| İşlem | Aynı bitler | Farklı bitler | Elde taşır mı? |
|---|---:|---:|---:|
| Toplama | Değişken | Değişken | Evet |
| XOR | 0 | 1 | Hayır |

Örneğin yığınlar $3,4,7$ olsun. İkilik gösterimleriyle $011\oplus100\oplus111=000$ elde edilir. Dolayısıyla ilk oyuncu, rakibi hata yapmadığı sürece kaybeder. Bunun nedeni, sıfır XOR değerinden yapılan her hamlenin sonucu sıfırdan farklı hâle getirmesidir. Sıfırdan farklı bir durumda ise en yüksek aktif biti hedefleyerek XOR değerini yeniden sıfıra indiren bir hamle bulunur.

## Kazandıran hamleyi üretmek

Yalnızca kazananı söylemek bazen yetmez; hamleyi de bulmamız gerekir. Toplam XOR değeri $S$ hesaplandıktan sonra her yığın için $b=a_i\oplus S$ denenir. Eğer $b<a_i$ ise ilgili yığını $b$ değerine düşürmek kazandıran hamledir.

```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<long long> pile(n);
    long long nimSum = 0;

    for (long long &x : pile) {
        cin >> x;
        nimSum ^= x; // Tüm yığınların oyun değerini birleştirir.
    }

    if (nimSum == 0) {
        cout << "Kaybeden konum\n";
        return 0;
    }

    for (int i = 0; i < n; ++i) {
        long long target = pile[i] ^ nimSum;
        if (target < pile[i]) {
            cout << i + 1 << ". yigini "
                 << target << " tas olacak sekilde azalt\n";
            break;
        }
    }
}
```

Algoritmanın zaman karmaşıklığı $O(n)$, ek alan ihtiyacı ise yığınları saklamadan uygulanırsa $O(1)$ olabilir. Üstel büyüklükteki oyun ağacına kıyasla oldukça etkileyici bir kestirmedir.

## Sprague-Grundy ile genelleme

Her oyun doğrudan Nim yığını gibi görünmez. Sprague-Grundy teoremi, sonlu ve tarafsız her alt oyuna bir Grundy sayısı atar:

$$g(x)=\operatorname{mex}\{g(y)\mid x\rightarrow y\}$$

`mex`, kümede bulunmayan en küçük negatif olmayan sayıdır. Örneğin erişilebilir değerler `{0, 1, 3}` ise mex değeri `2` olur. Bağımsız alt oyunların birleşimi, Grundy sayılarının XOR’udur:

$$G=g_1\oplus g_2\oplus\cdots\oplus g_k$$

Böylece garip taş alma kuralları, grafik üzerindeki hamleler veya birden fazla bağımsız tahta önce Grundy sayılarına çevrilir, sonra Nim gibi çözülür. Rekabetçi programlamadaki asıl beceri XOR yazmak değil, problemin bağımsız alt oyunlarını fark etmek ve doğru Grundy durumunu tasarlamaktır. Oyun ağacının gürültüsü içinde tek bir sayı konuşur: sıfırsa dikkat, sıfır değilse saldırı zamanı!
