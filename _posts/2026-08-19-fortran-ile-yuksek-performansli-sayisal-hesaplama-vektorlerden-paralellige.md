---
layout: post
title: "Fortran ile Yüksek Performanslı Sayısal Hesaplama: Vektörlerden Paralelliğe"
math: true
categories: 
  - Bilgi
tags: 
  - fortran
  - hpc
  - sayısal hesaplama
image: /img/fortran-ile-yuksek-43.png
---

Fortran, “eski ama eskimeyen” dillerin en güçlü örneklerinden biridir. Fizik, iklim modelleme, hesaplamalı akışkanlar dinamiği ve sonlu elemanlar gibi alanlarda bugün hâlâ yoğun biçimde kullanılır. Bunun sebebi nostalji değil; dizilerle doğal çalışması, derleyicilerin agresif optimizasyon yapabilmesi ve paralel donanımdan iyi yararlanabilmesidir. Özellikle milyonlarca hücre veya parçacık içeren simülasyonlarda birkaç yüzde puanlık performans farkı, saatler süren bir hesabı dakikalarca kısaltabilir.
``

Yüksek performanslı sayısal hesaplamanın temelinde aynı işlemin çok sayıda veri noktası üzerinde uygulanması vardır. Örneğin bir sıcaklık alanının zamana göre güncellenmesini düşünelim. Basitleştirilmiş difüzyon denklemi şöyledir:

$$\frac{\partial T}{\partial t} = \alpha \nabla^2 T$$

Burada $T$ sıcaklık, $\alpha$ ise ısıl yayınım katsayısıdır. Izgara tabanlı bir çözümde uzay ayrıklaştırılır; yani sürekli alan, büyük bir sayı dizisine dönüşür. Fortran’ın dizi sözdizimi tam olarak bu tür işlere uygundur: Tek tek elemanları yönetmek yerine dizinin tamamına uygulanacak işlemi tarif edersiniz.

| Yaklaşım | Güçlü yönü | Dikkat edilmesi gereken |
|---|---|---|
| Klasik `do` döngüsü | Tam kontrol, geniş uyumluluk | Bağımlılıklar optimizasyonu sınırlar |
| Dizi işlemleri | Okunabilir ve matematiksel ifade gücü yüksek | Geçici dizi üretimi maliyetli olabilir |
| `do concurrent` | Bağımsız iterasyonları açıkça belirtir | Döngü içinde veri yarışına izin verilmez |
| OpenMP | Çok çekirdekli CPU paralelliği | Paylaşılan değişkenler dikkatle yönetilmelidir |

![fortran-ile-yuksek-43](/img/fortran-ile-yuksek-43.svg)


Önce vektörel düşünelim. Fortran’da iki vektörün skaler çarpımını veya eleman bazlı dönüşümünü açık döngü yazmadan ifade edebilirsiniz. Bu, yalnızca kodu kısaltmaz; derleyiciye SIMD, yani tek komutla birden fazla veri işleme fırsatı da verir. Modern işlemcilerde AVX benzeri vektör birimleri aynı anda birden fazla kayan noktalı değeri işleyebilir.

```fortran
program vector_example
  implicit none
  integer, parameter :: n = 1000000
  real(8) :: x(n), y(n), energy

  x = [(real(i, 8) * 0.001d0, i = 1, n)]
  y = sin(x) * exp(-x)
  energy = sum(y * y)

  print *, 'Enerji = ', energy
end program vector_example
```

Bu örnekte `y = sin(x) * exp(-x)` ifadesi eleman bazında çalışır. `sum(y * y)` ise $E = \sum_i y_i^2$ hesabını yapar. Gerçek projelerde `real(8)` yerine taşınabilirlik için `iso_fortran_env` içindeki `real64` tercih etmek daha iyi bir alışkanlıktır.

Dizi işlemleri her zaman otomatik olarak en hızlı seçenek değildir. Çok büyük dizilerde `sin(x) * exp(-x)` ara bellek kullanımı oluşturabilir. Bellek bant genişliği, işlemcinin teorik hızından daha kritik hâle gelebilir. Bu nedenle performansın özeti kabaca şu ilişkiyle düşünülebilir:

$$T_{toplam} \approx T_{hesaplama} + T_{bellek} + T_{iletişim}$$

Çok çekirdekli paralellik gerektiğinde OpenMP devreye girer. Aşağıdaki örnek, bağımsız dizi elemanlarını CPU çekirdeklerine dağıtır:

```fortran
program omp_wave
  use omp_lib
  implicit none
  integer, parameter :: n = 10000000
  integer :: i
  real(8), allocatable :: u(:), next_u(:)

  allocate(u(n), next_u(n))
  u = 0.0d0
  u(n/2) = 1.0d0

  !$omp parallel do default(none) shared(u, next_u) private(i)
  do i = 2, n - 1
    next_u(i) = 0.5d0 * (u(i-1) + u(i+1))
  end do
  !$omp end parallel do

  deallocate(u, next_u)
end program omp_wave
```

Bu kod, komşu hücrelerin ortalamasını alarak basit bir güncelleme yapar. `next_u` ayrı tutulduğu için her iterasyon yalnızca eski `u` değerlerini okur; böylece veri yarışı oluşmaz. Derleme için çoğu GNU Fortran kurulumunda `gfortran -O3 -fopenmp dosya.f90` kullanılabilir.

Son olarak, HPC’de ölçmeden optimizasyon yapmak tahmin oyunudur. `-O3`, profil araçları, uygun veri yerleşimi ve mümkünse sınır kontrollerinin üretim derlemesinde kapatılması önemlidir. Fortran’ın sırrı da burada: Bilimsel problemi diziler ve bağımsız hesaplar olarak doğru modellerseniz, dil hem okunabilir hem de canavar gibi hızlı kod üretebilir.
