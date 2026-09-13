---
layout: post
title: "Fortran'ın Bilimsel Hesaplamadaki 70 Yıllık Direnci"
math: true
categories: 
  - Bilgi
tags: 
  - fortran
  - bilimsel hesaplama
  - yüksek başarımlı hesaplama
  - hpc
  - programlama tarihi
  - sayısal analiz
toc: true
---

1957 yılında IBM tarafından geliştirilen Fortran, yazılım dünyasının dinozorlarından biri gibi görünebilir. Ancak bu dinozor müzede sergilenmiyor; iklim modellerinden kuantum fiziğine, akışkanlar dinamiğinden uzay araştırmalarına kadar sayısız alanda hesaplama yapmayı sürdürüyor. Üstelik bunu, kendisinden onlarca yıl genç dillere meydan okuyarak gerçekleştiriyor.

``

## Formülleri makineye anlatma fikri

Fortran adı, **Formula Translation** ifadesinden gelir. Dilin temel amacı matematiksel formülleri, makinenin çalıştırabileceği komutlara dönüştürmekti. İlk sürüm çıktığında programcılar çoğunlukla makine dili veya assembly kullanıyordu. Örneğin

$$E = mc^2$$

gibi basit bir ilişkiyi kodlamak bile düşük seviyeli ayrıntılarla uğraşmayı gerektiriyordu. Fortran, bilim insanlarının işlemci yazmaçları yerine denklemlere odaklanmasını sağladı.

Bu yaklaşım günümüzde sıradan görünebilir, fakat 1950'lerde devrim niteliğindeydi. Derleyicinin insan tarafından yazılmış formülleri verimli makine koduna çevirebileceğini kanıtladı ve yüksek seviyeli programlama dillerinin önünü açtı.

## Neden hâlâ bu kadar hızlı?

Bilimsel uygulamalarda aynı işlemler milyonlarca veri üzerinde tekrar edilir. Örneğin iki vektörün skaler çarpımı

$$s = \sum_{i=1}^{n} a_i b_i$$

şeklinde tanımlanır. Fortran'ın dizi yapısı ve bellek modeli, bu tür işlemleri derleyicinin kolayca optimize edebileceği biçimde ifade eder. Derleyici döngüleri vektörleştirebilir, birden fazla işlemi paralel yürütebilir ve işlemcinin önbelleğini etkili kullanabilir.

| Özellik | Fortran | Python | C++ |
|---|---|---|---|
| Ham sayısal performans | Çok yüksek | Yorumlayıcıda düşük | Çok yüksek |
| Dizi işlemleri | Dilin doğal parçası | Genellikle NumPy gerekir | Kütüphane gerekebilir |
| Bellek yönetimi | Görece sade | Büyük ölçüde otomatik | Esnek fakat karmaşık |
| Öğrenme ekosistemi | Uzmanlaşmış | Çok geniş | Çok geniş |
| Eski bilimsel kodlarla uyum | Mükemmel | Dolaylı | Orta |

Python'ın yavaş görünmesine rağmen bilimsel hesaplamada popüler olması bir çelişki değildir. NumPy ve SciPy gibi araçların ağır hesaplamaları çoğu zaman Fortran, C veya C++ ile yazılmış alt katmanlara devrettiğini unutmamak gerekir. Başka bir deyişle Python sahnede şarkı söylerken Fortran bazen orkestrayı yönetir.

## Modern Fortran nasıl görünüyor?

Fortran yalnızca delikli kartlardan kalma satır numaraları ve `GOTO` komutlarından ibaret değildir. Modern standartlar modüller, kullanıcı tanımlı türler, paralel programlama özellikleri ve okunabilir dizi işlemleri sunar:

```fortran
program vector_demo
  implicit none
  integer, parameter :: n = 5
  real :: a(n), b(n), sonuc

  a = [1.0, 2.0, 3.0, 4.0, 5.0]
  b = [5.0, 4.0, 3.0, 2.0, 1.0]
  sonuc = dot_product(a, b)

  print *, "Skaler çarpım:", sonuc
end program vector_demo
```

Buradaki `implicit none`, değişkenlerin açıkça tanımlanmasını zorunlu tutarak yazım hatalarını azaltır. `dot_product` ise skaler çarpımı elle döngü kurmadan ifade eder. Derleyici bu işlemi hedef işlemcinin SIMD komutlarına uygun şekilde optimize edebilir.

## Yetmiş yıllık kod neden çöpe atılmıyor?

Bilimsel yazılımların değeri yalnızca kaynak koddan gelmez. On yıllar boyunca doğrulanmış fizik modelleri, sayısal yöntemler ve deney sonuçları bu kodlarda birikir. Milyonlarca satırlık bir iklim modelini sırf daha moda bir dil kullanmak için yeniden yazmak pahalı ve risklidir. Küçük bir yuvarlama farkı bile uzun simülasyonlarda büyük sonuç değişikliklerine dönüşebilir.

Fortran ayrıca BLAS, LAPACK ve çeşitli atmosfer modelleme sistemleri gibi kritik altyapıların merkezinde bulunur. Yeni sürümleri eski kodları büyük ölçüde desteklediği için kurumlar yatırımlarını koruyabilir.

Elbette dilin paket yönetimi, geliştirici araçları ve genç programcı topluluğu Python veya Rust kadar güçlü değildir. Buna rağmen süper bilgisayarlarda performans, güvenilirlik ve doğrulanmış kod birikimi moda akımlarından daha önemlidir. Fortran'ın sırrı ölümsüz olması değil; çözmek için tasarlandığı problemin hâlâ son derece canlı olmasıdır.
