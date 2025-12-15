# Personregister i testmiljön

Ett enkelt system för att hantera testdata på ett GDPR-kompatibelt sätt.

## Funktioner


- Skapa och initiera databas med testanvändare

- Visa alla användare

- Rensa all testdata (GDPR åtgärd 1)

- Anonymisera användardata (GDPR åtgärd 2)

## Validering av testdata

Projektet innehåller en funktion `test_fake_users()` som kan användas för att validera att den genererade testdatan är korrekt. Funktionen kontrollerar:

- att rätt antal användare har skapats
- att alla e‑postadresser är syntetiska
- att inga obligatoriska fält är tomma

Detta är ett manuellt valideringssteg som säkerställer
att testmiljön följer GDPR‑krav.

## Installation och körning


### Förutsättningar

- Docker och Docker Compose

- Python 3.9+

### Kör med Docker

1. Klona repot:

```bash

git clone <https://github.com/MariaAriza05/project-personregister>

cd project-personregister