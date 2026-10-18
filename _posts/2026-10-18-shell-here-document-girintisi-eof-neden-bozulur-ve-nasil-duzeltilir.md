---
layout: post
title: "Shell Here-Document Girintisi: EOF Neden Bozulur ve Nasıl Düzeltilir?"
math: true
categories: 
  - Bilgi
tags: 
  - shell
  - bash
  - heredoc
  - girinti
  - linux
  - betik
toc: true
image: /img/shell-here-document-73.png
---

Shell betiklerinde `<<EOF` ile oluşturulan here-document yapısı, çok satırlı metinleri bir komuta aktarmanın en rahat yollarından biridir. Ancak kodu daha okunaklı yapmak için sınırlayıcıya girinti eklediğinizde Shell aniden metnin hiç bitmediğini düşünebilir. Sorun görsel hizalama değil, kapanış sınırlayıcısının karakter karakter eşleşmek zorunda olmasıdır.
``
## Here-document nasıl çalışır?

Here-document, bir komutun standart girdisine çok satırlı içerik gönderir. Genel sözdizimi şöyledir:

```bash
cat <<EOF
Merhaba dünya
EOF
```

Shell, `<<EOF` ifadesini gördüğünde sonraki satırları okumaya başlar. Yalnızca tamamı `EOF` olan bir satırla karşılaştığında okumayı bırakır. Buradaki `EOF` özel bir anahtar kelime değildir; `SON`, `METIN` veya başka bir ad da seçilebilir.

Bunu bir eşitlik gibi düşünebiliriz. Açılışta tanımlanan sınırlayıcı $D$ olsun. Kapanışın geçerli olması için okunan satır $L$ şu koşulu sağlamalıdır:

$$L = D$$

Satırın başında boşluk varsa gerçekte $L = \text{"    EOF"}$ olur. Bu değer `EOF` ile aynı değildir. Dolayısıyla $L \neq D$ ve here-document kapanmaz.

## Girinti neden sınırlayıcıyı bozar?

Aşağıdaki kod estetik görünse de hatalıdır:

```bash
if true; then
    cat <<EOF
    Kullanıcı bulundu.
    EOF
fi
```

Kapanış satırındaki dört boşluk da verinin parçasıdır. Shell `EOF` ararken `    EOF` görür. Bash çoğunlukla dosyanın sonuna kadar okumayı sürdürür ve sınırlayıcının bulunamadığını belirten bir uyarı verir.

| Yazım | Sonuç | Neden |
|---|---|---|
| `EOF` | Çalışır | Birebir eşleşir |
| `    EOF` | Çalışmaz | Başında boşluk vardır |
| `EOF ` | Çalışmaz | Sonunda boşluk vardır |
| `\tEOF` ve `<<-EOF` | Çalışır | Baştaki sekmeler temizlenir |

## Çözüm 1: Sınırlayıcıyı satır başına taşımak

En taşınabilir çözüm, kapanış sınırlayıcısını girintisiz yazmaktır:

```bash
if true; then
    cat <<EOF
Kullanıcı bulundu.
İşlem başlatılıyor.
EOF
fi
```

Bu yaklaşım POSIX uyumludur. Dezavantajı, metnin çevresindeki kodla hizalanmamasıdır. Buna rağmen farklı Shell ortamlarında güvenilir davranması nedeniyle genellikle en güvenli seçimdir.

## Çözüm 2: `<<-EOF` ve sekme kullanmak

Tireli biçim, here-document satırlarının başındaki **sekme karakterlerini** kaldırır:

```bash
if true; then
	cat <<-EOF
	Kullanıcı bulundu.
	İşlem başlatılıyor.
	EOF
fi
```

Bu kodda girintiler gerçek tab karakteri olmalıdır. Dört boşluk, ekranda sekmeyle aynı görünebilir fakat aynı karakter değildir. Matematiksel olarak temizleme işlemini $T$ ile gösterirsek, `<<-` için karşılaştırma $T(L)=D$ biçiminde yapılır; burada $T$, yalnızca baştaki tab karakterlerini siler.

| Özellik | `<<EOF` | `<<-EOF` |
|---|---:|---:|
| Baştaki boşlukları siler | Hayır | Hayır |
| Baştaki sekmeleri siler | Hayır | Evet |
| Girintili kapanışa izin verir | Hayır | Yalnızca tab ile |
| POSIX desteği | Evet | Evet |

## Değişken genişletmesini de unutmayın

Sınırlayıcının tırnaklanması, içerikte değişkenlerin çalışıp çalışmayacağını belirler:

```bash
name="Ada"

cat <<EOF
Merhaba $name
EOF

cat <<'EOF'
Bu kez $name aynen yazılır.
EOF
```

İlk blok `Merhaba Ada` üretirken ikinci blok `$name` metnini değiştirmeden basar. Girinti problemiyle tırnaklama birbirinden ayrı konulardır: `<<-` sekmeleri yönetir, `'EOF'` ise değişken ve komut genişletmesini engeller.

## Pratik hata ayıklama

Editörünüz boşluk ve tab karakterlerini görünür yapabiliyorsa bu özelliği açın. Ayrıca sorunlu satırı incelemek için `sed -n l dosya.sh` kullanılabilir; tab karakterleri genellikle `\t` olarak görünür. Özetle kapanış sınırlayıcısını tamamen sola yaslamak en sade çözümdür. Kod hizalaması şartsa `<<-EOF` kullanın, fakat girintinin boşluk değil gerçek sekme olduğundan emin olun. Shell gözünde güzel hizalama değil, baytların birebir eşleşmesi önemlidir.

![shell-here-document-73](/img/shell-here-document-73.svg)

