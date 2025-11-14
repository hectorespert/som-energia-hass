# Som Energia for Home Assistant

[![HACS Action](https://github.com/hectorespert/som-energia-hass/actions/workflows/hacs.yml/badge.svg)](https://github.com/hectorespert/som-energia-hass/actions/workflows/hacs.yml)
[![hassfest](https://github.com/hectorespert/som-energia-hass/actions/workflows/hassfest.yaml/badge.svg)](https://github.com/hectorespert/som-energia-hass/actions/workflows/hassfest.yaml)
[![Python package](https://github.com/hectorespert/som-energia-hass/actions/workflows/python.yaml/badge.svg)](https://github.com/hectorespert/som-energia-hass/actions/workflows/python.yaml)
[![codecov](https://codecov.io/github/hectorespert/som-energia-hass/graph/badge.svg?token=XJG1KVGBT9)](https://codecov.io/github/hectorespert/som-energia-hass)
[![GitHub release](https://img.shields.io/github/v/release/hectorespert/som-energia-hass)](https://github.com/hectorespert/som-energia-hass/releases/latest)


Integration for Home Assistant of Som Energia.

* Sensor with the information of Som Energia's energy price.
* Sensor with the information of the compensation price.

## Installation

### Using [HACS](https://hacs.xyz/) (recommended)
1. Copy this repository URL: [https://github.com/hectorespert/som-energia-hass](https://github.com/hectorespert/som-energia-hass)

2. In the HACS section, add this repository as a custom one:
   - On the "repositorysitory" field put the URL copied before
   - On the "Category" select "Integration"
   - Click the "Download" button and download latest version.

3. Restart HA

4. Search for Som Energia in *Integrations* section and configure the integration.

### Manual

Descarga el archivo `som_energia.zip` de la [última release](https://github.com/hectorespert/som-energia-hass/releases/latest) y extrae el contenido en el directorio `custom_components` de tu instalación de Home Assistant:

```bash
cd config/custom_components
wget https://github.com/hectorespert/som-energia-hass/releases/latest/download/som_energia.zip
unzip som_energia.zip
rm som_energia.zip
```

Después de instalar, reinicia Home Assistant y configura la integración buscando "Som Energia" en la sección de Integraciones.

## Development

```bash
docker compose up -d
```