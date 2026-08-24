---
layout: post
title: "Program Analizinde AST Kullanımı: Kaynak Kodunu Anlamlı Veriye Dönüştürmek"
math: true
categories: 
  - Bilgi
tags: 
  - AST
  - Program Analizi
  - Derleyiciler
---

Bir programın kaynak kodu, insan gözüyle satırlardan oluşur; fakat analiz araçları için asıl değerli olan şey bu satırların taşıdığı yapıdır. Abstract Syntax Tree (AST), yani Soyut Sözdizim Ağacı, kodu değişken tanımı, fonksiyon çağrısı, koşul ve döngü gibi anlamlı düğümlere ayırır. Böylece otomatik kalite kontrolleri, güvenlik taramaları ve kod dönüşümleri düzenli ifadelerin kırılgan dünyasından kurtulur.
``

AST oluşturma süreci genellikle iki temel aşamaya dayanır. Önce **lexer** karakterleri anahtar kelime, tanımlayıcı, operatör ve sayı gibi token'lara böler. Ardından **parser**, bu token'ların dilin gramerine uyup uymadığını denetler ve hiyerarşik ağacı üretir. “Soyut” sözcüğü önemlidir: Parantez, boşluk ve yorum gibi çoğu yüzeysel ayrıntı atılır; programın sözdizimsel iskeleti korunur.

Örneğin `toplam = fiyat * adet` ifadesinin kökünde bir atama düğümü bulunabilir. Sol çocuk `toplam` tanımlayıcısıdır; sağ çocuk ise çarpma işlemidir. Bu ilişkiyi kabaca şöyle düşünebiliriz:

$$Atama(toplam,\ Çarpma(fiyat, adet))$$

Bu temsil, bir değişkenin nerede yazıldığını veya riskli bir fonksiyonun hangi argümanlarla çağrıldığını bulmayı oldukça kolaylaştırır. Metin araması `eval` kelimesini yorum satırında da yakalayabilir; AST gezgini ise yalnızca gerçek çağrı düğümlerini inceler.

| Yaklaşım | Güçlü yanı | Temel sınırlama |
|---|---|---|
| Düzenli ifade | Hızlı, basit metin kuralları | İç içe yapıları ve bağlamı zayıf anlar |
| AST analizi | Sözdizimsel ilişkiyi bilir | Dil ayrıştırıcısına ihtiyaç duyar |
| Çalışma zamanı analizi | Gerçek davranışı gözler | Tüm yolları çalıştırmak zor olabilir |

Python ekosisteminde yerleşik `ast` modülü, bu fikri denemek için harika bir laboratuvardır. Aşağıdaki örnek, bir kaynak metindeki fonksiyon çağrılarını ziyaret eder ve çağrılan isimleri toplar:

```python
import ast

kod = """
def hesapla(x):
    print(x)
    return abs(x) + eval("2 + 2")
"""

class CagriBulucu(ast.NodeVisitor):
    def __init__(self):
        self.cagrilar = []

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            self.cagrilar.append(node.func.id)
        self.generic_visit(node)

agac = ast.parse(kod)
bulucu = CagriBulucu()
bulucu.visit(agac)
print(bulucu.cagrilar)  # ['print', 'abs', 'eval']
```

Buradaki `NodeVisitor`, ziyaretçi tasarım desenini uygular. Her `Call` düğümünde `visit_Call` metodu çalışır. Kritik nokta `generic_visit(node)` çağrısıdır: Bu çağrı yapılmazsa ziyaretçi, çağrının içindeki alt ifadeleri dolaşmayabilir. Gerçek bir güvenlik kuralında `eval` çağrısını işaretleyebilir, kullanılan dosyayı ve satır numarasını `node.lineno` üzerinden raporlayabilirsiniz.

AST ile analiz yaparken yalnızca düğüm türüne bakmak her zaman yeterli değildir. Örneğin `os.system(...)` bir `Name` yerine `Attribute` düğümü olarak gelir. Ayrıca çağrılan fonksiyonun güvenli olup olmadığı, argümanın sabit mi yoksa kullanıcı girdisi mi olduğuna bağlı olabilir. Bu noktada veri akışı analizi devreye girer: Bir değerin tanımdan kullanıma ulaşabildiği yollar araştırılır.

| Analiz sorusu | İlgili AST düğümü | Örnek kullanım |
|---|---|---|
| Fonksiyon kim çağırıyor? | `Call`, `Name`, `Attribute` | Yasak API taraması |
| Değişken nerede atanıyor? | `Assign`, `AnnAssign` | Kullanılmayan değişken bulma |
| Koşul var mı? | `If`, `Compare` | Karmaşıklık ölçümü |
| Fonksiyon ne döndürüyor? | `FunctionDef`, `Return` | Tip ve sözleşme kontrolü |

AST'nin güzelliği, aynı ağacın hem okumaya hem dönüştürmeye izin vermesidir. Bir kod modernleştirici eski API çağrılarını yeni çağrılarla değiştirebilir; bir linter stil ihlallerini bulabilir; eğitim aracı ise öğrencinin döngü ve koşul kullanımını ölçebilir. Ancak AST tek başına programın kesin davranışını vermez: tür bilgisi, modüller arası çağrılar ve çalışma zamanı değerleri ek analiz gerektirir. Yine de kaynak kodunu metin değil yapı olarak ele almak, güvenilir otomasyonun en sağlam başlangıç noktasıdır.
