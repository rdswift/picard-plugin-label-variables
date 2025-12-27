# Label Variables

## Overview

This plugin provides variables containing label information for a release for use in user or file naming scripts.

---

## What it Does

This plugin reads the release metadata provided to Picard and exposes the information in a number of additional variables for use in Picard scripts.

***NOTE:*** This plugin makes no additional calls to the MusicBrainz website api for the information.

### Label Variables

* **_label_ids_multi** - All label IDs listed, as a multi-value
* **_label_names_multi** - All label names listed, as a multi-value
* **_label_sort_names_multi** - All label names listed (sort name), as a multi-value
* **_label_disambig_multi** - All label disambiguations listed, as a multi-value
* **_label_catalog_multi** - All label catalog numbers listed, as a multi-value
* **_label_label_count** - Count of the number of labels listed
* **_label_catalog_count** - Count of all catalog numbers listed

***NOTE:*** Variables will not be created if the data is missing.

---
