---
layout: post
title: "Qiskit ile Grover Algoritması: Klasik Aramaya Kuantum Hızı Katmak"
math: true
categories: 
  - Bilgi
tags: 
  - kuantum hesaplama
  - qiskit
  - grover algoritması
  - python
---

Bir telefon rehberinde adı bilinmeyen tek bir kişiyi bulduğunuzu düşünün: klasik bilgisayar kayıtları sırayla kontrol ederken, kuantum bilgisayar olasılıkları akıllıca yükselterek hedefe yönelmeyi amaçlar. Grover arama algoritması bu fikrin en ünlü örneklerinden biridir. Qiskit simülatörüyle algoritmayı çalıştırmak, kuantum donanımına erişmeden süperpozisyon, girişim ve ölçüm kavramlarını somut biçimde gözlemlemenin eğlenceli yoludur.
``

## Arama probleminin matematiği

Elimizde $N = 2^n$ olası kayıt ve bunlardan yalnızca bir hedef kayıt olduğunu varsayalım. Klasik, sıralı ve rastgele olmayan aramada en kötü durumda $N$ sorgu; ortalama durumda yaklaşık $N/2$ sorgu gerekir. Grover algoritması ise hedefi yaklaşık

$$
R \approx \left\lfloor \frac{\pi}{4}\sqrt{N} \right\rfloor
$$

oracle çağrısında bulmayı hedefler. Bu, üstel değil, **kuadratik hızlanma**dır. Yani $N$ iki katına çıktığında gereken kuantum iterasyonları kabaca $\sqrt{2}$ kat artar. Buna rağmen özellikle çok büyük, yapılandırılmamış arama uzaylarında önemli bir teorik fark yaratır.

| Özellik | Klasik doğrusal arama | Grover araması |
|---|---:|---:|
| Arama uzayı | $N$ aday | $N=2^n$ aday |
| Sorgu karmaşıklığı | $O(N)$ | $O(\sqrt{N})$ |
| Hedefi kesin bulma | Tüm kayıtlar denenirse | Uygun iterasyon sayısıyla yüksek olasılık |
| Temel mekanizma | Tek tek karşılaştırma | Süperpozisyon ve girişim |

Buradaki kritik ayrıntı, Grover'ın “her cevabı aynı anda okuması” değildir. Kuantum durumları ölçülmeden önce olasılık genlikleriyle temsil edilir. Algoritma, hedef durumun genliğini yapıcı girişimle artırır; hedef olmayanlarınkini ise göreli olarak azaltır. Ölçüm sonunda yüksek genlikli durum daha sık gözlenir.

## Oracle ve difüzör: algoritmanın iki motoru

İlk olarak $n$ kübit Hadamard kapılarıyla eşit süperpozisyona alınır. Böylece her adayın başlangıç genliği $1/\sqrt{N}$ olur. Ardından iki işlem döngü halinde uygulanır:

1. **Oracle**, hedef bit dizisinin fazını $-1$ ile çevirir.
2. **Difüzör**, genlikleri ortalama etrafında ters çevirerek işaretlenmiş hedefi güçlendirir.

Bu süreç iki boyutlu bir geometrik dönüş gibi düşünülebilir. Başarı olasılığı yaklaşık olarak

$$
P(R)=\sin^2\big((2R+1)\theta\big), \qquad \sin(\theta)=\frac{1}{\sqrt{N}}
$$

şeklindedir. İlginç biçimde iterasyonu gereğinden fazla sürdürmek başarıyı düşürebilir: dönüş hedefi geçip gider. Kuantumda “daha fazla tur” her zaman “daha iyi sonuç” demek değildir.

## Qiskit simülatöründe dört adaylı deney

Aşağıdaki örnekte hedefimiz `11` durumudur. İki kübit için $N=4$ olduğundan ideal iterasyon sayısı yaklaşık bir turdur. Oracle, `11` durumuna kontrollü-Z uygulayarak faz işaretlemesi yapar; difüzör de amplitüd yükseltmesini tamamlar.

```python
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

qc = QuantumCircuit(2, 2)
qc.h([0, 1])                 # 00, 01, 10, 11 süperpozisyonu

qc.cz(0, 1)                  # Oracle: |11> fazını ters çevirir
qc.h([0, 1])
qc.x([0, 1])
qc.cz(0, 1)                  # Difüzörün kontrollü faz kısmı
qc.x([0, 1])
qc.h([0, 1])

qc.measure([0, 1], [0, 1])

simulator = AerSimulator()
result = simulator.run(transpile(qc, simulator), shots=1024).result()
print(result.get_counts())
```

Çıktıda `11` sayımının baskın olması beklenir. Bit sıralamasının Qiskit ekranında bazen ters görünebildiğini unutmayın: ölçüm kübitleri ve klasik bit eşlemesini özellikle kontrol edin.

## Simülatörden gerçek dünyaya

Bu deney, hızlanma fikrini göstermek için mükemmeldir; ancak küçük örneklerde klasik bilgisayar doğal olarak daha hızlı çalışır. Simülatör, kuantum devresini klasik donanımda taklit ettiği için gerçek kuantum avantajı üretmez. Ayrıca gerçek cihazlarda gürültü, kapı hataları ve bağlantı kısıtları başarı oranını etkiler. Yine de Qiskit ile oracle tasarlamak, iterasyon sayısını değiştirmek ve histogramları karşılaştırmak; Grover'ın vaat ettiği $O(\sqrt{N})$ potansiyelini anlamanın en sağlam ilk adımıdır.
