---
layout: post
title: "Deterministik Lockstep: RTS Ordularını Aynı Ritme Sokmak"
math: true
categories: 
  - Bilgi
tags: 
  - oyun geliştirme
  - ağ programlama
  - deterministik lockstep
  - rts
  - senkronizasyon
  - simülasyon
toc: true
image: /img/deterministik-lockstep-rts-47.png
---

Ekranda bin asker yürürken her askerin konumunu sürekli diğer oyunculara göndermek, ağı dijital bir trafik sıkışıklığına çevirebilir. Gerçek zamanlı strateji oyunlarının klasik çözümü daha zariftir: Dünyayı değil, oyuncuların verdiği emirleri paylaşmak. Deterministik lockstep yaklaşımında herkes aynı tarifle aynı yemeği pişirir; tek şart, kimsenin gizlice fazladan tuz atmamasıdır.

``

## Temel fikir: Aynı başlangıç, aynı sonuç

Her istemci, oyun dünyasının tamamını yerel olarak simüle eder. Ağ üzerinden genellikle “birlikleri şu noktaya gönder” veya “kışla inşa et” gibi komutlar taşınır. Başlangıç durumu ve işlenen komutlar aynıysa, simülasyonun her bilgisayarda aynı sonucu üretmesi beklenir.

Bunu şu bağıntıyla düşünebiliriz:

$$S_{k+1}=F(S_k,C_k)$$

Burada $S_k$ dünya durumu, $C_k$ ilgili simülasyon adımının sıralanmış komutları, $F$ ise deterministik güncelleme fonksiyonudur. Lockstep, istemcilerin aynı adım için gereken komutlar tamamlanmadan ilerlememesini sağlar. Determinizm ise ilerlediklerinde aynı yere ulaşmalarını sağlar. Bu iki kavram birbirinin yerine geçmez.

| Yaklaşım | Ağda taşınan | Temel bedel |
|---|---|---|
| Durum senkronizasyonu | Konumlar ve durum güncellemeleri | Daha fazla bant genişliği |
| Deterministik lockstep | Oyuncu komutları | Determinizm ve bekleme yönetimi |

## Determinizm neden zor?

“Aynı kod çalışıyor, sonuç da aynıdır” düşüncesi burada tehlikelidir. Kayan noktalı hesaplamalar; işlemci, derleyici optimizasyonu veya matematik kütüphanesine göre farklılaşabilir. Küçük bir sapma, yüzlerce adım sonra iki istemcide farklı savaş sonuçları doğurabilir.

Bu yüzden kritik hesaplarda tam sayı veya sabit noktalı aritmetik tercih edilebilir. Sabit noktalı temsil, örneğin bir metreyi 1000 birim olarak saklar. Ancak taşma ve yuvarlama kuralları da tutarlı olmalıdır; yalnızca veri tipini değiştirmek sihirli çözüm değildir.

Rastgelelik de yasak değildir: Aynı algoritma, başlangıç tohumu ve çağrı sırası kullanılmalıdır. Koleksiyon dolaşım sırası, yol bulmadaki eşitlik kararları ve paralel işlerin tamamlanma sırası da sabitlenmelidir. Simülasyona duvar saati, değişken kare süresi veya yerel görsel efektlerden karar taşımayın.

## İnternet bekler, simülasyon sayar

Simülasyon sabit zaman adımlarıyla ilerler: $t_k=k\Delta t$. Ekran çizimi daha hızlı olabilir; aradaki görüntüler enterpolasyonla yumuşatılabilir. Böylece 30 simülasyon adımıyla çalışan bir oyun, 144 Hz ekranda akıcı görünebilir.

Oyuncunun emri çoğunlukla mevcut adıma değil, birkaç adım sonrasına atanır. Bu giriş gecikmesi, paketlerin ulaşması için zaman kazandırır. Tamamlanan her oyuncu paketi, emir yoksa bile boş bir komut listesi içermelidir. Aksi halde “oyuncu hiçbir şey yapmadı” ile “paket henüz gelmedi” ayırt edilemez.

| Tampon | Avantaj | Dezavantaj |
|---|---|---|
| Küçük | Daha hızlı komut tepkisi | Ağ dalgalanmasında daha çok bekleme |
| Büyük | Daha kararlı ilerleme | Daha belirgin giriş gecikmesi |

Paket kaybında yeniden gönderim gerekir. Komutlar adım ve oyuncu kimliğiyle eşleştirilmeli, tekrar gelenler ayıklanmalıdır. Geç kalan oyuncuyu sonsuza kadar beklemek yerine zaman aşımı ve bağlantı koparma politikası da tasarlanmalıdır.

## Küçük bir lockstep çekirdeği

Aşağıdaki Python örneği, ağ katmanının doğrulanmış ve eksiksiz oyuncu paketlerini `inbox[adım][oyuncu]` yapısına koyduğunu varsayar:

```python
def step_tick(state, tick, inbox, players, advance_fixed):
    bundles = inbox.get(tick, {})
    if set(bundles) != set(players):
        return False

    for player in sorted(players):
        commands = sorted(
            bundles[player], key=lambda command: command['seq']
        )
        for command in commands:
            if command['kind'] == 'move':
                unit = state['units'][command['unit']]
                unit['target'] = (command['x'], command['y'])

    advance_fixed(state)
    del inbox[tick]
    return True
```

Fonksiyon eksik paket varsa durur; aksi halde komutları ortak sırayla uygular ve dünyayı bir adım ilerletir. Çağıran döngü, yalnızca `True` sonucunda adım sayacını artırmalıdır. `advance_fixed` hareketi, çatışmayı ve kaynak üretimini deterministik biçimde yürütür. Gerçek uygulamada birim sahipliği, hedef geçerliliği ve sıra numarası benzersizliği ayrıca denetlenmelidir.

## Senkron kaymasını yakalamak

Belirli aralıklarla dünya durumunun özeti karşılaştırılabilir. Ancak bellekteki ham nesneleri veya Python'ın yerleşik `hash()` sonucunu kullanmak güvenilir değildir. Birimleri kimliklerine göre sıralayıp alanları tanımlı bir biçimde serileştirerek kararlı bir özet üretin.

Özetler farklıysa bir desync vardır. İlk ayrışan adımı bulmak için başlangıç durumunu, komut günlüğünü ve ara özetleri saklamak çok değerlidir. Kurtarma gerekiyorsa güvenilir bir referans durumdan yeniden yükleme düşünülebilir; özet karşılaştırması tek başına hatayı düzeltmez.

Lockstep'in ödülü, binlerce birimin sürekli durum aktarımı olmadan birlikte çalışabilmesidir. Bedeli ise titiz mühendisliktir. Kısacası ağdan orduyu taşımayın; emirleri taşıyın ve bütün generallerin aynı kurallarla düşündüğünden emin olun.

![deterministik-lockstep-rts-47](/img/deterministik-lockstep-rts-47.svg)

