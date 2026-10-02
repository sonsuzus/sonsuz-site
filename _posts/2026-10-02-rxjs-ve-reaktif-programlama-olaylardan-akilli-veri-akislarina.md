---
layout: post
title: "RxJS ve Reaktif Programlama: Olaylardan Akıllı Veri Akışlarına"
math: true
categories: 
  - Bilgi
tags: 
  - rxjs
  - reaktif programlama
  - javascript
  - typescript
  - observable
  - asenkron programlama
toc: true
image: /img/rxjs-ve-reaktif-12.png
---

Bir düğmeye tıklanması, sunucudan yanıt gelmesi veya klavyede tuşa basılması aynı ortak özelliğe sahiptir: Hepsi zaman içinde gerçekleşen olaylardır. RxJS, bu olayları tek tek yakalamak yerine onları akan bir veri dizisi olarak ele almamızı sağlar. Böylece uygulamamız, iç içe geri çağırma fonksiyonlarından oluşan bir labirent yerine filtreleri ve dönüşümleri bulunan düzenli bir veri boru hattına dönüşür.

![rxjs-ve-reaktif-12](/img/rxjs-ve-reaktif-12.svg)

``

## Reaktif programlama nedir?

Reaktif programlama, bir değerin yalnızca mevcut hâliyle değil, **zaman içindeki değişimleriyle** ilgilenen programlama yaklaşımıdır. Geleneksel kodda veriyi istediğimiz anda sorgularız. Reaktif kodda ise bir kaynağa abone olur, yeni veri geldiğinde tepki veririz.

Bir veri akışını matematiksel olarak zamana bağlı olaylar dizisi şeklinde düşünebiliriz:

$$S = \{(t_1, x_1), (t_2, x_2), \ldots, (t_n, x_n)\}$$

Burada $t_i$ olayın gerçekleştiği zamanı, $x_i$ ise taşınan değeri temsil eder. Örneğin $x_i$, kullanıcının arama kutusuna yazdığı metin olabilir.

| Yaklaşım | Veriyle ilişki | Asenkron olaylar | Tipik kullanım |
|---|---|---|---|
| Imperatif | Veriyi kod çağırır | Elle yönetilir | Basit, sıralı işlemler |
| Promise | Tek gelecek değer | Bir kez sonuçlanır | Tek ağ isteği |
| Observable | Zaman içinde çok değer | Operatörlerle yönetilir | Tıklama, form ve canlı veri |

## Observable, Observer ve Subscription

RxJS dünyasının başrolünde **Observable** bulunur. Observable, değerlerin ne zaman ve nasıl üretileceğini tanımlar. **Observer**, akıştan gelen `next`, `error` ve `complete` bildirimlerini karşılar. `subscribe()` çağrısıyla oluşan **Subscription** ise bu bağlantıyı temsil eder.

```typescript
import { Observable } from 'rxjs';

const sayac$ = new Observable<number>(observer => {
  observer.next(1);
  observer.next(2);
  observer.next(3);
  observer.complete();
});

const abonelik = sayac$.subscribe({
  next: deger => console.log('Gelen:', deger),
  error: hata => console.error(hata),
  complete: () => console.log('Akış tamamlandı')
});

abonelik.unsubscribe();
```

Bu örnekte `$` işareti özel bir JavaScript kuralı değildir; değişkenin Observable taşıdığını anlatan yaygın bir isimlendirme geleneğidir. `unsubscribe()` çağrısı özellikle sonsuz kullanıcı olaylarında bellek sızıntısını önlemek için önemlidir.

## Operatörlerle veri boru hattı kurmak

RxJS operatörleri, bir akışı başka bir akışa dönüştüren saf fonksiyonlar gibi düşünülebilir. Bir dönüşüm operatörü matematiksel olarak $f: S \rightarrow S'$ biçiminde ifade edilebilir. `map` değerleri dönüştürür, `filter` uygun olmayanları eler, `debounceTime` ise hızlı olayların sakinleşmesini bekler.

```typescript
import { fromEvent, map, filter, debounceTime } from 'rxjs';

const kutu = document.querySelector<HTMLInputElement>('#arama')!;

const arama$ = fromEvent<InputEvent>(kutu, 'input').pipe(
  map(() => kutu.value.trim()),
  debounceTime(300),
  filter(metin => metin.length >= 3)
);

arama$.subscribe(metin => console.log('Aranacak:', metin));
```

Bu boru hattı, her klavye hareketinde işlem yapmak yerine 300 milisaniye bekler ve en az üç karakter içeren metinleri geçirir. Sonuç: Daha az gereksiz işlem ve daha mutlu bir sunucu!

## Ağ isteklerinde switchMap

Arama metniyle HTTP isteği yapılırken önceki istek geç tamamlanabilir. `switchMap`, yeni değer geldiğinde eski iç akıştan çıkarak güncel isteğe geçer.

```typescript
import { switchMap } from 'rxjs/operators';
import { from } from 'rxjs';

const sonuc$ = arama$.pipe(
  switchMap(metin =>
    from(fetch(`/api/ara?q=${encodeURIComponent(metin)}`))
  ),
  switchMap(yanit => from(yanit.json()))
);

sonuc$.subscribe({
  next: veri => console.log('Sonuçlar:', veri),
  error: hata => console.error('İstek başarısız:', hata)
});
```

| Operatör | Davranış | Uygun senaryo |
|---|---|---|
| `switchMap` | Öncekini bırakır | Canlı arama |
| `mergeMap` | Akışları paralel yürütür | Bağımsız istekler |
| `concatMap` | Sırayla çalıştırır | İşlem kuyruğu |
| `exhaustMap` | Aktif işlem bitene kadar yeniyi yok sayar | Tekrarlanan gönderim tıklamaları |

RxJS’nin gücü, asenkronluğu ortadan kaldırmasında değil, onu açık ve birleştirilebilir akışlara dönüştürmesindedir. Kaynağı Observable olarak modelleyip doğru operatörleri seçtiğimizde tıklamalar, istekler ve zamanlayıcılar aynı düşünce modeliyle yönetilebilir. Reaktif programlamanın sihri de tam burada başlar: Olayları kovalamak yerine akışın kurallarını tanımlarız.
