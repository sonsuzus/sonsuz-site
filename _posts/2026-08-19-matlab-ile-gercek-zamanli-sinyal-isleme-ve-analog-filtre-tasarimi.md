---
layout: post
title: "MATLAB ile Gerçek Zamanlı Sinyal İşleme ve Analog Filtre Tasarımı"
math: true
categories: 
  - Program
tags: 
  - matlab
  - sinyal işleme
  - fourier dönüşümü
  - filtre tasarımı
toc: true
---

Bir mikrofonun uğultusunu temizlemek, titreşim sensöründen arıza belirtisi yakalamak veya kalp atışı verisindeki gürültüyü azaltmak; hepsi sinyal işlemenin günlük hayattaki süper güçleridir. MATLAB, güçlü matematik altyapısı ve Signal Processing Toolbox araçları sayesinde ham ses ya da sensör örneklerini anlamlı bilgiye dönüştürmek için oldukça uygundur. Üstelik doğru örnekleme hızı, Fourier analizi ve filtre seçimiyle bu işlemler gerçek zamana yakın biçimde yapılabilir.

``

## Sinyali zaman alanından frekans alanına taşımak

Bir sinyalin zaman içindeki değişimi her zaman ne içerdiğini açıkça söylemez. Örneğin, sensör verisindeki hızlı titreşimler bir mekanik arızaya; ses kaydındaki sabit 50 Hz bileşeni ise elektrik şebekesi gürültüsüne işaret edebilir. Fourier dönüşümü, sinyali sinüs bileşenlerine ayırarak bu frekansları görünür kılar.

Sürekli zamanlı Fourier dönüşümü şu şekilde tanımlanır:

$$X(f) = \int_{-\infty}^{\infty} x(t)e^{-j2\pi ft}dt$$

Dijital sistemlerde ise ayrık Fourier dönüşümü (DFT) kullanılır. MATLAB'daki `fft` fonksiyonu, DFT'yi hızlı biçimde hesaplayan FFT algoritmasını kullanır. Örnekleme frekansı $F_s$ ise analiz edilebilecek en yüksek frekans Nyquist sınırı olan $F_s/2$'dir. Bu nedenle 8 kHz'e kadar ses bileşeni için en az 16 kHz örnekleme gerekir.

| Kavram | Ne anlatır? | MATLAB karşılığı |
|---|---|---|
| Zaman alanı | Genliğin zamana göre değişimi | `plot(t, x)` |
| Frekans alanı | Sinyaldeki frekansların gücü | `fft(x)` |
| Örnekleme hızı | Saniyedeki ölçüm sayısı | `Fs` |
| Nyquist frekansı | Güvenli üst frekans limiti | `Fs/2` |

Aşağıdaki örnek, gürültülü bir sensör sinyalinin spektrumunu çıkarır. Kod, 60 Hz civarındaki istenmeyen bileşeni gözlemlemek için kullanılabilir.

```matlab
Fs = 1000;                 % Örnekleme frekansı
T = 1/Fs;
t = 0:T:2-T;

x = sin(2*pi*20*t) + 0.5*sin(2*pi*60*t) + 0.2*randn(size(t));
N = length(x);
X = fft(x);
f = (0:N-1) * (Fs/N);

plot(f(1:N/2), abs(X(1:N/2))/N);
xlabel('Frekans (Hz)'); ylabel('Genlik');
grid on;
```

## Analog filtre mantığı: Hangi frekans yaşamalı?

Filtre tasarımında temel soru şudur: “Hangi frekansları koruyor, hangilerini bastırıyoruz?” Analog filtreler bu davranışı Laplace düzlemindeki transfer fonksiyonu ile tanımlar. Birinci dereceden alçak geçiren RC filtresinin transfer fonksiyonu şöyledir:

$$H(s) = \frac{1}{1 + sRC}$$

Kesim frekansı ise $f_c = \frac{1}{2\pi RC}$ formülüyle bulunur. Pratikte MATLAB'da analog prototip tasarlanır, ardından sayısal uygulama için dönüşüm yapılır. Butterworth filtreler geçiş bandında düz tepki verirken, Chebyshev filtreler daha keskin geçiş karşılığında dalgalanma oluşturur.

| Filtre türü | Geçirdiği bölge | Tipik kullanım |
|---|---|---|
| Alçak geçiren | Düşük frekanslar | Sensör gürültüsü azaltma |
| Yüksek geçiren | Yüksek frekanslar | DC kayması temizleme |
| Bant geçiren | Belirli frekans bandı | Ses tonu veya titreşim takibi |
| Bant durduran | Dar bir istenmeyen bant | 50/60 Hz uğultu giderme |

Örneğin 100 Hz üzerindeki titreşimleri bastırmak için dördüncü dereceden Butterworth alçak geçiren filtre tasarlanabilir:

```matlab
fc = 100;                  % Kesim frekansı
Wn = fc / (Fs/2);          % Nyquist'e göre normalize frekans
[b, a] = butter(4, Wn, 'low');
y = filter(b, a, x);

plot(t, x, ':', t, y, 'LineWidth', 1.2);
legend('Ham sinyal', 'Filtrelenmiş sinyal');
xlabel('Zaman (s)'); grid on;
```

Gerçek zamanlı senaryoda veriyi küçük bloklar halinde okumak önemlidir. `audioDeviceReader`, `dsp.AudioFileReader` veya seri porttan gelen sensör paketleriyle her blok filtrelenebilir. Filtrenin önceki durumunu korumak için `dsp.IIRFilter` gibi System object yapıları tercih edilir; aksi halde blok sınırlarında rahatsız edici sıçramalar oluşabilir. Kısacası Fourier dönüşümü sinyalin dedektifidir, filtre ise olay yerine doğru müdahale eden teknisyenidir.
