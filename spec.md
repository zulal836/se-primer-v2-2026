# Son Boş Randevu — eğitim öncesi sözleşme

Sürüm: 0.1 · 5 Kasım 2026. Bu dosya ilk eğitim çalıştırılmadan yazılmıştır.

## Problem ve kapsam
Yeni sürüm hastane randevularında çift rezervasyon üretiyor. Oyuncu nöbetçi yazılım ekibinde üç karar verir: yazmayı durdurup uyumlu sürüme dönüş, eşzamanlılık testi, kişisel veri içermeyen olay kaydı. Tüm isimler ve olaylar kurgudur. Üç giriş sorusu seviye, rol ve öğrenme hedefidir. Sekiz yol, iki son: üç güvenli seçimde kontrollü toparlanma; diğerlerinde olay incelemesi. Her seçimin teknik sonucu açıklanır. Tutor insan tarafından doğrulanmayı bekleyen sabit Sokratik sorulardır; LLM çağrısı yoktur.

## Model gereksinimi
Tek karar: kısa ipucu (0) veya ayrıntılı açıklama (1). Hedef, kararı göndermeden önce oyuncunun “Bu anda ne kadar açıklama istersin?” yanıtıdır. Yanıt inference girdisi değildir. Oyuncu önce yalnız senaryo ve seçenekleri görür, seçeneği işaretleyip isteğini bildirir; model çıktısı ancak gönderimden sonra gösterilir. Eğitim için davranış ölçümü bu anda dondurulur. Bu etiket öz bildirime dayanır; öğrenme başarısı ölçmez.

Girdiler float32 sırasıyla: `bekleme_sn` (0–300), `degistirme_sayisi` (0–20), `ipucu_sayisi` (0–10). Yalnız mevcut karar öncesi sayımlar; gelecek karar, doğru/yanlış seçimi veya etiket girdi olamaz. Lojistik regresyon ve standart ölçekleme, sabit tohum 42. Eşik p(ayrıntılı) >= 0.5. Kural karşılaştırması: yeni başlayan veya o kararda ipucu isteyen ayrıntılı yardım alır.

## Eval kapısı (sonuçlara göre değiştirilemez)
Oturum bazlı %25 test ayırımı, random_state=42. Birincil metrik balanced accuracy >= 0.70; açıklama sınıfı recall >= 0.65; her sınıf testte en az 5 örnek. Dengeli doğruluk çoğunluk sınıfına sürekli kısa deme hilesini önler; recall ihtiyaç bildirenleri kaçırmayı sınırlar. Küçük veri güven aralığı geniştir; değerler eğitim başarısı garantisi değildir. En az 15 tamamlanmış gerçek oturum (her biri üç karar), iki sınıfın her birinde en az 10 örnek gerekir. Sentetik demo ayrı kaynakla aynı kapıdan geçer fakat nihai yayına uygun sayılmaz. Split'te aynı oturum bulunamaz. Eşik altı çalışma mevcut artefaktları değiştirmeden hata ile durur. ONNX/sklearn farkı <=1e-4, tarayıcı/Python farkı <1e-4 olmalı.

## Temel oyunun beş kabul örneği
1. Üç profil sorusu yanıtlanır; rol ve hedef sahnede görünür, seviyeye göre anlatım değişir.
2. Güvenli üç seçim kontrollü toparlanmaya ulaşır; her kararın nedeni görünür.
3. Sekiz yoldan kalan yedisi olay incelemesine ulaşır; yeniden başlatma seçimleri ve kimliği yeniler.
4. Katılım yoksa CSV'ye satır eklenmez; açık katılımda üç karar aynı rastgele kimlik altında, kaynak=gerçek kaydolur.
5. Model indirilemezse görünür kural modu ile oyun tamamlanır; kişisel bilgi alanı bulunmaz.

## Modele eklenen üç kabul örneği
1. Aynı sahnede [2,0,0] ve [100,5,3] girdilerinde gerçek ONNX farklı açıklama kararları verir (demo doğrulaması); kısa ve ayrıntılı metin DOM'da gözlenir.
2. Beş Python ONNX oracle girdisi tarayıcıda aynı dosyayla <1e-4 mutlak toleransla eşleşir; taklit çıkarım kullanılamaz.
3. Yetersiz veri veya kabul eşiği altındaki çalışma sıfır olmayan kodla durur; önceki model hash'i değişmez. Gerçek veri olmadan nihai yayın reddedilir.

## Kapsam dışı
Hesap/giriş, gerçek hasta bilgisi, mobil/Rails, ikinci bölüm, ücretli API, klinik karar ve öğrenci başarısını puanlama.
