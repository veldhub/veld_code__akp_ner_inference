# veld_code__akp_ner_inference

This repo contains [code velds](https://zenodo.org/records/13322913) which apply NER models on
linkedcat data for usage of the inferenced entites in the AKP project.

## requirements

- git
- docker compose (note: older docker compose versions require running `docker-compose` instead of 
  `docker compose`)

## how to use

A code veld may be integrated into a chain veld, or used directly by adapting the configuration 
within its yaml file and using the template folders provided in this repo. Open the respective veld 
yaml file for more information.

**[./veld_infer.yaml](./veld_infer.yaml)** : apply NER models on linkedcat data for usage of the inferenced entites in the AKP project
```
docker compose -f veld_infer.yaml up
```

