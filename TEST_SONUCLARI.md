# Gerçekte çalıştırılan kontroller

5 Kasım 2026, Windows 11 · Node 24.20.0 · Python 3.12.10 · Cypress 15.21.1 / Electron 138. Model verisi yalnız sentetik; gerçek oturumlar 0. İnsan tutor incelemesi yapılmadı.

| Kontrol | Gerçek sonuç |
|---|---|
| Model öncesi temel oyun `npm run test:base` | 11/11 geçti; artefakt henüz yokken çalıştırıldı |
| ONNX sonrası tüm Cypress suite | 15/15 geçti: 12 oyun, 3 model/parite testi |
| Üretim build'i, localhost:5175 | 15/15 geçti; tarayıcı gerçek WASM+ONNX kullandı |
| Python `unittest discover` | 6/6 geçti |
| Python `tests/parite.py` | 5/5 referans girdisi geçti, mutlak hata <1e-4 |
| `train.py --demo` | Eval kapısı geçti; balanced accuracy 0.9260651629, ayrıntılı recall 0.9047619048 |
| sklearn/ONNX en büyük fark, tüm 480 sentetik karar | 1.0823183327e-7, sınır 1e-4 |
| Eğitim tekrarı | Sabit ONNX graph adıyla model, config, oracle dosyaları bayt düzeyinde aynı |
| `npm run build -- --base=./` | Başarılı, Vite 6.4.5; WASM 11.9 MB, uygulama JS yaklaşık 82 KB |
| `npm audit --audit-level=moderate` | 0 güvenlik açığı |
| Gerçek tarayıcı demo kaydı | Cypress otomatik oynatımı 70.85 saniye; kısa/ayrıntılı ONNX kararları ve oyun sonu doğrulandı; public/demo.mp4 |
| GitHub Actions / Ubuntu 24.04 | 15 tarayıcı testi, build ve Pages deploy başarılı; koşu 42100198789 |
| Canlı HTTP, kimlik bilgisi gönderilmeden | HTML 200, model SHA-256 aynı, MP4 HEAD 200; MP4 süresi 73.040 sn |
| Canlı sitede yeni Cypress tarayıcı oturumu | 2/2 geçti: gerçek ONNX ile beş referans girdisi, üç karar ve iyi son; public MP4. Son koşu 48 sn |

Python testleri şunları doğrular: boş gerçek veri eğitimi reddedilir ve önceki model korunur; sentetik model nihai yayına kabul edilmez; oturum split'i kesişmez; bağımsız gürültülü etiketler eval kapısında durur ve model korunur; CSV yinelenmez, tamamlanma güncellenir ve çelişki reddedilir; tek sınıf/karışık kaynak reddedilir.

Tarayıcı suite sekiz yolu, iki sonu, rol/hedef anlatımını, katılım olmadan kayıt yapılmamasını, CSV'yi, yeni kimliği, temizlemeyi, yükleme hatasında kural yedeğini, beş sayısal parite girdisini ve gerçek model yardım değişimini sınar. `test-results/browser-parity.json` gerçek ölçülen farkları, `test-results/reproducibility.json` hash karşılaştırmasını saklar. Cypress'in geçici yerel kayıtları test girdileridir; gerçek veri dosyasına eklenmedi.

İlk model sonrası tarayıcı koşusu Vite'ın public mjs import sınırı nedeniyle başarısız oldu. WASM-only paket ve Vite `?url` ile düzeltildi; başarı sonuçları düzeltmeden sonraki koşulara aittir. İlk tekrar denemesinde ONNX'in otomatik rastgele graph adı dosya hash'ini değiştirdi; sabit graph adıyla giderildi. Sonuçları geçsin diye metrik eşiği değiştirilmedi. SciPy'nin `iprint` seçenek uyarısı hesaplanan metrikleri veya testleri başarısız kılmadı; tam bağımlılık sürümleri requirements-lock.txt içinde.

Canlı tarayıcının ilk koşusu 60 sn yükleme sınırında kaldı; ilk WASM indirmesine 180 sn sınırı tanınan ikinci koşu 48 sn'de 2/2 geçti. Çıkarım taklit edilmedi. İlk yüklemede yaklaşık 12 MB WASM indirilir; model hazır olana kadar oyun görünür kural yedeğiyle çalışabilir.

Henüz doğrulanmayanlar: gerçek kullanıcı ihtiyacına genelleme, insan tutor puanları, nihai HF commit'i ve gerçek dağıtımda Shadow/Canary. Yerel ağdan fiziksel telefon erişimi ayrıca denenmedi; mobil viewport 390×844 ve demo 430×932 ile tarayıcıda sınandı. Yayın ve demo kayıt sonuçları RELEASE.md/DEMO.md içindedir.
