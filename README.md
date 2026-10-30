# This repository is archived

**This project is no longer maintained.** Development continues at **[aldweb/ha-lg-hombot](https://github.com/aldweb/ha-lg-hombot)**.

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=aldweb&repository=ha-lg-hombot&category=integration)

aldweb's fork is actively maintained, works with current Home Assistant versions and adds a lot on top of this version, including:

- Compatibility with Home Assistant 2026.8+ (battery level as a separate sensor)
- Extended vacuum attributes (cleaning mode, repeat mode, last cleaning, …)
- Camera snapshots from the robot

Please don't open new issues or pull requests here – head over to the new repository instead.

## Switching to the new repository

1. In HACS, remove the LG Hombot integration downloaded from this repository (`plakna/ha-lg-hombot`).
2. Add `https://github.com/aldweb/ha-lg-hombot` as a custom repository (category: Integration) – or use the button above.
3. Install the integration and restart Home Assistant.
4. Check the [migration notes](https://github.com/aldweb/ha-lg-hombot#migration-from-version-1x-to-20) – since v2.0 the battery level is a separate sensor instead of a vacuum attribute, so automations and dashboards may need updating.

## Thanks

Thanks to everyone who used, tested and contributed to this integration – and a special thanks to [@aldweb](https://github.com/aldweb) for carrying it forward.

This was a fork of [ericpignet](https://github.com/ericpignet)'s original LG Hombot integration.
