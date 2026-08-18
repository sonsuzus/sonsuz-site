---
layout: post
title: "Solidity Akıllı Sözleşmelerinde Reentrancy ve Overflow Tuzaklarını Kapatmak"
math: true
categories: 
  - Bilgi
tags: 
  - Blockchain
  - Solidity
  - Akıllı Sözleşme Güvenliği
---

Akıllı sözleşmeler dağıtıldıktan sonra çoğunlukla değiştirilemez; bu nedenle küçük görünen bir kod hatası, kasadaki tüm varlıkların saniyeler içinde boşalmasına dönüşebilir. Solidity güvenliği yalnızca doğru sözdizimi yazmak değildir: EVM’nin çağrı akışını, durum değişikliklerini ve sayısal sınırları anlamayı gerektirir. İki klasik tehdit olan **reentrancy** ve **overflow**, güvenli tasarım alışkanlıklarıyla büyük ölçüde önlenebilir.
``

## Teorik zemin: EVM’de kontrol kimde?

Bir sözleşme başka bir adrese ETH ya da token gönderirken harici kodu tetikleyebilir. Çağrılan adres bir cüzdan değil de sözleşmeyse, onun `receive`, `fallback` veya ilgili fonksiyonu çalışır. Kritik nokta şudur: İlk fonksiyonunuz henüz tamamlanmadan karşı taraf size yeniden çağrı yapabilir. Bu, reentrancy’nin kalbidir.

Sayısal taşmada ise bir `uint8` değişkeninin aralığını düşünün:

$$0 \leq x \leq 2^8 - 1 = 255$$

Eski Solidity sürümlerinde `255 + 1`, hata vermek yerine `0` değerine sarılabilirdi. Bu davranış, bakiye veya limit kontrollerini anlamsızlaştırabilirdi.

| Açık | Temel neden | Tipik sonuç | Ana savunma |
|---|---|---|---|
| Reentrancy | Harici çağrıdan önce durum güncellenmesi | Tek bakiyenin tekrar tekrar çekilmesi | Checks-Effects-Interactions |
| Overflow/Underflow | Sınır dışı aritmetik | Limit atlama, yanlış bakiye | Solidity 0.8+, kontrollü `unchecked` |

## Reentrancy: Önce defteri düzelt, sonra parayı gönder

Güvensiz bir çekim fonksiyonu önce ETH gönderip sonra bakiyeyi azaltırsa saldırganın fallback fonksiyonu tekrar `withdraw` çağırabilir. Her turda eski bakiye hâlâ görünür. Güvenli sıra **Kontroller → Durum etkileri → Harici etkileşimler** olmalıdır; buna CEI deseni denir.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

contract SafeVault is ReentrancyGuard {
    mapping(address => uint256) public balances;

    function deposit() external payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint256 amount) external nonReentrant {
        require(amount > 0 && balances[msg.sender] >= amount, "Yetersiz bakiye");

        // Effects: Harici çağrıdan once muhasebeyi güncelle.
        balances[msg.sender] -= amount;

        // Interactions: Sonra transferi yap.
        (bool ok, ) = payable(msg.sender).call{value: amount}("");
        require(ok, "Transfer basarisiz");
    }
}
```

Burada `nonReentrant`, aynı korumalı fonksiyona iç içe girişi engelleyen ek bir kilittir. Ancak onu sihirli değnek saymayın: Durumu erken güncellemek hâlâ temel savunmadır. Ayrıca token transferleri, callback içeren standartlar ve çapraz fonksiyon çağrıları da reentrancy yüzeyi oluşturabilir.

## Overflow: Derleyici korumasını doğru okumak

Solidity `0.8.0` ve sonrası, varsayılan olarak taşma ve eksik taşma işlemlerinde işlemi geri alır. Dolayısıyla çoğu senaryoda `SafeMath` eklemek zorunlu değildir. Yine de gaz optimizasyonu için kullanılan `unchecked` bloğu bu korumayı bilinçli biçimde kapatır:

```solidity
uint256 index = 0;

for (uint256 i = 0; i < users.length; ) {
    // Liste uzunluğu uint256 sinirina ulasamayacagi varsayimiyla kullanilir.
    process(users[i]);
    unchecked { ++i; }
}
```

Bu kullanım ancak taşmanın mantıksal olarak imkânsız olduğu kanıtlanabiliyorsa güvenlidir. Bakiye, fiyat, faiz veya pay hesaplarında `unchecked` kullanmak; kilit açıkken “kimse girmez” demeye benzer.

## Yayına çıkmadan önce kontrol listesi

- Harici çağrılardan önce tüm kritik durumları güncelleyin.
- OpenZeppelin’in `ReentrancyGuard` ve test edilmiş erişim kontrol bileşenlerini tercih edin.
- Solidity sürümünü sabitleyin; örneğin `pragma solidity 0.8.20;`.
- Birim testlerinde kötü niyetli alıcı sözleşmesi yazıp yeniden giriş denemesi yapın.
- Slither gibi statik analiz araçlarıyla tarama, ardından bağımsız denetim gerçekleştirin.

Güvenli sözleşme geliştirme, tek bir kütüphane eklemekten çok bir düşünme disiplinidir. Her harici çağrıda kontrolün el değiştirdiğini, her aritmetik işlemde sınırların bulunduğunu varsayın; zincirdeki en pahalı hatalar genellikle bu iki gerçeğin unutulmasından doğar.
