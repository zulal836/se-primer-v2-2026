import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
items=[
('Mimari','Hemen eski sürüme mi döneyim?','Geri dönmeden önce mevcut şemanın eski kodla uyumunu nasıl kontrol edersin?'),
('Mimari','Yama küçük; canlıda denerim.','Değişiklik küçük olsa bile etkilenen yazmaların sınırını nasıl belirlersin?'),
('Mimari','Geri alma her şeyi düzeltir.','Kod geri döndüğünde daha önce yazılmış çift rezervasyonlara ne olur?'),
('Mimari','Veritabanı migrasyonu geri alınamıyor.','Geri döndürülemeyen veri değişiminde hangi uyumluluk kanıtına ihtiyaç duyarsın?'),
('Mimari','Tüm trafiği açsak?','Küçük bir kullanıcı grubunda hangi belirtiyi görürsen dağıtımı durdurursun?'),
('Mimari','Sistem ayağa kalktı, bitti.','Sistemin çalışması ile tutarsız verinin düzelmesi aynı kanıtla gösterilebilir mi?'),
('Test','Tek kullanıcı testi geçti.','İki istek aynı anda boş saati okursa bu test hangi davranışı gözden kaçırır?'),
('Test','Eski testlere gerek var mı?','Yeni düzeltme iptal ve yeniden rezervasyon akışını değiştirirse bunu nasıl fark edersin?'),
('Test','Python ve web aynı, model doğru.','İki uygulama ortak bir hatayı taşıyorsa aynı sonuç neyi kanıtlayamaz?'),
('Test','Fark 0.00013, az değil mi?','Önceden yazdığın tolerans sınırıyla bu farkı nasıl karşılaştırırsın?'),
('Test','Etiket girişe eklense başarı artar.','Tahmin anında oyuncunun yardım ihtiyacı zaten biliniyorsa model hangi problemi çözüyor olur?'),
('Test','Satırları rastgele böleyim.','Aynı oyuncu oturumunun başka kararları iki bölümdeyse ne tür bağımlılık oluşur?'),
('Test','Sentetik doğruluk çok iyi.','Kurguladığın ilişkiyi öğrenmek ile gerçek insan ihtiyacına uymak nasıl ayrılır?'),
('Test','Model başarısız, eşiği düşürelim.','Sonuçtan önce koyduğun kabul ölçütünü değiştirmek hangi iddiayı zayıflatır?'),
('Gizlilik','Logu olduğu gibi göndereyim.','Hatayı yeniden üretmek için kayıttaki hangi alanlar gerçekten gerekli?'),
('Gizlilik','Sadece ekip görecek.','Paylaşımın kapsamı küçük olsa bile kişisel alanları taşımak gerekli mi?'),
('Gizlilik','İsimleri silmek yeter.','Kalan alanlar bir araya gelince bir kişiyi yeniden tanımlamak mümkün mü?'),
('Gizlilik','Herkes veri toplamaya katılsın.','Katılmayan birinin aynı oyunu veri bırakmadan oynamasını nasıl sağlarsın?'),
('Gizlilik','Oturum kimliği kişinin kimliği mi?','Her oyunda yeni rastgele kimlik üretildiğinde kaç farklı insan oynadığını anlayabilir misin?'),
('Gizlilik','Model tarayıcıda gizlidir.','Kullanıcının cihazına indirilen dosyayı o kullanıcıdan saklayabilir misin?')]
with (ROOT/'eval/tutor_eval.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.writer(f);w.writerow(['id','konu','oyuncu_ifadesi','tutor_yaniti','cevabi_soyluyor','teknik_hata','soru_yararli','durum','not'])
    for i,(topic,prompt,answer) in enumerate(items,1):w.writerow([i,topic,prompt,answer,'','','','bekliyor','Taslak sabit metin; insan değerlendirmesi yok'])
print('20 tutor değerlendirme örneği hazır; insan puanları boş.')
