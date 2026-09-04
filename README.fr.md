# Open NG-SOC Lab

Open NG-SOC Lab est un laboratoire pédagogique de détection et de réponse fondé sur des preuves, intégrant Wazuh, Suricata, MISP et Shuffle.

> [!WARNING]
> Ce laboratoire VMware isolé n'est **pas prêt pour la production**. Utilisez-le uniquement sur des systèmes possédés ou explicitement autorisés.

Le dépôt documente dix capacités (`100051` à `100059` et `100100`). Les règles exactes, décodeurs et fixtures ne seront publiés qu'après export, assainissement et validation. PT-01, PT-02, PT-03, PT-04 et PT-06 ont réussi dans le laboratoire avec des preuves privées. PT-05 n'a volontairement pas été exécuté, car l'effacement des journaux est destructif. Les événements AWS CloudTrail sont entièrement synthétiques.

La documentation principale est en anglais : [README.md](README.md).

## État actuel

- Baseline confirmée : Wazuh `4.8.2`.
- MISP → Shuffle → Slack validé dans le laboratoire privé.
- Export public différé jusqu'à l'audit de sécurité et la rotation des secrets.
- Aucune release, aucun tag et aucune revendication de déploiement en une commande.
- Propriété intellectuelle et licence en attente ; aucune licence open source n'est accordée.

## Validation

```powershell
pwsh -File scripts/validate_repository.ps1
```

Consultez [REPOSITORY_STATUS.md](REPOSITORY_STATUS.md) et [la checklist d'export](docs/LAB_EXPORT_CHECKLIST.md).

## Sécurité

Ne publiez jamais de clés API, jetons, identifiants de webhook, clés privées, données personnelles, topologie confidentielle, images de VM, journaux bruts, malware ou captures réseau dangereuses.
