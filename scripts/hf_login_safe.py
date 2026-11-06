"""Tek kimlik isteğiyle, token'ı göstermeden açık hata veren yerel HF girişi."""
import getpass
import sys
import requests
from huggingface_hub import HfFolder, constants

def main():
    token=getpass.getpass('HF WRITE token (gizli): ').strip()
    if not token.startswith('hf_') or not token.isascii() or any(c.isspace() for c in token):
        sys.exit('Kaydedilmedi: hf_ ile başlayan token değerinin kendisini yapıştırın; adını/URL/Bearer önekini/tırnakları değil. Token gösterilmedi.')
    try:
        response=requests.get('https://huggingface.co/api/whoami-v2',headers={'Authorization':'Bearer '+token,'User-Agent':'se-primer-v2-login'},timeout=30)
    except requests.RequestException:
        sys.exit('Kaydedilmedi: HF bağlantısı kurulamadı. Token gösterilmedi; otomatik tekrar yok.')
    if response.status_code!=200:
        sys.exit(f'Kaydedilmedi: HF kimlik doğrulama HTTP {response.status_code}. Token geçerliliği/hesap erişimi doğrulanamadı. Token gösterilmedi; otomatik tekrar yok.')
    account=response.json()
    role=account.get('auth',{}).get('accessToken',{}).get('role')
    if role=='read':
        sys.exit('Kaydedilmedi: token salt okunur. Repo oluşturup dosya yüklemek için Write token gerekli.')
    HfFolder.save_token(token)
    print('Giriş başarılı; hesap:',account.get('name','(doğrulandı)'))
    print('Token kaydedildi:',constants.HF_TOKEN_PATH)
    print('Token içeriği gösterilmedi. Yayın için hazır.')

if __name__=='__main__':
    main()
