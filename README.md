# Comparație între două versiuni de fișiere Excel

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-%E2%9C%A8%20App-red?logo=streamlit)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

Aplicație Streamlit care permite **compararea vizuală** între două versiuni ale aceluiași fișier Excel. Este ideală pentru planuri, baze de date sau rapoarte în care identificarea rapidă a diferențelor este esențială.

---

## ✅ Funcționalități principale

- 🔍 Încarcă două fișiere `.xlsx` cu un sheet numit exact **`Refit plan 2025`**
- 🔑 Detectează automat rândul antetului (în funcție de celula `"Nr. mag."`)
- 🧩 Poți selecta **coloanele de comparat** (cu 8 coloane presetate utile)
- 🔁 Compară pe baza coloanei `"Nr. mag."` (ID unic)
- 🚨 Identifică:
  - ✅ **Modificări** în coloanele selectate
  - ➕ **ID-uri noi** (existente doar în a doua versiune)
  - ➖ **ID-uri dispărute** (existente doar în prima versiune)
- 🎨 Afișează diferențele evidențiate în tabel:
  - Modificări: fundal **roșu deschis**
  - ID-uri noi: fundal **albastru deschis**
  - ID-uri dispărute: fundal **gri deschis**
- 📂 **Filtru vizual** după tipul de diferență:
  - Toate
  - Doar ID-uri noi
  - Doar ID-uri dispărute
  - Doar modificări

---

## 🟢 Utilizare

1. Instalează dependențele:
   ```bash
   pip install -r requirements.txt
    ```
2.	Rulează aplicația:
   ```bash
   streamlit run compara_excel.py
   ```

3.	Încarcă cele două fișiere .xlsx în aplicație
4.	Selectează coloanele de interes și tipul de diferențe dorit
5.	Analizează diferențele evidențiate direct în tabel

---

## 📝 Cerințe fișiere
	•	Fișierele trebuie să conțină un sheet cu numele exact: Refit plan 2025
	•	Antetul tabelului trebuie să înceapă pe un rând în care prima celulă este: Nr. mag.
	•	Coloana "Nr. mag." trebuie să conțină ID-uri unice pe rânduri