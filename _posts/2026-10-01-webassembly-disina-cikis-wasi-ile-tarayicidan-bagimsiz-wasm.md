---
layout: post
title: "WebAssembly Dışına Çıkış: WASI ile Tarayıcıdan Bağımsız Wasm"
math: true
categories: 
  - Bilgi
tags: 
  - webassembly
  - wasi
  - rust
  - wasmtime
  - sistem-programlama
  - güvenlik
toc: true
image: /img/webassembly-disina-cikis-98.png
---

WebAssembly denildiğinde çoğumuzun aklına tarayıcıda çalışan hızlı uygulamalar gelir. Oysa Wasm, taşınabilir bir ikili kod biçimidir; JavaScript’e veya tarayıcıya mahkûm değildir. Eksik parça, modülün dosya sistemi, saat, rastgele sayı üreticisi ve ağ gibi işletim sistemi kaynaklarıyla nasıl konuşacağını tanımlayan standart bir arayüzdür. İşte WASI, yani WebAssembly System Interface, bu boşluğu güvenli ve taşınabilir biçimde doldurur.


![webassembly-disina-cikis-98](/img/webassembly-disina-cikis-98.svg)

``

## Wasm neden tek başına yeterli değil?

Bir Wasm modülü, izole edilmiş doğrusal belleği ve sınırlı komut kümesi olan küçük bir sanal makinede çalışır. Bu makine işlem yapabilir fakat kendi başına `open`, `read` veya `connect` gibi sistem çağrılarını gerçekleştiremez. İşletim sistemleri de farklı API’ler sunduğundan doğrudan POSIX çağrısı kullanmak taşınabilirliği bozar.

WASI, modül ile çalışma zamanı arasına standartlaştırılmış bir sözleşme yerleştirir:

$$
\text{Wasm Modülü} \rightarrow \text{WASI Arayüzü} \rightarrow \text{Runtime} \rightarrow \text{İşletim Sistemi}
$$

Buradaki runtime; Wasmtime, Wasmer veya WASI destekleyen başka bir yürütücü olabilir. Modül işletim sistemine doğrudan ulaşmaz, yalnızca runtime tarafından kendisine verilen yetkileri kullanır.

| Özellik | Tarayıcı Wasm | WASI Wasm | Yerel program |
|---|---|---|---|
| Çalışma ortamı | Web sayfası | Sunucu, CLI, edge | Belirli işletim sistemi |
| Dosya erişimi | Web API’leriyle dolaylı | Yetki verilen dizinlerle | Kullanıcı izinleri kapsamında |
| Ağ erişimi | `fetch` gibi API’ler | Runtime ve WASI sürümüne bağlı | İşletim sistemi soketleri |
| Taşınabilirlik | Yüksek | Yüksek | Derleme hedefine bağlı |
| İzolasyon | Tarayıcı sandbox’ı | Capability tabanlı sandbox | Süreç ve OS mekanizmaları |

## Capability tabanlı güvenlik

WASI’nin en önemli fikri “önce yetki ver, sonra kullan” yaklaşımıdır. Bir modül, bilgisayarın tüm dosya sistemini göremez. Runtime başlatılırken yalnızca belirli bir dizin modüle açılabilir. Yetki kümesini $C$, programın erişmeye çalıştığı kaynakları $R$ ile gösterirsek izin koşulu şöyledir:

$$
R \subseteq C
$$

Program `/etc` dizisini okumak istiyor fakat yalnızca `./data` dizinine erişim verilmişse çağrı reddedilir. Böylece güvenilmeyen eklentiler veya üçüncü taraf araçlar, ayrı bir konteyner olmadan daha dar yetkilerle çalıştırılabilir.

## Rust ile küçük bir WASI programı

Aşağıdaki program bir dosya oluşturur ve içine metin yazar:

```rust
use std::fs;

fn main() -> std::io::Result<()> {
    fs::write("hello.txt", "WASI dış dünyaya merhaba diyor!\n")?;
    println!("Dosya başarıyla oluşturuldu.");
    Ok(())
}
```

Rust hedefini kurup programı derleyebiliriz:

```bash
rustup target add wasm32-wasip1
rustc main.rs --target wasm32-wasip1 -O -o app.wasm
```

`wasm32-wasip1`, yaygın WASI Preview 1 ABI’sini hedefler. Üretilen `app.wasm` dosyası doğrudan Linux veya Windows çalıştırılabilir dosyası değildir; WASI uyumlu bir runtime gerekir:

```bash
wasmtime run --dir=. app.wasm
```

`--dir=.` seçeneği mevcut dizini modüle açar. Bu seçenek kaldırılırsa programın dosya yazma girişimi başarısız olur. Yani güvenlik yalnızca teoride değil, komut satırında açıkça görülebilir.

## Preview 1, Preview 2 ve bileşenler

Preview 1 daha çok POSIX benzeri dosya tanıtıcılarına ve çekirdek sistem işlevlerine odaklanır. WASI Preview 2 ise Component Model ile birlikte daha yüksek seviyeli, dil bağımsız arayüzler sunar. WIT adı verilen arayüz tanımlama dili sayesinde bir Rust bileşeni, uygun bağlayıcılar üzerinden Go veya JavaScript bileşeniyle konuşabilir.

| Yaklaşım | Temel model | Uygun kullanım |
|---|---|---|
| Preview 1 | Düşük seviyeli ABI | CLI araçları ve mevcut uygulamalar |
| Preview 2 | Component Model ve WIT | Birleştirilebilir servisler ve eklentiler |

Ağ desteği ise runtime’a ve uygulanan WASI tekliflerine göre değişebilir. Bu nedenle “WASI varsa tüm soketler hazırdır” varsayımı yapılmamalı; hedef runtime’ın HTTP ve socket desteği ayrıca kontrol edilmelidir.

## Nerelerde kullanılır?

WASI; güvenli eklenti sistemleri, edge fonksiyonları, taşınabilir komut satırı araçları ve çok kiracılı sunucu uygulamaları için güçlü bir adaydır. Docker’ın birebir yerine geçmez; fakat küçük başlangıç süresi, kontrollü yetkiler ve platform bağımsız dağıtım sağladığı için bazı iş yüklerinde oldukça hafif bir alternatif oluşturur. Kısacası Wasm hesaplama motoruysa, WASI onun dış dünyaya açılan kontrollü kapısıdır.
