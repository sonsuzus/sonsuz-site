---
layout: post
title: "Sıfırdan Mini Git: Blob, Tree ve Commit Nesneleriyle Kendi Depomuzu Yazmak"
math: true
categories: 
  - Proje
tags: 
  - Git
  - Python
  - Versiyon Kontrol
  - Nesne Modeli
  - Proje
---

Git'i yalnızca `git add` ve `git commit` komutlarından ibaret görmek kolaydır; fakat perde arkasında Git, dosyaları ve geçmişi içerik adreslemeli küçük nesneler olarak saklar. Bu projede Python ile basit bir Git klonu yazacak, bir dosyadan **blob**, dosya listesinden **tree** ve geçmiş kaydından **commit** üreteceğiz. Amaç Git komutlarını kopyalamak değil; Git'in neden hızlı, güvenilir ve tekrar eden içeriklerde verimli olduğunu somut olarak anlamaktır.
``
## Temel fikir: içerik adresleme

Git'te bir nesnenin kimliği, rastgele seçilmiş bir numara değildir. Nesnenin türü, boyutu ve içeriği birlikte SHA-1 özetinden geçirilir:

$$oid = SHA1(type + \" \" + size + \0 + content)$$

Aynı içerik her zaman aynı kimliği üretir. Dosyada tek karakter değişirse özet dramatik biçimde değişir; bu etkiye çığ etkisi denir. Bu yaklaşım, hem bütünlük kontrolü hem de doğal tekilleştirme sağlar: Aynı dosya içeriği ikinci kez saklanmaz.

| Nesne | Ne saklar? | Neye işaret eder? | Günlük benzetme |
|---|---|---|---|
| Blob | Dosyanın ham içeriği | Hiçbir şeye | Sayfa içeriği |
| Tree | Dosya adları ve blob/tree kimlikleri | Blob veya alt tree | Klasör indeksi |
| Commit | Tree, ebeveyn, yazar ve mesaj | Tree ve önceki commit | Tarihli klasör fotoğrafı |

Önemli ayrıntı: Blob, dosya adını bilmez. `notlar.txt` adı tree içinde yaşar. Böylece aynı içerik farklı adlarla kullanılabilir; Git'in veri modelindeki sade ama güçlü ayrım budur.

## Nesneleri disk üzerinde saklamak

Gerçek Git, nesneleri `.git/objects/aa/bb...` biçiminde saklar ve zlib ile sıkıştırır. İlk iki hex karakter klasör, kalan karakterler dosya adıdır. Aşağıdaki kod nesne başlığını üretir, SHA-1 hesaplar ve sıkıştırılmış veriyi doğru konuma yazar:

```python
from pathlib import Path
import hashlib
import zlib

OBJECTS = Path(".mini-git/objects")

def write_object(kind: str, content: bytes) -> str:
    raw = f"{kind} {len(content)}\0".encode() + content
    oid = hashlib.sha1(raw).hexdigest()
    path = OBJECTS / oid[:2] / oid[2:]

    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(zlib.compress(raw))
    return oid

def make_blob(filename: str) -> str:
    return write_object("blob", Path(filename).read_bytes())
```

`make_blob("merhaba.txt")` çağrısı dosyanın içeriğini bir blob'a dönüştürür. Aynı dosyayı yeniden işlemek aynı `oid` değerini döndürür; `if not path.exists()` satırı gereksiz yazmayı engeller.

## Tree: isimler ile içerikleri buluşturmak

Basit klonumuzda tree içeriğini satır tabanlı tutacağız. Gerçek Git, sıralanmış ikili kayıtlar kullanır; bizim metin biçimimiz öğrenme için daha görünürdür.

```python
def make_tree(entries: list[tuple[str, str]]) -> str:
    # entries: [(dosya_adi, blob_oid), ...]
    lines = [f"100644 blob {oid}\t{name}" for name, oid in sorted(entries)]
    content = ("\n".join(lines) + "\n").encode()
    return write_object("tree", content)

blob_oid = make_blob("merhaba.txt")
tree_oid = make_tree([("merhaba.txt", blob_oid)])
```

Buradaki `100644`, sıradan bir dosyanın Unix kipini temsil eder. Tree, blob kimliğini ve `merhaba.txt` adını aynı kayıtta birleştirir. Klasör desteği eklemek isterseniz, alt klasör için önce başka bir tree üretip üst tree'ye `40000 tree <oid>` olarak yerleştirmeniz gerekir.

## Commit: bir anlık görüntüye anlam katmak

Commit, doğrudan dosyaları değil tree'yi referans alır. Önceki commit kimliği de eklenirse tarihçe zinciri oluşur. Zincirin her halkası öncekinin özetini taşıdığı için eski bir kaydı değiştirmek sonraki tüm kimlikleri etkiler.

```python
from datetime import datetime, timezone

def make_commit(tree_oid: str, message: str, parent: str | None = None) -> str:
    who = "Mini Git <mini@example.com>"
    now = int(datetime.now(timezone.utc).timestamp())
    header = [f"tree {tree_oid}"]
    if parent:
        header.append(f"parent {parent}")
    header += [f"author {who} {now} +0000", f"committer {who} {now} +0000"]
    content = ("\n".join(header) + f"\n\n{message}\n").encode()
    return write_object("commit", content)

commit_oid = make_commit(tree_oid, "İlk mini commit")
print(commit_oid)
```

Bu noktada elinizde gerçek Git'in temel düşüncesini taşıyan, değişmez nesne deposu vardır. Sonraki adım olarak bir `HEAD` dosyası, branch referansları ve nesne okuma komutu ekleyebilirsiniz. Böylece Git geçmişinin aslında dosya kopyaları değil, birbirine bağlı içerik özetleri olduğunu uygulayarak keşfedersiniz.
