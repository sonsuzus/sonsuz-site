---
layout: post
title: "Kubernetes Temelleri ve Pod Mantığı: Konteyner Orkestrasyonuna İlk Adım"
math: true
categories: 
  - Bilgi
tags: 
  - kubernetes
  - docker
  - konteyner
  - devops
  - pod
image: /img/kubernetes-temelleri-ve-14.png
toc: true
---

![kubernetes-temelleri-ve-14](/img/kubernetes-temelleri-ve-14.svg)


Modern uygulamalar tek bir sunucuda çalışan dev programlar olmaktan çıktı; küçük, bağımsız ve konteynerleşmiş servislerden oluşuyor. Ancak yüzlerce konteyneri doğru makineye yerleştirmek, çökenleri yeniden başlatmak ve trafik arttığında kapasiteyi büyütmek elle yapılabilecek bir iş değildir. Kubernetes, tam bu noktada konteyner kümelerini yöneten, dağıtımı otomatikleştiren ve uygulamanın arzu edilen durumunu koruyan orkestrasyon platformudur.
``

Kubernetes'in temel fikri **bildirimsel yönetimdir**: “Şu komutu çalıştır” demek yerine “Uygulamamdan üç kopya çalışsın” dersiniz. Kontrol düzlemi mevcut durumu izler, hedefle karşılaştırır ve farkı kapatmak için gerekli işlemleri yapar. Bu yaklaşımın basit modeli şöyledir:

$$Hata = Arzu\ Edilen\ Durum - Mevcut\ Durum$$

Hata sıfır değilse Kubernetes yeni Pod oluşturabilir, başarısız olanı değiştirebilir veya fazla kopyaları azaltabilir. Bu sürekli uzlaştırma döngüsü, sistemin tek seferlik komutlara değil hedef duruma odaklanmasını sağlar.

## Küme mimarisi: Kararı kim verir?

Bir Kubernetes kümesi, karar veren **control plane** ile iş yükünü çalıştıran **worker node**'lardan oluşur. API Server tüm isteklerin kapısıdır; etcd kümenin kalıcı durum kaydını tutar; scheduler uygun node'u seçer; controller'lar ise hedef durumu korur. Node tarafındaki kubelet Pod'ları çalıştırır, kube-proxy ise ağ kurallarına yardım eder.

| Bileşen | Görevi | Günlük benzetme |
|---|---|---|
| API Server | API isteklerini kabul eder | Resepsiyon |
| Scheduler | Pod için uygun node seçer | İş dağıtım sorumlusu |
| Controller Manager | Hedef kopya sayısını korur | Kalite kontrol |
| kubelet | Node üzerindeki Pod'ları yönetir | Vardiya amiri |
| etcd | Küme durumunu saklar | Kasa defteri |

## Pod: Kubernetes'in en küçük dağıtım birimi

Yeni başlayanların sık yaptığı hata, Pod'u doğrudan “konteyner” sanmaktır. Pod, bir veya daha fazla konteyneri saran mantıksal çalışma birimidir. Aynı Pod'daki konteynerler aynı ağ ad alanını paylaşır; yani birbirlerine `localhost` üzerinden ulaşabilirler. Ayrıca ortak volume kullanabilirler. Bu nedenle ana uygulama konteynerinin yanında log toplayan veya proxy görevi gören bir *sidecar* konteyneri bulundurmak mantıklıdır.

| Kavram | Kapsam | Ne zaman kullanılır? |
|---|---|---|
| Konteyner | Tek süreç/uygulama | Uygulamayı paketlemek |
| Pod | Birlikte çalışan konteynerler | Çalıştırma ve ağ birimi |
| Deployment | Pod replikalarını yönetir | Stateless web uygulamaları |
| Service | Pod'lara sabit erişim noktası verir | Trafiği yönlendirmek |

Tek bir Pod manifesti aşağıdaki gibi tanımlanabilir. Bu örnek, NGINX imajını çalıştıran ve `app: web` etiketi taşıyan bir Pod oluşturur:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-pod
  labels:
    app: web
spec:
  containers:
    - name: nginx
      image: nginx:1.27
      ports:
        - containerPort: 80
```

Bu dosyayı `pod.yaml` adıyla kaydedip aşağıdaki komutla uygularız:

```bash
kubectl apply -f pod.yaml
kubectl get pods -o wide
kubectl describe pod web-pod
```

Yine de üretimde çoğunlukla çıplak Pod oluşturulmaz. Pod ölürse geri gelmesini, sürüm güncellemelerini ve kopya sayısını yönetmek için **Deployment** kullanılır. Scheduler, node seçerken CPU/bellek istekleri, kaynak limitleri, node seçicileri ve kısıtları değerlendirir. Basitleştirilmiş kapasite hesabında, bir node'un yerleştirebileceği Pod sayısı yaklaşık olarak şudur:

$$N = \min\left(\left\lfloor\frac{CPU_{kullanılabilir}}{CPU_{istek}}\right\rfloor,\left\lfloor\frac{RAM_{kullanılabilir}}{RAM_{istek}}\right\rfloor\right)$$

Örneğin 4 CPU ve 8 GiB kullanılabilir kaynağa sahip bir node'da, her biri 0.5 CPU ve 1 GiB isteyen Pod'lardan en fazla $\min(8,8)=8$ adet yerleşebilir.

Ölçekleme iki katmanda gerçekleşir: **Horizontal Pod Autoscaler (HPA)** Pod sayısını metriklere göre artırır; **Cluster Autoscaler** ise Pod'lar sığmadığında node ekleyebilir. Böylece trafik yükseldiğinde sistem hem uygulama kopyalarını hem de altyapı kapasitesini büyütür. Kubernetes sihir yapmaz; ama doğru tanımlanmış hedefleri sabırla, sürekli ve otomatik biçimde gerçeğe dönüştürür.
