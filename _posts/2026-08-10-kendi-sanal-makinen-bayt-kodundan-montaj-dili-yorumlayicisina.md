---
layout: post
title: "Kendi Sanal Makinen: Bayt Kodundan Montaj Dili Yorumlayıcısına"
math: true
categories: 
  - Proje
tags: 
  - sanal makine
  - bayt kodu
  - yorumlayıcı
image: /img/kendi-sanal-makinen-60.png
---

Bir sanal makine (VM) tasarlamak, bilgisayarların sihirli görünen çalışma biçimini küçük ve yönetilebilir parçalara ayırmanın harika yoludur. Bu projede gerçek bir işlemciyi taklit etmeye çalışmayacağız; bunun yerine kendi komut kümesine, kayıtçılarına ve belleğine sahip minik bir işlemci oluşturacağız. Ardından bu işlemcinin anlayacağı bayt kodunu tanımlayıp, insanlar için daha okunabilir bir montaj dili yorumlayıcısı yazacağız. Sonuç: `LOAD`, `ADD` ve `JMP` gibi komutlarla program çalıştıran oyuncak ama öğretici bir bilgisayar.

``

Bir VM'nin kalbinde **fetch-decode-execute** döngüsü bulunur. İşlemci önce program sayacının (`PC`) gösterdiği adresteki komutu getirir, komutun ne olduğunu çözer ve etkisini uygular. Son olarak `PC` bir sonraki komuta ilerler. Kavramsal olarak bu döngü şöyledir:

$$\text{Durum}_{t+1} = \text{Execute}(\text{Decode}(\text{Memory}[PC_t]), \text{Durum}_t)$$

Durum; bellek, kayıtçılar, yığın ve program sayacından oluşur. Gerçek işlemcilerde çok daha fazla ayrıntı vardır; ancak eğitim amaçlı tasarımda iki kayıtçı (`R0`, `R1`), 256 hücrelik bellek ve bir `PC` yeterlidir.

| Bileşen | Gerçek işlemcideki rolü | Mini VM karşılığı |
|---|---|---|
| Kayıtçı | Çok hızlı geçici veri alanı | `R0` ve `R1` tamsayıları |
| Program sayacı | Sıradaki komutun adresi | `pc` değişkeni |
| RAM | Kod ve veriyi saklar | 256 baytlık liste |
| Opcode | İşlem türünü belirtir | `1 = LOAD`, `2 = ADD` |

![kendi-sanal-makinen-60](/img/kendi-sanal-makinen-60.svg)


Önce komutlarımızın ikili biçimini seçelim. Basitlik için her komut iki bayt olsun: ilk bayt opcode, ikinci bayt operand. Örneğin `LOAD 7`, `R0` içine 7 yüklerken `ADD 3`, `R0` değerine 3 eklesin. `PRINT` ise operand gerektirmese de sabit uzunluğu korumak için ikinci baytı görmezden gelebilir.

| Mnemonic | Opcode | Operand | Etki |
|---|---:|---|---|
| `LOAD n` | `1` | `n` | `R0 = n` |
| `ADD n` | `2` | `n` | `R0 = R0 + n` |
| `STORE a` | `3` | adres | `RAM[a] = R0` |
| `JMP a` | `4` | adres | `PC = a` |
| `PRINT` | `5` | yok | `R0` yazdır |
| `HALT` | `255` | yok | Programı bitir |

Aşağıdaki Python sınıfı, bayt kodunu doğrudan yürüten VM'nin temelidir. `pc += 2` varsayılan ilerlemedir; atlama komutu bu akışı değiştirir. Böylece koşullar ve döngüler eklemek için sağlam bir temel oluşur.

```python
class MiniVM:
    def __init__(self, code):
        self.memory = list(code) + [0] * (256 - len(code))
        self.r0 = 0
        self.pc = 0
        self.running = True

    def run(self):
        while self.running:
            opcode = self.memory[self.pc]
            operand = self.memory[self.pc + 1]
            self.pc += 2

            if opcode == 1:
                self.r0 = operand
            elif opcode == 2:
                self.r0 += operand
            elif opcode == 3:
                self.memory[operand] = self.r0
            elif opcode == 4:
                self.pc = operand
            elif opcode == 5:
                print(self.r0)
            elif opcode == 255:
                self.running = False
            else:
                raise ValueError(f"Bilinmeyen opcode: {opcode}")
```

Bayt kodu makine için mükemmeldir, insan için ise `1, 7, 2, 3, 5, 0` gibi gizemli sayılardan ibarettir. Yorumlayıcının ya da mini assembler'ın görevi, metin komutlarını opcode çiftlerine çevirmektir. Bu katman, kaynak kod ile yürütülebilir temsil arasındaki çeviridir.

```python
OPCODES = {"LOAD": 1, "ADD": 2, "STORE": 3,
           "JMP": 4, "PRINT": 5, "HALT": 255}

def assemble(source):
    bytecode = []
    for line in source.splitlines():
        parts = line.strip().upper().split()
        if not parts or parts[0].startswith(";"):
            continue
        opcode = OPCODES[parts[0]]
        operand = int(parts[1]) if len(parts) > 1 else 0
        bytecode.extend([opcode, operand])
    return bytecode

program = """
LOAD 7
ADD 3
PRINT
HALT
"""
MiniVM(assemble(program)).run()  # 10
```

Bu küçük tasarımda her komutun maliyetini kabaca $O(1)$ kabul edebiliriz. Dolayısıyla $n$ komutluk, sonlanan bir programın çalışma süresi $O(n)$ olur. Bir sonraki eğlenceli adım `SUB`, `JZ` ve etiket desteği eklemektir. Etiketler, sayısal adres ezberlemek yerine `JMP DONGU` yazmanızı sağlar; VM'niz böylece basit hesaplamalardan gerçek kontrol akışına doğru evrilir.
