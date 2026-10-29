---
layout: post
title: "Akıllı Sözleşmeler Bankacılığı Nasıl Değiştirebilir?"
math: true
categories: 
  - Bilgi
tags: 
  - akıllı sözleşmeler
  - blockchain
  - fintech
  - bankacılık
  - solidity
  - merkeziyetsiz finans
toc: true
image: /img/akilli-sozlesmeler-bankaciligi-63.png
---

Bir kredi başvurusu yaptığınızı ve banka görevlisi, mesai saati ya da birkaç günlük onay süreci beklemeden paranızın saniyeler içinde hesabınıza geçtiğini düşünün. Üstelik faiz hesabı, teminat kontrolü ve geri ödeme takibi otomatik yürütülüyor. Akıllı sözleşmeler, finans dünyasına tam olarak bu tür programlanabilir işlemler vadediyor.

``

## Akıllı sözleşme nedir?

Akıllı sözleşme, belirli koşullar gerçekleştiğinde önceden tanımlanmış işlemleri otomatik olarak yürüten blokzincir tabanlı bir programdır. Geleneksel sözleşmeler hukuki metinlerle “ne yapılacağını” söylerken akıllı sözleşmeler, uygun şartlar oluştuğunda işlemi doğrudan gerçekleştirir.

Temel mantık oldukça tanıdıktır:

> Eğer X koşulu gerçekleşirse Y işlemini yap.

Örneğin bir borçlu, ödeme tarihine kadar gerekli tutarı gönderirse sistem borcu kapatabilir ve teminatı serbest bırakabilir. İşlem kayıtları blokzincire yazıldığı için tarafların aynı veri üzerinde uzlaşması kolaylaşır.

Basit bir kredinin toplam geri ödemesi şöyle modellenebilir:

$$
G = A(1 + r \cdot t)
$$

Burada $A$ anapara, $r$ faiz oranı, $t$ süre ve $G$ toplam geri ödemedir. Akıllı sözleşme bu hesabı yalnızca göstermekle kalmaz; ödeme geldiğinde bakiyeleri kurallara göre değiştirebilir.

## Geleneksel bankacılık ile karşılaştırma

| Özellik | Geleneksel sistem | Akıllı sözleşme tabanlı sistem |
|---|---|---|
| Çalışma zamanı | Mesai ve kurum altyapısına bağlı | 7/24 çalışabilir |
| Aracı ihtiyacı | Banka, takas kurumu, noter | Bazı aracılar kodla değiştirilebilir |
| İşlem hızı | Saatler veya günler | Ağ durumuna göre saniyeler veya dakikalar |
| Şeffaflık | Kayıtlar çoğunlukla kurum içindedir | Kod ve işlemler incelenebilir |
| Hata kaynağı | İnsan ve yazılım hataları | Yazılım, veri ve tasarım hataları |
| Geri alma | Kurumsal süreçlerle mümkün olabilir | Çoğu işlem kolayca geri alınamaz |

![akilli-sozlesmeler-bankaciligi-63](/img/akilli-sozlesmeler-bankaciligi-63.svg)


Bu tablo, bankaların tamamen ortadan kalkacağı anlamına gelmez. Bankalar kimlik doğrulama, mevzuata uyum, risk değerlendirmesi ve müşteri desteği gibi görevleri sürdürürken operasyonlarının bir bölümünü akıllı sözleşmelere devredebilir.

## Kodla çalışan küçük bir emanet hesabı

Aşağıdaki Solidity örneği, alıcının parasını teslim koşulu gerçekleşene kadar sözleşmede tutar:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Emanet {
    address public alici;
    address payable public satici;
    bool public tamamlandi;

    constructor(address payable _satici) payable {
        alici = msg.sender;
        satici = _satici;
    }

    function teslimiOnayla() external {
        require(msg.sender == alici, "Yalnizca alici onaylayabilir");
        require(!tamamlandi, "Islem zaten tamamlandi");

        tamamlandi = true;
        satici.transfer(address(this).balance);
    }
}
```

Kurucu fonksiyona gönderilen para sözleşmede kilitlenir. `teslimiOnayla` çağrıldığında önce çağrıyı yapan kişinin alıcı olup olmadığı kontrol edilir; ardından bakiye satıcıya aktarılır. Böylece basit bir emanet hizmetinin temel davranışı kodlanmış olur. Gerçek kullanımda iade süresi, anlaşmazlık çözümü ve güvenlik kontrolleri de eklenmelidir.

## Finans dünyasında olası kullanım alanları

Akıllı sözleşmeler; otomatik kredi ödemeleri, sigorta tazminatları, uluslararası para transferleri, menkul kıymet takası ve dijital varlık yönetiminde kullanılabilir. Örneğin uçuş gecikme verisini güvenilir bir kaynaktan alan sigorta sözleşmesi, koşul sağlandığında müşteriye otomatik ödeme yapabilir.

Ancak blokzincir dışındaki bilgileri sisteme taşıyan **oracle** servisleri kritik bir risk oluşturur. Kod doğru olsa bile yanlış fiyat veya olay verisi, yanlış ödeme üretebilir. Ayrıca yazılım açıkları, özel anahtar kaybı, ağ ücretleri ve değişen düzenlemeler dikkatle yönetilmelidir.

## Bankasız değil, programlanabilir bankacılık

Akıllı sözleşmelerin en güçlü etkisi bankaları yok etmekten çok finansal süreçleri programlanabilir hâle getirmektir. Mutabakat ve ödeme gibi tekrarlı işlemler otomatikleşirken kurumlar denetim, güvenlik ve müşteri ilişkilerine odaklanabilir. Geleceğin bankası muhtemelen yalnızca kasalar ve hesaplardan değil; denetlenmiş kodlardan, güvenilir veri kaynaklarından ve hukuki kurallarla uyumlu dijital protokollerden oluşacaktır.
