import requests
from bs4 import BeautifulSoup

def scrape_medbase(medicine_name):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept-Language": "fr-FR,fr;q=0.9,ar;q=0.8"
    }
    
    search_url = f"https://medbase.ma/medicaments?search={medicine_name.replace(' ', '+')}"
    
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        med_card = soup.find('div', class_='medicament-card') or soup.find('div', class_='product-item')
        
        if med_card:
            name = med_card.find('h2') or med_card.find('h3') or med_card.find('a')
            name_text = name.text.strip() if name else medicine_name
            
            text_content = med_card.get_text(separator=' | ', strip=True)
            
            extracted_data = {
                "الاسم": name_text,
                "المادة الفعالة": "يحتاج مراجعة يدوية",
                "المختبر": "غير محدد",
            }
            
            if "sanofi" in text_content.lower():
                extracted_data["المختبر"] = "Sanofi"
            elif "servier" in text_content.lower():
                extracted_data["المختبر"] = "Servier"
            elif "pfizer" in text_content.lower():
                extracted_data["المختبر"] = "Pfizer"
            
            return extracted_data
        else:
            return None
            
    except Exception as e:
        return {"error": str(e)}
