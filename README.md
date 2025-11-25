# Som Energia for Home Assistant

[![HACS Action](https://github.com/hectorespert/som-energia-hass/actions/workflows/hacs.yml/badge.svg)](https://github.com/hectorespert/som-energia-hass/actions/workflows/hacs.yml)
[![hassfest](https://github.com/hectorespert/som-energia-hass/actions/workflows/hassfest.yaml/badge.svg)](https://github.com/hectorespert/som-energia-hass/actions/workflows/hassfest.yaml)
[![Python package](https://github.com/hectorespert/som-energia-hass/actions/workflows/python.yaml/badge.svg)](https://github.com/hectorespert/som-energia-hass/actions/workflows/python.yaml)
[![codecov](https://codecov.io/github/hectorespert/som-energia-hass/graph/badge.svg?token=XJG1KVGBT9)](https://codecov.io/github/hectorespert/som-energia-hass)
[![GitHub release](https://img.shields.io/github/v/release/hectorespert/som-energia-hass)](https://github.com/hectorespert/som-energia-hass/releases/latest)

---

## Documentación

Integración para Home Assistant de Som Energia.

Proporciona:

* Sensor con la información del precio de la energía consumida.
* Sensor con la información del precio de compensación.
* Sensor con el periodo tarifario actual (punta, llano, valle).

### Instalación

#### Usando [HACS](https://hacs.xyz/) (recomendado)
1. Copia la URL de este repositorio: [https://github.com/hectorespert/som-energia-hass](https://github.com/hectorespert/som-energia-hass)

2. En la sección de HACS, añade este repositorio como uno personalizado:
   - En el campo "repository" pon la URL copiada anteriormente
   - En "Category" selecciona "Integration"
   - Haz clic en el botón "Download" y descarga la última versión.

3. Reinicia HA

4. Busca Som Energia en la sección de *Integraciones* y configura la integración.

#### Manual

Descarga el archivo `som_energia.zip` de la [última release](https://github.com/hectorespert/som-energia-hass/releases/latest) y extrae el contenido en el directorio `custom_components` de tu instalación de Home Assistant:

```bash
cd config/custom_components
wget https://github.com/hectorespert/som-energia-hass/releases/latest/download/som_energia.zip
unzip som_energia.zip
rm som_energia.zip
```

Después de instalar, reinicia Home Assistant y configura la integración buscando "Som Energia" en la sección de Integraciones.

### Desarrollo

```bash
docker compose up -d
```

---

## Documentation

Integration for Home Assistant of Som Energia.

Provides:

* Sensor with the information of Som Energia's energy price.
* Sensor with the information of the compensation price.
* Sensor with the current tariff period (peak, flat, valley).

### Installation

#### Using [HACS](https://hacs.xyz/) (recommended)
1. Copy this repository URL: [https://github.com/hectorespert/som-energia-hass](https://github.com/hectorespert/som-energia-hass)

2. In the HACS section, add this repository as a custom one:
   - On the "repository" field put the URL copied before
   - On the "Category" select "Integration"
   - Click the "Download" button and download latest version.

3. Restart HA

4. Search for Som Energia in *Integrations* section and configure the integration.

#### Manual

Download the `som_energia.zip` file from the [latest release](https://github.com/hectorespert/som-energia-hass/releases/latest) and extract the contents into the `custom_components` directory of your Home Assistant installation:

```bash
cd config/custom_components
wget https://github.com/hectorespert/som-energia-hass/releases/latest/download/som_energia.zip
unzip som_energia.zip
rm som_energia.zip
```

After installing, restart Home Assistant and configure the integration by searching for "Som Energia" in the Integrations section.

### Development

```bash
docker compose up -d
```
