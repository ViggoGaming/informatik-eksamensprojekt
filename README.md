# Informatik eksamensprojekt

Hent kildekoden:
```bash
git clone https://github.com/ViggoGaming/informatik-eksamensprojekt/
cd informatik-eksamensprojekt
```

## ANGIV OPENAI-API NØGLEN MED KOMMANDOEN FRA RAPPORTEN UNDER AFSNITTET BRUGERVEJLEDNING


Byg docker-image
```bash
docker build -t informatik-eksamensprojekt .
```

Kør docker-containeren
```bash
docker run -p 8501:8501 informatik-eksamensprojekt
```

Herefter kan vores produkt tilgås via følgende web-adresse:
```
http://localhost:8501
```
