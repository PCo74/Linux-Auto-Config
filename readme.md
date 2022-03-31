# Linux Auto Configuration

## Environnement

- Windows + VirtualBox

📌 adaptable sur d'autres environnements (`.bat` à convertir)

## Pourquoi ?

- conserver l'historique des modifications réalisées sur une VM
- installer automatiquement une VM de base (p.e. pour une démonstration)
- tester rapidement toutes modifications (p.e. changement de version)

## Principe

- configurer rapidement une VM de base
  - soit en copiant des fichiers
  - soit en exécutant des commandes **«bash»**

Ces fichiers et commandes seront définis dans un même fichier `*.txt` au format `UTF-8 UNIX (LF)`

## Mode <q>utilisateur</q>

### Sur la machine hôte

- installer Python (si ce n'est pas déjà fait !)
- lancer le serveur de configuration `...\LAC_SIO_2021\run_python_http.server.bat`

### Sur la machine virtuelle :

1. laisser le mode d'accès par défaut sous VirtualBox (**NAT**)
2. récupérer le script bash `wget 192.168.56.1:8000/vmslinux`
3. puis l'exécuter `bash vmslinux`
4. choisir, dans le menu proposé, la configuration voulue
5. l'auto-configuration est lancée ...
6. après un redémarrage de la VM, se reconnecter pour poursuivre l'auto-configuration !

## Mode <q>concepteur</q>

1. créer un fichier `*.txt` au format `UTF-8 UNIX (LF)` pour chaque VM dans le dossier `vmslinux`
   ou dans un sous-dossier de celui-ci
2. commencer toujours par indiquer le nom d'un bloc qui correspondra
   soit à un fichier à copier
   soit à une liste de commandes à exécuter

	- pour indiquer le nom d'un bloc :
		- saisir en premier l'identifiant défini dans le fichier `config.ini` (par défaut `=--=`)
		- ensuite lui donner un nom :
			- si ce nom commence par un `/` ou bien un `.`, c'est un bloc à copier selon son chemin absolu ou relatif
			- sinon c'est un bloc de commandes à exécuter !
		
☼ exemple pour un serveur Web Apache `web1.txt`

```
=--=/etc/hostname
web1

=--=/etc/hosts
127.0.0.1       localhost
127.0.1.1       web1
192.168.56.12   web2

# The following lines are desirable for IPv6 capable hosts
::1     localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters

=--=/etc/network/interfaces
# This file describes the network interfaces available on your system
# and how to activate them. For more information, see interfaces(5).

# The loopback network interface
auto lo
iface lo inet loopback

# privé hôte 192.168.56.0/24
auto enp0s3
iface enp0s3 inet static
    address 192.168.56.11/24
    gateway 192.168.56.254
	
=--=install_paquets_apache
apt update
apt install -y apache2
```

4 blocs sont ainsi définis :

| bloc 			             | type	    |
|----------------------------|----------|
|`/etc/hostname`             | fichier  |
|`/etc/hosts`                | fichier  |
|`/etc/network/interfaces`   | fichier  |
|`install_paquets_apache`    | commande |

- les 3 premiers correspondent à des blocs de fichiers à copier selon leur chemin absolu
- le dernier est une liste de commandes à exécuter !

## Vue HTML

Extension qui permet de générer au format **HTML** la configuration d'une VM via un script **Python**
- déposer le fichier ou le dossier sur le fichier **batch** `...\LAC_SIO_2021\vmslinux_vmlinux-vue-html.bat`

---
©PCo-2021