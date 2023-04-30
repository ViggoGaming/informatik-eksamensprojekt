# Informatik eksamensprojekt

Hent kildekoden:
```bash
git clone https://github.com/ViggoGaming/informatik-eksamensprojekt/
cd informatik-eksamensprojekt
```
Byg docker-filen
```bash
docker build -t informatik-eksamensprojekt .
```

Kør docker-containeren (Husk at angiv den rigtige API-nøgle)
```bash
docker run -p 8501:8501 informatik-eksamensprojekt
```

Herefter kan vores produkt tilgås via følgende web-adresse:
```
http://localhost:8501
```
