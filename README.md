# Paylaşımlı Ledger Sistemi

## Sorun
Monorepo içindeki her uygulama için ayrı ledger sistemi yazmam gerekiyordu. Bu da kod tekrarına ve aynı operasyonların farklı uygulamalarda tekrar yazılmasına sebep oluyordu.

## Çözüm
Merkezi bir ledger servisi oluşturup, tüm isteklere `app_id` parametresi ekleyerek çözdüm.

## Bu Çözümün Sağladıkları:
- Her şeyi tek bir serviste topladım 
- Her uygulama kendi kredilerini `app_id` ile takip edebiliyor
- Kod tekrarını önledim
- Bakiye ve işlem mantığını tek noktada yönettim

Bu basit yaklaşım ile karmaşık inheritance ve type-safety problemlerini sadece `app_id` parametresi ekleyerek çözmüş oldum.