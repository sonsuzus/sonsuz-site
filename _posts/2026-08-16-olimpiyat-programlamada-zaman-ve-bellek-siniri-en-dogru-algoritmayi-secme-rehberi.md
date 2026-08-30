---
layout: post
title: "Olimpiyat Programlamada Zaman ve Bellek Sınırı: En Doğru Algoritmayı Seçme Rehberi"
math: true
categories: 
  - Bilgi
tags: 
  - olimpiyat programlama
  - algoritma
  - karmaşıklık
  - dinamik programlama
  - optimizasyon
image: /img/olimpiyat-programlamada-zaman-93.png
---

Olimpiyat programlamada bir çözümün doğru cevap üretmesi yalnızca ilk adımdır; asıl soru, bunu verilen süre ve bellek içinde yapıp yapamayacağıdır. Aynı problemi kaba kuvvet, dinamik programlama, açgözlü yaklaşım veya gelişmiş veri yapılarıyla çözmek mümkün olabilir. Fakat yarışmada kazanan çözüm, test verisinin ölçeğine uygun karmaşıklık sınıfını seçen çözümdür. Bu nedenle kod yazmadan önce sınırları okumak, algoritma seçiminin pusulasıdır.
``

Bir algoritmanın çalışma süresi çoğunlukla girdi boyutu $n$ üzerinden ifade edilir. Örneğin iki iç içe döngü genellikle $O(n^2)$, sıralama ise $O(n \log n)$ maliyet taşır. Buradaki büyük-O gösterimi sabit katsayıları ve küçük terimleri gizler; ancak hangi yaklaşımın büyüyen veride ayakta kalacağını harika biçimde anlatır. Yaklaşık işlem sayısını düşünmek için $10^8$ işlemin çoğu ortamda 1-2 saniye civarında kritik bir eşik olabilir. Bu kesin bir yasa değildir: dil, donanım ve işlem türü sonucu değiştirir. Yine de güçlü bir yarışma sezgisidir.

| Girdi sınırı | Genellikle hedeflenebilecek karmaşıklık | Tipik yaklaşım |
|---:|---|---|
| $n \leq 20$ | $O(2^n \cdot n)$ | Bitmask, altküme DP |
| $n \leq 500$ | $O(n^3)$ | Floyd-Warshall, aralıklı DP |
| $n \leq 10^5$ | $O(n \log n)$ | Sıralama, heap, segment tree |
| $n \leq 10^6$ | $O(n)$ | Prefix sum, iki işaretçi |
| $n \geq 10^7$ | $O(n)$ ve düşük sabit | Akış tabanlı, dikkatli I/O |

Mesela bir dizide toplamı hedef değeri geçen en kısa alt diziyi bulma problemi düşünelim. Negatif sayı yoksa ilk fikir tüm başlangıç ve bitiş çiftlerini denemektir. Prefix sum ile her aralığın toplamı $O(1)$ hesaplanabilir, ama çift sayısı yaklaşık $n(n+1)/2$ olduğundan toplam maliyet yine $O(n^2)$ olur. $n=10^5$ için bu, yaklaşık $10^{10}$ kontrol demektir: süre sınırına adeta roketle çarpar.

Aynı problemde pozitiflik özelliği önemli bir ipucudur. Pencereye yeni eleman eklemek toplamı artırır; soldan eleman çıkarmak azaltır. Böylece iki işaretçi kullanılır. Her eleman en fazla bir kez pencereye girip bir kez çıkar, yani hareket sayısı en fazla $2n$ olur. Karmaşıklık $O(n)$'dir. Buradaki ders şudur: Optimizasyon çoğu zaman daha karmaşık kod yazmak değil, problemin matematiksel özelliğini kullanmaktır.

```cpp
int minLengthAtLeastK(const vector<int>& a, long long k) {
    long long sum = 0;
    int left = 0, answer = INT_MAX;

    for (int right = 0; right < (int)a.size(); ++right) {
        sum += a[right];
        while (sum >= k) {
            answer = min(answer, right - left + 1);
            sum -= a[left++];
        }
    }
    return answer == INT_MAX ? -1 : answer;
}
```

Bu kodun kritik noktası `while` döngüsüdür. İlk bakışta iç içe döngü gibi görünse de `left` geri gitmez. Dolayısıyla toplamda $O(n)$ çalışır. Ancak dizi negatif değerler içerirse pencere toplamı artık monoton davranmaz; bu teknik geçersiz olabilir. Algoritma seçimi, yalnızca hız değil, varsayımların doğruluğudur.

Bellek sınırı da ikinci hakemdir. Örneğin $n=10^6$ için `long long dp[n][n]` tasarlamak yalnızca yavaş değil, astronomik derecede büyüktür. Bir `long long` 8 bayt ise teorik bellek ihtiyacı $8n^2$ bayttır. Buna karşılık bazı DP geçişleri yalnızca önceki satıra bağlıdır; iki satır saklayarak belleği $O(n^2)$ yerine $O(n)$ yapabilirsiniz.

| Yaklaşım | Zaman | Bellek | Ne zaman seçilmeli? |
|---|---:|---:|---|
| Kaba kuvvet | $O(n^2)$ | $O(1)$ | Çok küçük sınırlar |
| Prefix sum + tüm aralıklar | $O(n^2)$ | $O(n)$ | Sorgu yapısı uygunsa ama $n$ küçükse |
| İki işaretçi | $O(n)$ | $O(1)$ | Monotonluk/pozitiflik varsa |
| DP sıkıştırma | Probleme bağlı | $O(n)$ | Önceki katman yeterliyse |

Yarışma anında şu sırayı izleyin: Önce kısıtlardan izin verilen karmaşıklığı tahmin edin, sonra problemin özel yapısını—sıralılık, monotonluk, küçük değer aralığı veya tekrar eden alt problemler—arayın. En sonunda en kötü durumu hesaplayın. “Örnek test geçti” rahatlatıcıdır; fakat $O(n^2)$ bir kodun $n=200000$ üzerindeki kaderini değiştirmez. Doğru karmaşıklık, olimpiyat programlamanın görünmez ama en güçlü veri yapısıdır.

![olimpiyat-programlamada-zaman-93](/img/olimpiyat-programlamada-zaman-93.svg)

