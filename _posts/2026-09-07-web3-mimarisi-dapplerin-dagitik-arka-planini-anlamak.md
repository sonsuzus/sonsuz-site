---
layout: post
title: "Web3 Mimarisi: DApp’lerin Dağıtık Arka Planını Anlamak"
math: true
categories: 
  - Bilgi
tags: 
  - web3
  - dapp
  - akıllı sözleşmeler
toc: true
---

Bir DApp ilk bakışta React, Vue veya sade JavaScript ile hazırlanmış sıradan bir web uygulamasına benzeyebilir. Ancak kullanıcı “Gönder” düğmesine bastığında istek merkezi bir API sunucusuna değil, cüzdan tarafından imzalanarak dağıtık bir ağa gider. Veritabanı rolünü blokzincir, iş kurallarını ise akıllı sözleşmeler üstlenir. Kısacası görünen yüz tanıdık, motor bölümü oldukça farklıdır.

``

## Geleneksel uygulamadan DApp’e geçiş

Klasik üç katmanlı mimaride önyüz bir REST veya GraphQL API ile konuşur. API; kimlik doğrulama, iş mantığı ve veritabanı işlemlerini yönetir. Web3 mimarisinde bu sorumlulukların bir bölümü akıllı sözleşmelere ve kullanıcı cüzdanına taşınır.

| Katman | Geleneksel Web | Web3 DApp |
|---|---|---|
| Kimlik | Kullanıcı adı, parola, oturum | Açık adres ve dijital imza |
| İş mantığı | Sunucu uygulaması | Akıllı sözleşme |
| Veri | SQL veya NoSQL | Blokzincir durumu, IPFS |
| Yetkilendirme | Sunucudaki roller | Sözleşme koşulları |
| İşlem maliyeti | İşletme karşılar | Genellikle kullanıcı gas öder |
| Değiştirilebilirlik | Hızlı dağıtım yapılabilir | Sözleşme çoğunlukla kalıcıdır |

Bu değişim, “arka plan tamamen ortadan kalktı” anlamına gelmez. RPC sağlayıcıları, indeksleyiciler, oracle servisleri ve merkezi olmayan depolama ağları hâlâ mimarinin önemli parçalarıdır.

## Akıllı sözleşme nasıl arka plan olur?

Akıllı sözleşme, ağdaki düğümlerin aynı sonucu üretmek üzere çalıştırdığı deterministik bir programdır. Solidity ile yazılan kod EVM bayt koduna derlenir ve Ethereum benzeri ağlara dağıtılır. Her düğüm sözleşmenin durumunu doğruladığı için tek bir yöneticinin kayıtları gizlice değiştirmesi zorlaşır.

İşlem maliyeti kabaca şu şekilde hesaplanır:

$$IslemMaliyeti = KullanilanGas × GasFiyati$$

Dolayısıyla zincire uzun metinler kaydetmek pahalıdır. Yaygın yaklaşım; kritik sahiplik ve izin verilerini zincirde, görsel veya belge gibi büyük içerikleri IPFS üzerinde tutmaktır. Sözleşmede yalnızca içeriğin hash değeri saklanabilir.

Aşağıdaki sözleşme, zincir üzerinde basit bir mesaj yönetir:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract MesajKutusu {
    string public mesaj;
    address public sahip;

    event MesajDegisti(string yeniMesaj);

    constructor(string memory ilkMesaj) {
        sahip = msg.sender;
        mesaj = ilkMesaj;
    }

    function mesajGuncelle(string calldata yeniMesaj) external {
        require(msg.sender == sahip, "Yetkiniz yok");
        mesaj = yeniMesaj;
        emit MesajDegisti(yeniMesaj);
    }
}
```

Burada `require` yetkilendirme yapar, `public` değişken otomatik okuma fonksiyonu sağlar ve event, zincir dışı uygulamaların değişiklikleri izlemesini kolaylaştırır.

## Geleneksel önyüz nasıl bağlanır?

React veya Vue çöpe gitmez; yalnızca veri kaynağı değişir. Önyüz, cüzdanın sağladığı provider üzerinden RPC düğümüne bağlanır. Sözleşmeyle iletişim kurabilmek için sözleşme adresi ve ABI gerekir. ABI, JavaScript ile bayt kodu arasında bir tür çevirmen görevi görür.

```javascript
import { BrowserProvider, Contract } from "ethers";
import abi from "./MesajKutusuABI.json";

const adres = "0xSOZLESME_ADRESI";

export async function mesajGuncelle(yeniMesaj) {
  if (!window.ethereum) throw new Error("Cüzdan bulunamadı");

  const provider = new BrowserProvider(window.ethereum);
  await provider.send("eth_requestAccounts", []);
  const signer = await provider.getSigner();
  const sozlesme = new Contract(adres, abi, signer);

  const islem = await sozlesme.mesajGuncelle(yeniMesaj);
  await islem.wait();
  return islem.hash;
}
```

`signer`, kullanıcının işlemi cüzdanında onaylamasını sağlar. Okuma işlemleri ücretsiz RPC çağrıları olabilirken durum değiştiren işlemler imza, ağ onayı ve gas gerektirir. Bu yüzden arayüzde “cüzdan onayı bekleniyor”, “işlem gönderildi” ve “blok onayı alındı” aşamaları ayrı gösterilmelidir.

## Görünmeyen yardımcı katmanlar

Blokzinciri her ekran açılışında baştan taramak verimsizdir. The Graph benzeri indeksleyiciler event verilerini sorgulanabilir hâle getirir. Oracle’lar döviz kuru veya hava durumu gibi zincir dışı bilgileri sözleşmelere ulaştırır. IPFS büyük dosyaları dağıtık biçimde saklar. RPC servisleri ise önyüz ile ağ arasında geçit oluşturur.

DApp geliştirirken özel anahtarları asla önyüze gömmemek, sözleşmeleri test etmek, yeniden giriş saldırılarına karşı önlem almak ve yanlış ağ seçimini kontrol etmek gerekir. Web3, sunucusuz bir sihir numarası değil; güvenin tek merkezden protokole dağıtıldığı farklı bir mühendislik modelidir.
