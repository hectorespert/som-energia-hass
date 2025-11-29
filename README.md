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

[![Abre tu instancia de Home Assistant y abre un repositorio dentro de Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=hectorespert&repository=som-energia-hass&category=Integration)

1. Abre HACS en Home Assistant
2. Ve a la sección de "Integraciones"
3. Busca "Som Energia" en el buscador
4. Haz clic en "Descargar" e instala la última versión
5. Reinicia Home Assistant
6. Busca Som Energia en la sección de *Integraciones* y configura la integración.

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

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=hectorespert&repository=som-energia-hass&category=Integration)

1. Open HACS in Home Assistant
2. Go to the "Integrations" section
3. Search for "Som Energia" in the search bar
4. Click "Download" and install the latest version
5. Restart Home Assistant
6. Search for Som Energia in the *Integrations* section and configure the integration.

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
