# Veri sözlüğü

UTF-8 CSV, virgülle ayrılır. Her satır bir karardır. Gerçek veri dosyası başlangıçta yalnız başlıktır. `sentetik.csv` geliştirme verisidir, gerçek dosyaya kopyalanmaz.

| Sütun | Anlam / birim / sınır |
|---|---|
| oturum_id | Tarayıcı crypto.randomUUID; yeni oyunda yeni kimlik. Kişi sayısı değildir. |
| karar_no | 1, 2, 3 |
| bekleme_sn | Sahnenin açılmasından gönderimine kadar saniye, 0–300; sekme arka plandaysa süre artabilir |
| degistirme_sayisi | İlk işaretlemeden sonraki farklı seçeneğe geçiş, 0–20 |
| ipucu_sayisi | Bu kararda ipucu düğmesine basma sayısı, 0–10 |
| ayrinti_istegi | Model yardımı görülmeden istenen derinlik: 0 kısa, 1 ayrıntı; boş: yanıt yok, eğitim dışı |
| secim | 0 veya 1; eğitim girdisi değildir |
| seviye | yeni / deneyimli; eğitim girdisi değildir |
| rol | Geliştirici / Test mühendisi / Teknik lider |
| hedef | Güvenli sürüm / Test stratejisi / Veri gizliliği |
| kaynak | gerçek / sentetik; karıştırılmaz |
| tamamlandi | Aynı oturumdaki üç karar bittiyse 1, aksi halde 0 |

Katılım gönüllüdür. Katılmayanın kaydı yoktur. Etiket öz bildirimdir; doğru cevap, gelecekteki başarı veya doğrulanmış insan gereksinimi yerine geçmez. Oyuncudan özel bilgi istenmez. Zaman damgası, IP, cihaz kimliği ve kişi kimliği yoktur. Üç kişinin beşer oyunu mümkündür; kişi sayısı teknik kimlik takibiyle kanıtlanmaz, organizatör anonim toplamı ayrıca doğrular.

Telefonda üç kararı tamamlayıp CSV indir'e basın; indirdiğiniz dosyayı organizatöre isteyerek iletin. Organizatör dosyaları `private-data/` altında tutup `python scripts/merge_csv.py private-data/oyun1.csv private-data/oyun2.csv` çalıştırır. Aynı satır yeniden eklenmez, çelişen kayıt reddedilir. Tamamlanmamış eski dışa aktarımlar tamamlanmış sürümle güncellenir. Özel bilgi yazılmış bir dosyayı paylaşmayın. Yerel kayıtlar “Yerel veriyi temizle” ile silinir; daha önce paylaşılan kopyalar için organizatörden silme istenir. Ham oturum verisini public depoya yüklemeyin; nihai yayın betiği veri dosyasını içermez.
