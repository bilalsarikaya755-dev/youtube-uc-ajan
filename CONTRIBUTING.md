# Katkı rehberi

Bu proje, araştırmadan Türkçe video senaryosu ve çekim planı oluşturmak için
geliştirilen erken aşama bir Python aracıdır.

## İlk katkı

1. README'deki ücretsiz demoyu kendi bilgisayarında çalıştır.
2. Mevcut testleri çalıştır: `python -m unittest discover -s tests -v`.
3. Hata bildiriminde işletim sistemini, Python sürümünü, kullandığın komutu,
   beklenen sonucu ve kişisel bilgilerden arındırılmış hata mesajını paylaş.
4. Değişikliğin hangi sorunu çözdüğünü açıklayan küçük bir pull request aç.
5. Davranışı değiştiriyorsan o davranışı kontrol eden anlamlı bir test ekle.

Canlı sağlayıcı testini yapmadıysan yaptığını iddia etme. Demo sonucunu canlı
araştırma veya model çalıştırması olarak sunma.

## Öncelikli geliştirme işleri

- Windows'ta temiz kurulumun bağımsız bir kullanıcı tarafından doğrulanması.
- Kullanıcının kendi sağlayıcı hesabıyla canlı akışın denenmesi; tarih,
  model ve sürüm bilgilerinin kaydı.
- Yarım kalan akışa daha önce tamamlanmış aşamalardan devam edebilme.
- Örnek çıktıların farklı konular ve sürelerle genişletilmesi.
- Kullanıcıların bildirdiği somut hataların yeniden üretilip düzeltilmesi.

## Anahtarlar ve veriler

API anahtarlarını, gerçek `.env` dosyalarını, özel mesajları veya kişisel
verileri depoya ve hata kayıtlarına ekleme. `.env.example` sadece alan adlarını
ve örnek ayarları gösterir.

MIT lisanslı bu projeye katkıların da MIT lisansıyla paylaşılır. Bağımlılıkların
kendi lisansları geçerlidir.

## Çıktıların kontrolü

Şema kontrolleri, kaynak kimliği ilişkileri ve süre toplamı denetimleri olguların
gerçekliğini kanıtlamaz. Yayınlanacak içeriği ve kaynakların kapsamını bir kişi
ayrıca incelemelidir.

