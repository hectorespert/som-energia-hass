# Som Energia for Home Assistant

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
To install this integration manually you have to download the content of this repository to `config/custom_components/som-energia-hass` directory:
```bash
mkdir -p custom_components/som-energia-hass
cd custom_components/som-energia-hass
curl -s https://api.github.com/repos/hectorespert/som-energia-hass/releases/latest | grep "/som-energia-hass.zip"|cut -d : -f 2,3|tr -d \"| wget -i -
unzip som-energia-hass.zip
rm som-energia-hass.zip
```
After that restart Home Assistant and configure the integration.

## Development

```bash
docker compose up -d
```