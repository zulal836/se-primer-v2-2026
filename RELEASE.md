# Sürüm durumu ve dağıtım kararı

5 Kasım 2026 · v0.1.0-demo geliştirme adayı. Eski uygulama yoktu; temel oyun sıfırdan kuruldu. Üç karar, iki son, profil uyarlaması, gönüllü veri toplama ve yerel CSV eklendi. Davranış modeli gerçek ONNX dosyasıyla açıklama derinliğini seçer. Temel kural karşılaştırması ve yükleme hatasında yedek vardır.

## Uygulanan / bekleyen

GitHub public proje deposu oluşturuldu: https://github.com/zulal836/se-primer-v2-2026 . İlk kaynak commit'i `869289e8fc2a7d3e5299d93f1671fc45b46943c9`; eğitim öncesi spec commit'i `5e9008e`. İlk Pages workflow koşusunda üçüncü taraf Cypress action'ının sunucu başlatma/bekleme adımı socket hatası verdi. Yerel sunucu başlatma ve hazır olma kontrolünü yapan `scripts/test_e2e.mjs` ile değiştirildi, Ubuntu 24.04 ortamı sabitlendi. Web yayın durumu aşağıda ayrıca doğrulanır.

Model dosyasındaki `data_source=sentetik`, `publishable=false` geliştirme durumunu gösterir. Bu model gerçek veriyle eğitilmiş v2.0 diye yayımlanamaz. Gerçek oturum sayısı başlangıçta 0; insan tutor değerlendirmesi bekliyor. Nihai HF commit'i henüz yoktur. GitHub ve Pages yayın sonuçları doğrulandıktan sonra bu dosyaya gerçek bağlantılar eklenir; `publication.json` otomatik yayın makbuzudur. Bağlantı şablonları gerçek bağlantı diye sunulmaz.

## Mimari ödünleşim

| Seçenek | İnternet / gecikme | Veri cihazdan çıkar mı? | Model gizliliği |
|---|---|---|---|
| Tarayıcı, seçilen | İlk sayfa/runtime/model indirmesi gerekir. Sonraki çıkarım yereldir; çevrimdışı yeniden açılış garanti edilmez, service worker yoktur. | Davranış sunucuya gönderilmez; kullanıcı CSV paylaşırsa çıkar. Sunucu yalnız normal dosya isteklerini görür. | İndirilen model herkese açıktır. |
| Cihaz içi mobil | Gömülü modelle ağsız çalışabilir; cihaz hızına bağlı. | Yerel çıkarımda gerekmez. | Uygulama paketinden çıkarılabilir. |
| Sunucu | Her istekte ağ ve servis gecikmesi, çevrimdışı kullanılamaz. | Girdiler sunucuya gider; gizlilik ve saklama yönetimi gerekir. | Dosya saklanabilir; çıktı sorgularından çıkarım/tersine mühendislik riski sürer. |

Tarayıcı, ücretsiz yayın ve davranışın cihazda kalması nedeniyle seçildi. Model sır gerektirmiyor. Küçük ONNX + npm ile eşleşen WASM sürümü kullanılır. Hastane senaryosu eğitim kurgusudur; gerçek hasta bilgisi yoktur.

## v2.0 için planlanan güvenli geçiş (henüz uygulanmadı)

1. **Eval:** 15+ tamamlanmış gerçek oturum, yeterli iki sınıf, oturum bazlı split, önceden belirlenen metrik kapısı ve 1e-4 ONNX paritesi. İnsan tutor incelemesi ayrıca tamamlanır. Model/config aynı HF commit'inde, web manifesti tam commit'e sabitlenir.
2. **Shadow:** gönüllü denemelerde mevcut kural oyuncuya gösterilir; aday model aynı girdide yerel olarak sessiz hesaplanır. İki kararı yerel inceleme CSV'sinde karşılaştırmak için ayrı uygulama gerekir; şu an üretimde shadow trafiği yoktur. En az 30 etiketli kararda model hata oranı, ihtiyaç sınıfı recall ve yükleme hataları incelenir. Mevcut sürümdeki “kural/model” seçimi otomatik shadow değildir.
3. **Canary %5:** model/config çifti test edilmiş adayla, rastgele oturum grubu altında yalnız %5'e açılır; gönüllü test grubunda organize edilir. Oturum sürüm boyunca sabit kalır. Kalan oyuncular mevcut kural sürümünde kalır. Bu yönlendirme henüz kodlanmadı, plan aşamasındadır.
4. **Progressive %25 → %50 → %100:** her aşamada en az 30 yeni etiketli karar ve bir gün gözlem. Parite ihlali olmaması, model yükleme/çıkarım hatasının %1 altında olması, ayrıntı ihtiyacı recall >=0.65 ve balanced accuracy >=0.70 aranır. Örnek sayısı küçükse ilerleme ertelenir. Kural ve modelin gerçek öğrenmeye etkisi ayrıca kullanıcı çalışmasıyla değerlendirilir.
5. **Durdurma:** tek bir <1e-4 parite ihlali, veri sözleşmesi bozulması veya eski E2E regresyonunda hata dağıtımı durdurur. Veri güvenliği olayı varsa rollout durur; yerel veri paylaşımı sınırlandırılır.

Bu sayılar yapılmış dağıtım sonuçları değildir. 3V: küçük model/tek komut Velocity'yi, eval+parite Validation'ı, hash ve sabit HF commit Versioning'i destekler.

## Geri alma

- İlk geliştirme sürümünden önceki model yoktur; güvenli mevcut sürüm kural modudur. Model kaynağı erişilemezse görünür kural yedeği devreye girer. Kullanıcı da girişten kuralı seçebilir.
- İlk gerçek yayın öncesinde çalışan web Git commit'i, HF repo+40 haneli commit ve model/config SHA-256 makbuza yazılır. Makbuz yoksa eski sürüm varmış gibi hash yazılmaz.
- Sonraki sorunlu yayında `public/model/source.json` dosyasını kaydedilmiş önceki HF commit'ine döndürün (model ve config birlikte). Önceki web commit'i gerekirse yeni dalda geri getirilebilir; geçmişi zorla silmeyin. Parite ve tüm E2E testlerini çalıştırın, ardından Pages'e normal yeni commit gönderin.
- İlk gerçek sürüm sorunluysa önceki doğrulanmış geliştirme web sürümüne dönün ve kullanıcılara kural modu seçildiğini açıkça bildirin. Yeni tarayıcı oturumunda kaynak ve durum etiketini kontrol edin. Uygulama kullanıcı kayıtlarını dağıtım sırasında silmez; kayıt sözleşmesi değişirse ayrıca göç planı gerekir.

Kaynak yaklaşım: [huggingface-hello-web](https://github.com/seyyah/huggingface-hello-web), [ONNX Runtime Web dağıtımı](https://onnxruntime.ai/docs/tutorials/web/deploy.html), [HF upload](https://huggingface.co/docs/huggingface_hub/guides/upload).
