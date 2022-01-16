✅ installation «viewer MarkDown» https://addons.mozilla.org/en-US/firefox/addon/gitlab-markdown-viewer/

# Linux Auto Configuration

## Environnement

- Windows + VirtualBox

## Sur la machine hôte

- installer Python (si ce n'est pas déjà fait !)
- lancer le serveur de configuration `...\LAC_SIO_2021\run_python_http.server.bat`

## Sur la machine virtuelle :

0. laisser le mode d'accès par défaut sous VirtualBox (**NAT**)
1. récupérer le script bash `wget 192.168.56.1:8000/vmslinux`
2. puis l'exécuter `bash vmslinux`
3. choisir, dans le menu proposé, la configuration voulue
4. l'auto-configuration est lancée ...
5. après un redémarrage de la VM, se reconnecter pour poursuivre l'auto-configuration !

---
©PCo-2021