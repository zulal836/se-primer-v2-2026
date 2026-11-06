# Sürüm durumu ve dağıtım kararı

## Ayrı public SENTETİK GELİŞTİRME DEMOSU HF yayını

Kullanıcının açık talebiyle yalnız mevcut `0.1.0-demo` yayımlandı: `zulalertrk/se-primer-v2-synthetic-demo`, tam commit `d79adb407da3be479d77fe4a909b932bc1b77a8a`. Model/config/kart/şema tek commit'te yüklendi; dört dosya anonim indirilerek yerel SHA-256 ile karşılaştırıldı. Makbuz `release-demo.json`. Model ve config byte'ları değişmedi, `publishable=false` ve sentetik metrikler korundu. Gerçek model kapısını uygulayan `scripts/publish_model.py` değiştirilmedi. Yeni gerçek eğitim yapılmadı; BA=0.25/recall=0.50 ret kararı geçerlidir.

Web manifesti `hf-pinned-synthetic-demo` moduyla tam HF commit'ine bağlandı. Değişken main dalından indirme yok. `source.json` manifesti yeni yayınların tarayıcı önbelleğinde eski kalmaması için no-store ile okunur; model/config ise sabit commit URL'sinden gelir. Mevcut MP4 aynı `5a08f081cdf16ec82365879e2cad5479575481de0a3eb59e1313a1f8a1982938` SHA-256'lı ONNX modelini gösterdiğinden yeniden çekilmedi.

Demo geri alma: `public/model/source.json` eski Git sürümündeki `local-demo` manifestine geri alınabilir; paketlenmiş model/config byte'ları aynı olduğundan bu yalnız dosya barındırma kaynağını değiştirir. Alternatif olarak doğrulanmış bu HF commit'i korunur. Testler ve normal Pages push sonrası kaynak manifestini doğrulayın. Gerçek model kabulü gibi sunulmaz.

HF web entegrasyonu kaynak commit'i `37cf42be75e2d3ec17bdd12c5c5841147d5a9991`, [başarılı Pages koşusu 42287731950](https://github.com/zulal836/se-primer-v2-2026/actions/runs/42287731950). 15 yerel ve 15 bulut tarayıcı testi, 15 Python testi, beş Python ONNX referansı, build ve 2 girişsiz canlı test geçti. Canlı manifest, HF repo/commit ve model/config'in sentetik durumu anonim doğrulandı. `publication.json` ve `release-demo.json` gerçek yayın makbuzlarıdır.

Son makbuz/belge kaydı da normal push ile yayımlandı: `2fad9376ac16d8a7ef10f805a7436e62f55707ff`, [koşu 42288555958](https://github.com/zulal836/se-primer-v2-2026/actions/runs/42288555958) test/build/deploy başarılı. Uygulama/model/video dosyaları önceki canlı doğrulamayla aynı; güncel yayın makbuzu `publication.json` içindedir.

## Son teslim durumu — eğitim içi seçim sonrası kapı yine geçilmedi

Teslim kaynak commit'i `1fd3e31615e56d153d64fd5ea81d2fd79ec8d6da` normal push ile gönderildi. [Koşu 42281454788](https://github.com/zulal836/se-primer-v2-2026/actions/runs/42281454788): 15 tarayıcı testi, build ve Pages deploy başarılı. Son girişsiz canlı kontrolde 2/2 test geçti (yaklaşık 65 sn); mevcut sentetik ONNX, oyun akışı ve MP4 doğrulandı. Yeni gerçek model yayımlanmış değildir. Kaynak ve test raporları GitHub'da günceldir.

Kullanıcı isteğiyle iki sabit aday, yalnız mevcut dış eğitim oturumlarında beş katlı grup CV ile karşılaştırıldı (`MODEL_SECIMI.md`, ön kayıt commit'i `edb0a9e`). Ortalama CV BA: ağırlıklı lojistik 0.470000, küçük ağaç 0.413333. Tek seçilen lojistik mevcut sabit testte bir kez değerlendirildi: BA=0.25 ve ayrıntılı recall=0.50. Kabul 0.70/0.65 altında; başka modele geçilip test tekrar kullanılmadı. Etiketler, veri, dış test, seed ve eşikler korunmuştur. Sklearn ile web'in eşit olasılık davranışı önceden yazılı p>=0.5 kararıyla tutarlı hâle getirildi.

Gerçek aday yayımlanmadı. Mevcut uygulama/video sentetik demo olarak korunur; nihai HF bağlantısı ve gerçek model videosu eksiktir. HF oturumu yok, ancak kapı geçilmediği için giriş olsa da nihai yayın yapılmaz. 20 tutor değerlendirmesi v2 tesliminin engeli değildir. Hazır linkler ve forma yapıştırılabilecek doğru açıklama `TESLIM.md` içindedir. Aşağıdaki bölümler önceki denemelerin tarihçesidir.

## Güncel CSV sonrası — gerçek aday eğitildi, eval kapısında reddedildi

6 Kasım 2026: beş CSV, 123 kaynak satırı, 24 yinelenen kaynak kaydı; birleşik veri 99 benzersiz karar. Yeni dosya 10 tamamlanmış oturum ve 30 yeni karar ekledi. Toplam 32 tamamlanmış/2 yarım oturum var. Tamamlanmış 96 karardan 49 etiket kullanılabilir (28 kısa/21 ayrıntılı); 47 boş hedef eğitim dışında. Ham dosyalar ve cevaplar korunmuştur.

Sabit seed=42 ve %25 oturum split'iyle gerçek eğitim çalıştı: eğitim 17 oturum (23 kısa/15 ayrıntılı), test 6 oturum (5 kısa/6 ayrıntılı), oturum kesişimi 0. Veri koşulları geçti. Adayın **BA=0.50**, **ayrıntılı recall=0.00**; önceden belirlenen >=0.70 ve >=0.65 eşikleri geçilemedi. Confusion matrix `[[5,0],[6,0]]`: tüm test kararlarına kısa tahmini. `train.py` exit code 1 ile, ONNX dışa aktarma ve paket güncellemesinden önce durdu. Eşik, model seçimi veya seed sonuç geçsin diye değiştirilmedi.

Yeni gerçek ONNX/config, HF yayını, manifest değişikliği veya nihai demo yenilemesi yapılmadı. Mevcut sentetik model ve video korunuyor. Bu belge güncel başarısız adayın kaydıdır; yeni model sürümü değildir. Tanısal olarak kullanılabilir 49 satırda seçenek değiştirme sinyali hep sıfır, ipucu sinyali yalnız dört kararda sıfırdan farklıdır. Daha çeşitli doğal insan davranışlarıyla yeni bağımsız veri gerekir; başarı garanti edilemez. Aşağıdaki bölümler önceki denetimlerin tarihçesidir.

## Dördüncü CSV sonrası — gerçek model kapısı hâlâ geçilmedi

6 Kasım 2026: `primer-oturumlar3.csv`, 24 yeni karar/8 tamamlanmış oturum ekledi. Dört kaynakta 69 benzersiz karar, 22 tamamlanmış ve 2 yarım oturum var; kaynaklar arasında tekrar yok. Tekrar birleştirmede eski 45 karar çift sayılmadı. Tamamlanmış 66 karardan boş hedefler çıkarılınca **19** kullanılabilir yanıt kalıyor: kısa=11, ayrıntılı=8. Boş tamamlanmış hedef sayısı 47; yarım oturumdaki bir etiket de eğitim dışında.

Mevcut `train.py`, her sınıfta en az 10 etiket koşulunda exit code 1 ile fit başlamadan durdu. Aynı seed=42, %25 GroupShuffleSplit ile yapılan bağımsız tanısal kontrolde eğitim sınıfları 5/7, test sınıfları **6/1** bulundu; testte her sınıfta en az beş koşulu da sağlanmıyor. Kesişen oturum yok. Yeni model/metrik üretilmedi; kabul eşikleri ve değerlendirme yöntemi değiştirilmedi. Yeni veri split'i yeniden belirlediği için sadece iki ek etiketin yeterli olacağı söylenemez.

Model, config, manifest, referanslar ve video eğitim denemesinde korunmuştur; yeni gerçek model yayını ve nihai video yapılmadı. Ham CSV'ler private kalır. Güncel makbuzlar `test-results/real-*.json` dosyalarındadır. Aşağıdaki üç CSV sonuçları önceki denetimin tarihçesidir.

## 6 Kasım 2026 gerçek veri kontrolü — nihai yayın yapılmadı

Denetim ve belge güncellemesi normal commit/push ile gönderildi: `b0ce348a6c6724edfe59501a3f3d16b0ad65a91a`. [GitHub Actions koşusu 42272543090](https://github.com/zulal836/se-primer-v2-2026/actions/runs/42272543090) 15 tarayıcı testi, üretim build'i ve Pages dağıtımıyla başarılı tamamlandı. Canlı uygulama ayrıca girişsiz Cypress oturumunda 2/2 test geçti (yaklaşık 13 sn): önceki ONNX artefaktı referanslarla eşleşti, oyun sonu ve MP4 erişimi doğrulandı. Model/config/source manifest ve video hâlâ önceki sentetik sürümdür.

Üç CSV, 45 benzersiz karar ve 16 farklı oturum içeriyor. Kaynak dosyalar arasında yinelenen oturum/karar yok; tekrar birleştirme mevcut 45 kararı çift saymadı. Tamamlanmış oturum sayısı **14**, yarım oturum sayısı **2**. Tamamlanmış 42 kararın hedefleri: kısa=4, ayrıntılı=3, eksik=35. Tüm 45 kararda kısa=4, ayrıntılı=4, eksik=37. Ham dosyalar ve insan yanıtları değişmedi; ham veriler Git'ten hariç.

`train.py` exit code 1 ile, fit/split/model dönüşümü başlamadan durdu: “En az 15 tamamlanmış gerçek oturum gerekli; bulunan: 14”. Balanced accuracy/recall eşikleri, seed=42 ve oturum bazlı %25 split korundu. Yeni gerçek model veya gerçek eval metriği oluşmadı. Model/config/ONNX oracle/demo eğitim denemesinde korunmuştur; hash makbuzu `test-results/real-training-attempt.json` içindedir. Gerçek veriyle eğitim yapılmadığı için eğitim/test sızıntısı oluşmadı; ileride aynı oturumun iki gruba girmemesini mevcut kapı kontrol eder.

HF oturumu yok; giriş komutu `.venv/Scripts/hf.exe auth login`. Veri koşulu da geçilmediğinden HF modeli yayımlanmadı, web manifesti değiştirilmedi ve nihai modelle yeni video çekilmiş gibi gösterilmedi. Mevcut Pages ve MP4 sentetik demo olarak kalıyor. Tutor insan değerlendirmeleri hâlâ bekliyor. Bu bölüm yeni model sürümü değil, veri denetimi ve korunmuş demo sürümünün durum kaydıdır.

Sonraki veri adımı: her üç kararı yardım öncesinde dürüstçe etiketlenmiş yeni tamamlanmış oturumlar. Mevcut beş etiketli oturumla en az sekiz yeni tam etiketli oturum, split/test sınıf sayıları için yalnız kuramsal alt sınırdır; daha fazla veri gerekebilir. Eski boş etiketleri geriye dönük doldurmayın. README veri sayısı gerekçesini içerir.

5 Kasım 2026 · v0.1.0-demo geliştirme adayı. Eski uygulama yoktu; temel oyun sıfırdan kuruldu. Üç karar, iki son, profil uyarlaması, gönüllü veri toplama ve yerel CSV eklendi. Davranış modeli gerçek ONNX dosyasıyla açıklama derinliğini seçer. Temel kural karşılaştırması ve yükleme hatasında yedek vardır.

## Uygulanan / bekleyen

GitHub public proje deposu oluşturuldu: https://github.com/zulal836/se-primer-v2-2026 . İlk kaynak commit'i `869289e8fc2a7d3e5299d93f1671fc45b46943c9`; eğitim öncesi spec commit'i `5e9008e`. İlk Pages workflow koşusunda üçüncü taraf Cypress action'ının sunucu başlatma/bekleme adımı socket hatası verdi. Yerel sunucu başlatma ve hazır olma kontrolünü yapan `scripts/test_e2e.mjs` ile değiştirildi, Ubuntu 24.04 ortamı sabitlendi. Web yayın durumu aşağıda ayrıca doğrulanır.

Model dosyasındaki `data_source=sentetik`, `publishable=false` geliştirme durumunu gösterir. Bu model gerçek veriyle eğitilmiş v2.0 diye yayımlanamaz. Gerçek oturum sayısı başlangıçta 0; insan tutor değerlendirmesi bekliyor. Nihai HF commit'i henüz yoktur. GitHub ve Pages yayın sonuçları doğrulandıktan sonra bu dosyaya gerçek bağlantılar eklenir; `publication.json` otomatik yayın makbuzudur. Bağlantı şablonları gerçek bağlantı diye sunulmaz.

## Doğrulanan ilk web yayını

- Uygulama: https://zulal836.github.io/se-primer-v2-2026/
- Demo MP4: https://zulal836.github.io/se-primer-v2-2026/demo.mp4 (73.040 saniye)
- Yayımlanan web kaynak commit'i: `ebb2b9126714e54e1d26839e652657a903bff246`
- Başarılı test/build/deploy koşusu: https://github.com/zulal836/se-primer-v2-2026/actions/runs/42100198789
- Giriş bilgisi gönderilmeden HTML ve MP4 HTTP 200 doğrulandı. Model SHA-256: `5a08f081cdf16ec82365879e2cad5479575481de0a3eb59e1313a1f8a1982938`; aynı commit'teki yerel dosya ile eşleşiyor. `test-results/public-http.json` makbuzdur.
- Bu, sentetik geliştirme sürümünün web yayınıdır. Nihai gerçek-veri modeli/HF yayını değildir. Gerçek model başarısız olursa bu commit doğrulanmış kural+demo uygulamasına dönüş noktasıdır.
- Canlı sitede giriş yapılmamış Cypress oturumunda 2/2 test geçti: gerçek ONNX ile beş olasılık karşılaştırması, üç kararla oyun sonu ve public MP4. İlk yükleme büyük WASM dosyası nedeniyle onlarca saniye sürebilir; hazır olana kadar kural yedeği görünür.

## Mimari seçeneklerin karşılaştırması

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
