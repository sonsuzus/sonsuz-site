---
layout: post
title: "Python Type Hint’leri Emniyet Kemeri Değil, Yol Tabelasıdır"
math: true
categories: 
  - Bilgi
tags: 
  - python
  - type-hints
  - typing
  - mypy
  - statik-analiz
  - yazılım-güvenliği
toc: true
image: /img/python-type-hintleri-81.png
---

Python’da bir fonksiyonun parametresine `str`, dönüş değerine `int` yazınca kodumuzun artık yanlış türlere karşı korunduğunu düşünebiliriz. Ne yazık ki bu, kapıya “Girilmez” tabelası asıp fiziksel olarak kilitlediğimizi sanmaya benzer. Type hint’ler geliştiriciye ve analiz araçlarına yol gösterir; Python yorumlayıcısı ise çoğu durumda onları yalnızca izler ve çalışmaya devam eder.

``

## Type hint gerçekte ne yapar?

Python, dinamik tür sistemine sahip bir dildir. Değişkenlerin türü kaynak kodda sabitlenmez; çalışma zamanında nesneler üzerinden belirlenir. Aşağıdaki imza, `age` değişkeninin mutlaka tam sayı olacağını ilan etmekten çok bir niyet bildirir:

```python
def next_age(age: int) -> int:
    return age + 1
```

Bu fonksiyon için beklenen eşleme matematiksel olarak şöyle yazılabilir:

$$
f: \mathbb{Z} \rightarrow \mathbb{Z}, \qquad f(x)=x+1
$$

Ancak Python bu kümeye üyeliği otomatik olarak denetlemez. `next_age("20")` çağrısı daha fonksiyona girerken engellenmez; hata ancak `"20" + 1` işlemi yapılırken oluşur. Fonksiyon parametreyi hiç kullanmasaydı yanlış tür sessizce yoluna devam edebilirdi.

```python
def welcome(age: int) -> str:
    return "Hoş geldin!"

print(welcome("yirmi"))  # Sorunsuz çalışır
```

Buradaki `int`, çalışma zamanı muhafızı değil, `__annotations__` içinde saklanan bir meta veridir.

## Yanlış güven nerede başlıyor?

IDE’nin otomatik tamamlama sunması, parametrelerin renklenmesi ve editörde kırmızı çizgilerin görünmesi güçlü bir güvenlik hissi oluşturur. Fakat kod; API isteği, JSON belgesi, kullanıcı girdisi veya veritabanı kaydı aldığında dış dünyadan gelen değerler type hint sözleşmesini okumaz.

| Yaklaşım | Kontrol zamanı | Yanlış türü durdurur mu? | Temel amaç |
|---|---|---:|---|
| Type hint | Tek başına kontrol etmez | Hayır | Niyeti belgelemek |
| `mypy` / `pyright` | Çalıştırmadan önce | Analiz aşamasında | Statik hata bulmak |
| `isinstance` | Çalışma zamanı | Evet | Elle doğrulama |
| Pydantic | Çalışma zamanı | Evet | Veri doğrulama ve dönüştürme |

![python-type-hintleri-81](/img/python-type-hintleri-81.svg)


Statik analiz aracının yakalayabildiği hata oranını kabaca

$$
G = \frac{\text{analizde bulunan tür hataları}}{\text{toplam tür hataları}}
$$

olarak düşünürsek, $G$ hiçbir zaman otomatik olarak $1$ değildir. Özellikle `Any`, doğrulanmamış dış veri ve analiz edilmeyen modüller bu güvenceyi azaltır.

## Statik analiz eklenmediyse tabela bile okunmaz

Type hint yazmak tek başına yeterli değildir. CI sürecinde `mypy` veya `pyright` çalıştırılmıyorsa ekip, tabelaları yerleştirip sürücülerin bakmasını umuyor demektir.

```python
def repeat(text: str, count: int) -> str:
    return text * count

result = repeat(3, "iki")
```

Python bu çağrıyı başlatır; hata çalışma zamanında ortaya çıkar. Buna karşılık `mypy`, çağrıdaki iki argümanın da beklenen türlerle uyuşmadığını uygulamayı çalıştırmadan bildirir. Böylece type hint, ancak araç zinciriyle birleştiğinde gerçek bir kalite kapısına dönüşür.

## Sınır noktalarında doğrulama yapın

Uygulamanın içine gelen veriler güven sınırıdır. Bu noktalarda açık doğrulama kullanmak gerekir:

```python
def calculate_discount(price: float, rate: float) -> float:
    if not isinstance(price, (int, float)):
        raise TypeError("price sayısal olmalıdır")
    if not isinstance(rate, (int, float)):
        raise TypeError("rate sayısal olmalıdır")
    if not 0 <= rate <= 1:
        raise ValueError("rate, 0 ile 1 arasında olmalıdır")

    return float(price) * (1 - float(rate))
```

Burada tür kontrolü yetmez; `rate=42` teknik olarak `int` olsa da iş kuralına aykırıdır. Demek ki doğruluk iki katmanlıdır: tür uygunluğu ve alan doğrulaması. API modellerinde Pydantic, veri sınıflarında doğrulayıcılar veya kritik fonksiyonlarda açık kontroller kullanılabilir.

Sonuç olarak type hint’leri küçümsemek değil, doğru konumlandırmak gerekir. Onlar okunabilirliği, editör desteğini ve statik analizi güçlendiren mükemmel sözleşmelerdir; fakat sözleşmenin polisi değildir. Güvenilir Python kodu için type hint, statik analiz, test ve çalışma zamanı doğrulaması birlikte kullanılmalıdır.
