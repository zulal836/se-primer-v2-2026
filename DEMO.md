# 75 saniyelik demo akışı

HF barındırmasına geçişte video yeniden çekilmedi: yayımlanan `0.1.0-demo` ONNX SHA-256'sı `5a08f081cdf16ec82365879e2cad5479575481de0a3eb59e1313a1f8a1982938`, videoda kullanılan dosyayla aynıdır. Yalnız dosyanın indirme kaynağı sabit HF commit'i `d79adb407da3be479d77fe4a909b932bc1b77a8a` oldu. Mevcut MP4 byte'larının değişmediği `test-results/hf-demo-checks.json` içinde doğrulandı. Video sentetik demo olarak sunulur; gerçek model kabulünü göstermez.

Gerçek tarayıcı kaydı oluşturuldu: `public/demo.mp4`. MP4 süresi **73.040 saniye**, `python scripts/video_info.py` ile doğrulandı. Cypress ile otomatik oynatılan iki davranışı gösterir; insan oturumu değildir ve gerçek veri sayılmaz. Test akışı 70.85 saniye sürdü. Seslendirme yoktur; açıklamalar uygulama ekranındadır. Nihai gerçek-veri modelinin demosu değildir; sentetik demo etiketi görünür. Aşağıdaki tablo çekim için başlangıç planıdır; gerçekleşen kayıtta aynı güvenli seçenek kısa ve ayrıntılı yardım koşullarında kullanılmıştır.

| Süre | Ekran / anlatım |
|---|---|
| 0–10 sn | Başlık ve “sentetik demo” durumunu göster. “Bu bir eğitim oyunu; model henüz gerçek oturumlarla doğrulanmadı.” |
| 10–25 sn | Deneyimliyim, Geliştirici, Güvenli sürüm. Katılımı kapalı tut. Model modunda ilk sahneye gir; doğrudan A'yı seçip gönder. Kısa ipucu ve gerçek ONNX olasılığını göster. |
| 25–40 sn | Yeni oturum. Aynı sahnede A/B arasında en az beş kez değiştir; ipucuna üç kez bas. İhtiyacını kendin bildir ve gönder. Ayrıntılı açıklama ile olasılığı göster. |
| 40–55 sn | Diğer iki güvenli kararı tamamla. Teknik nedenler ve kontrollü toparlanma sonunu göster. |
| 55–65 sn | Yeni oturumda kural modunu ve açık katılım seçeneğini göster. Kayıt alanlarının kimlik içermediğini açıkla. |
| 65–75 sn | CSV indir, test raporu ve Python/tarayıcı farkını göster. Gerçek veri, HF yayın ve video teslim durumunu dürüstçe söyle. |

İlk oyuncu gönderimi uzarsa bekleme süresi kısa yardım kararını değiştirebilir; ilk sahneyi hızlı geçin. İkinci davranışta değişim ve ipucu yeterli ayrıntı sinyalidir. Sesli 60–90 saniye ekran kaydını giriş gerektirmeyen bir bağlantıya koyun. Gerçek katılımcı kayıtlarını videoda açmayın.
