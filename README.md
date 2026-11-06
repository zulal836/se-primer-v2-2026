# SE Primer v2 — Son Boş Randevu

[Oyunu aç](https://zulal836.github.io/se-primer-v2-2026/) · [73 saniyelik demo video](https://zulal836.github.io/se-primer-v2-2026/demo.mp4) · [GitHub kaynak kodu](https://github.com/zulal836/se-primer-v2-2026)

[Commit'e sabit HF SENTETİK DEMO modeli](https://huggingface.co/zulalertrk/se-primer-v2-synthetic-demo/resolve/d79adb407da3be479d77fe4a909b932bc1b77a8a/model.onnx). Model/config/kart aynı commit'te; gerçek model kabul edilmedi, `publishable=false` korunuyor. Web aynı sabit HF commit'inden indirir. 0.1.0-demo sentetik metrikleri BA=0.9260651629, recall=0.9047619048; **bunlar gerçek kullanıcı başarımı değildir**. Gerçek adayın BA=0.25/recall=0.50 ret sonucu aşağıda ve TESLIM.md'de açıkça kayıtlıdır.

Türkçe, telefona uyumlu üç kararlı yazılım mühendisliği oyunu. Çift rezervasyon olayında sürüm geri alma, eşzamanlılık testi ve kişisel veriyi koruma ele alınır. Üç profil sorusu anlatımı uyarlar. Kural modu ile gerçek ONNX kullanan davranış modeli karşılaştırılabilir. Sunucu, kullanıcı hesabı veya ücretli API gerekmez.

**Son teslim durumu — 6 Kasım 2026:** 32 tamamlanmış oturumdan 49 gerçek etiket kullanıldı (28 kısa/21 ayrıntılı). Eğitim oturumlarında beş katlı CV ile iki sabit aday karşılaştırıldı: ağırlıklı lojistik BA=0.470, küçük ağaç BA=0.413. Yalnız CV ile seçilen lojistik mevcut sabit testte bir kez değerlendirildi: **BA=0.25, ayrıntılı recall=0.50**; gerekli **0.70/0.65** kapısı geçilmedi. Nihai gerçek model yayımlanmadı; canlı uygulama ve 73 saniyelik video açıkça **sentetik demo** olarak korunuyor. Eşikler, seed, dış test ve cevaplar değiştirilmedi. Sonuçlar `test-results/final-model-selection.json`, yöntem `MODEL_SECIMI.md`, hazır bağlantılar/forma yazılacak açıklama **[TESLIM.md](TESLIM.md)** içinde. Önceki ödevin 20 tutor değerlendirmesi bu v2 teslimini engelleyen koşul değildir.

## Başlangıç: en fazla üç komut (Windows PowerShell)

Node 22+ ve Python 3.12 kurulu olmalı. Proje klasöründe:

```powershell
node scripts/setup.mjs
npm run dev
```

Bilgisayarda http://localhost:5173 açılır. Telefon aynı Wi-Fi'deyken Vite'ın terminalde verdiği Network adresini kullanır. Yerel ağ erişimi cihaz/güvenlik duvarı koşullarına bağlıdır; bu proje sistem ayarlarını değiştirmez. HTTPS public yayın, telefon paylaşımını kolaylaştırır. Sayfa yalnız yerel depolama kullanır, arka uca veri göndermez. Tarayıcı gizli modda da oyun çalışır, pencere kapanınca yerel kayıtlar silinebilir.

Linux/macOS: `python3 -m venv .venv` sonrasında `.venv/bin/python -m pip install -r requirements.txt`, `npm ci`, `node scripts/copy_runtime.mjs`; model hazır değilse `.venv/bin/python scripts/generate_demo.py` ve `.venv/bin/python train.py --demo`. Windows yolu `.venv/Scripts/python.exe` biçimindedir.

## Veri toplama

Girişte açık katılım seçeneği var; katılmadan oynanabilir. Her sahnede model sonucu görülmeden kısa/ayrıntılı açıklama isteği sorulur. Yanıt vermemek mümkündür; boş etiket eğitim dışıdır. Süre, seçenek değiştirme ve ipucu isteme yalnız o kararda ölçülür. Model geri bildirim yanıtını, seçimin doğruluğunu veya geleceği girdi almaz.

En az **15 tamamlanmış gerçek oturum** toplayın (ör. üç gönüllü × beş oyun). Her oyun üç karar ve yeni rastgele kimlik üretir. Oturum sayısı kişi sayısı değildir; aynı insan iki eval grubunda olabilir. Bu sınırlama model kartında yazılıdır. Oyun bitince telefondan CSV indirilir. Her cihazın CSV'sini `private-data/` içine koyun:

```powershell
.venv/Scripts/python.exe scripts/merge_csv.py private-data/oyun1.csv private-data/oyun2.csv
.venv/Scripts/python.exe train.py
```

Eğitim varsayılan olarak yalnız `data/oturumlar.csv` gerçek verisini okur. Başlangıç dosyası boştu; şimdi yalnız kullanıcının sağladığı CSV'lerden birleştirilen gerçek kayıtları içeriyor ve Git'ten hariç tutuluyor. Ham dosyalar ve cevaplar değiştirilmedi. `python scripts/audit_real_data.py` CSV'leri doğrular ve aynı oturum/kararı çift saymadan mevcut birleştiriciyle birleştirir. Public raporda yalnız toplamlar bulunur. Veri sözlüğü, saklama/silme ve birleştirme ayrıntıları `data/SOZLUK.md` içindedir. Kimlik ya da hasta verisi toplamayın. Toplanan gerçek CSV'yi public depoya göndermeyin.

**Teslim kararı:** Yeni veri beklemeden mevcut çalışan demo ve başarısız gerçek model sonuçlarıyla dosyalar tamamlandı. Kabul kapısı gevşetilmedi; test sonucuna göre başka aday denenmedi. Nihai gerçek model/HF/gerçek model videosu eksikleri TESLIM.md dosyasında açıkça listelenir. 20 tutor değerlendirmesi teslim/yayın kapısı değildir.

## Eğitim ve sözleşme

`spec.md` eğitimden önce yazıldı: balanced accuracy >=0.70, ayrıntılı sınıf recall >=0.65. Sabit seed=42 ile oturum bazında %25 test ayrılır. Aynı oturum iki tarafta bulunmaz. Her sınıfın testte en az beş örneği gerekir. Kapı başarısızsa önceki artefakt korunur. Yetersiz veriyle eşik düşürmek yerine veri toplanır ve sorun araştırılır.

Model: StandardScaler → LogisticRegression. Girdi `features`, float32 `[n,3]`; sıra bekleme_sn, degistirme_sayisi, ipucu_sayisi. Çıkış `probabilities` `[n,2]`; sınıf sırası kısa, ayrıntılı. p>=0.5 ise ayrıntılı yardım. `config.json` özellikler, tipler, sınıflar, metrikler, eşikler, split ve SHA-256 içerir; JSON şeması eğitimde doğrulanır. `model/README.md` model kartıdır. Python sklearn/ONNX farkı 1e-4'ü aşarsa eğitim durur.

Sentetik geliştirme için ayrı komutlar:

```powershell
.venv/Scripts/python.exe scripts/generate_demo.py
.venv/Scripts/python.exe train.py --demo
```

Üretici seed=42, 160 kurgusal oturum, her biri üç karar. Süre 1–130 saniye, değişim 0–6, ipucu 0–3; gizli skor `süre/65 + değişim/2 + ipucu*0.9 > 3.8`, %8 etiket gürültüsü. Bu, insan ihtiyacının ölçülmesi değildir. Geliştirme modeli `publishable=false` işaretlenir. `train.py` aynı veri ve ortamda aynı split ve metrikleri üretir. Tekrarlanabilir tam ortam için kurulumdan sonra alınan `requirements-lock.txt` de mevcuttur.

## Doğrulama

Vite çalışırken:

```powershell
.venv/Scripts/python.exe -m unittest discover -s tests -p "test_*.py"
.venv/Scripts/python.exe tests/parite.py
npm run test:e2e
npm run build -- --base=./
```

Temel oyun testleri model üretilmeden önce `npm run test:base` ile çalıştırılır, modelden sonra tüm suite regresyon olarak tekrar çalıştırılır. Sekiz yol, iki son, profil, katılım, yeniden başlatma, CSV, yerel silme ve yükleme hatasında yedek test edilir. Python oracle beş sabit girdinin gerçek ONNX olasılıklarını verir; Cypress aynı gerçek dosyada toleransı kontrol eder. Model yardım derinliğini DOM üzerinde değiştirmelidir. Test yüzeyi `window.primer.predict` yalnız gerçek üretim çıkarımını çağırır. Model testinde inference taklidi yoktur; yedek testinde yalnız başarısız indirme simüle edilir.

Tutor sabit Sokratik metinlerden oluşur, LLM çıktısı diye sunulmaz. `eval/tutor_eval.csv` 20 değerlendirme örneği ve boş insan etiketlerini içerir. Henüz insan başarım oranı hesaplanmamıştır. `SINAV_TASARIMI.md` ayrı klasik vize sorusudur; oyuna eklenmez. `DEMO.md` gerçek demo kaydı ve çekim planının ayrıntılarını içerir.

## Yayın

### Sentetik geliştirme demosu için ayrı HF komutu

Kullanıcı son teslimde **mevcut 0.1.0-demo sentetik modelin**, açıkça demo etiketiyle ayrı public HF deposuna yüklenmesini ayrıca yetkilendirdi. Bu, gerçek model kabulü değildir. `publishable=false`, gerçek model kapısı ve config'teki sentetik metrikler değiştirilmez. Sadece model/kart/config/şema yüklenir; ham oyuncu verisi yüklenmez.

```powershell
.venv/Scripts/hf.exe auth login
.venv/Scripts/python.exe scripts/publish_demo.py --push
```

`publish_demo.py` yalnız sentetik 0.1.0-demo kabul eder; yeni `kullanıcı/se-primer-v2-synthetic-demo` deposuna dosyaları tek commit'te yükler, anonim indirmelerin hash'lerini doğrular, web manifestini tam commit'e sabitler ve `release-demo.json` makbuzunu yazar. Yeni gerçek model eğitimi yapmaz. Mevcut video aynı ONNX SHA-256'yı gösterdiğinden yeniden çekilmez. HF demo bağlantısı oluştuğunda TESLIM.md'de **HF DEMO** olarak listelenir; gerçek modelin BA=0.25/recall=0.50 sonucu ve kabul edilmediği bilgisi korunur.

### Nihai gerçek model için ayrı ve değişmeyen kapı

Hesap erişimiyle yeni GitHub public reposu oluşturup bu klasörü main dalına gönderin; Settings → Pages → GitHub Actions seçin. `.github/workflows/pages.yml` gerçek Cypress testlerinden sonra ücretsiz Pages yayını yapar. Ortak dizin altında çalışabilmesi için build `--base=./` kullanır. Repo kurulumu otomasyonu `scripts/publish_github.py` içindedir.

Gerçek veri modeli kapıyı geçtikten sonra:

```powershell
.venv/Scripts/hf.exe auth login
.venv/Scripts/python.exe scripts/publish_model.py KULLANICI/YENI_PRIMER_MODEL --push
```

Betik mevcut depoları değiştirmez; yeni public HF reposu açar, model+config aynı commit'te yüklenir, indirilen içerikler doğrulanır. Manifestte 40 haneli commit sabitlenir; web değişken main URL'sini kullanmaz. Mevcut sentetik demo artık sabit HF commit kaynağından indiriliyor; yerel paket aynı dosyanın kopyasını içerir. Model indirme başarısızsa durum görünür ve kural yedeği oyunu sürdürür. HF sonrası parite/build çalıştırıp yeni web sürümünü yayınlayın. Rollout ve geri alma `RELEASE.md` içindedir.

Teslim için dört gerçek bağlantı: GitHub reposu, commit'e sabit HF modeli, girişsiz uygulama, 60–90 sn demo video. Form kullanıcı tarafından gönderilir.

## Ürün kararları

- Native mobil yapılmadı: tek web uygulaması dersin uçtan uca çıkarım koşulunu karşılıyor.
- Serbest sohbet eklenmedi: sabit Sokratik sorular, ücretsiz ve denetlenebilir bir tutor sağlıyor.
- Sunucu ve hesap eklenmedi: davranış verisi cihazda kalıyor, kurulum ve gizlilik yükü azalıyor.

## İncelenen kaynaklar

- [Başlangıç reposu README ve AGENTS](https://github.com/seyyah/huggingface-hello-web): sözleşme, yerel eğitim, model paketleme. `hf_cli.py` içindeki `onnx_aktar` ve `web/index.html` incelendi; zipmap=false olasılık tensörü ve sklearn/ONNX tolerans kontrolü yaklaşımından yararlanıldı. Bu projede bağımsız üç özellik, seed=42 ve `features` girdi adı kullanılıyor; tüm tüketiciler buna uyarlanmıştır. Mobil/Rails/diyabet verisi taşınmadı.
- [ONNX Runtime Web deployment](https://onnxruntime.ai/docs/tutorials/web/deploy.html): WASM dosyaları npm sürümüyle birlikte yerelden sunulur; CDN sürüm uyuşmazlığı önlenir.
- [scikit-learn GroupShuffleSplit](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupShuffleSplit.html): oturumları gruplar halinde ayırma. StandardScaler yalnız eğitim bölümünde fit edilir.
- [Hugging Face Hub upload](https://huggingface.co/docs/huggingface_hub/guides/upload): dosyaları tek commit'te yükleme ve commit'ten indirme.
- [Model Cards for Model Reporting, Mitchell vd. 2019](https://arxiv.org/abs/1810.03993): amaç, değerlendirme ve kullanım sınırlarını görünür kılan model kartı yapısı.

## AI araç kullanımı beyanı

1. OpenAI Codex; oyun, spec ve veri toplama akışının ilk sürümünü oluşturdu.
2. Codex; eğitim, ONNX, yayın betikleri ve testleri yazıp komutlarla doğruladı; gerçek sonuçlar test raporunda yer alır.
3. Codex; belgeler, tutor değerlendirme taslağı ve demo planını hazırladı. Tutor metinleri üretim sırasında LLM ile oluşturulmaz.
4. Gerçek CSV'leri kullanıcı sağladı; Codex bunları denetleyip çift saymadan birleştirdi. İnsan yanıtları değiştirilmedi. Yeterli yeni etiketli oturumlar ve tutor insan incelemesi beklemektedir.





