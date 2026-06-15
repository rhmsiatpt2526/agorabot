# AgoraBot — Navigation Sociale ROS2

## Présentation

AgoraBot est un projet de navigation sociale basé sur ROS2, Nav2 et HuNavSim.

L’objectif est de développer un robot mobile capable de naviguer dans un environnement humain dynamique en respectant des contraintes sociales :

- distance interpersonnelle
- évitement naturel
- adaptation locale du comportement
- gestion de zones sociales
- recovery behaviors

Le projet combine :

- ROS2 Humble
- Nav2
- Gazebo
- HuNavSim
- Social Costmaps
- Nav2 Costmap Filters
- Behavior Trees
- Social Force Models (SFM)

---

# Installation

Veuillez suivre rigoureusement les étapes suivantes d'installation dans l'ordre conseillé afin de garantir le succès de la simulation.

Le projet doit s'exécuter de préférence sur Ubuntu-22.04 Humble, le développement a été fait sur Windows 11 avec WSL. Le développement peut se faire via WSL dans VS Code.

## Dépendances système

```bash
sudo apt update

sudo apt install ros-humble-nav2*
sudo apt install ros-humble-navigation2
sudo apt install ros-humble-behaviortree-cpp-v3
sudo apt install ros-humble-gazebo-ros-pkgs
sudo apt install python3-vcstool
sudo apt install python3-rosdep
```

## Création du workspace

De préférence, utiliser un workspace du nom de "ros2_ws", mais tout autre nom est également valide:

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
```

---

## Clone du projet
Le git du projet est public et ne devrait donc présenter aucun soucis de téléchargement.
```bash
cd src

git clone https://github.com/rhmsiatpt2526/agorabot.git
```

---

## Import automatique des dépendances

```bash
vcs import --debug . < agorabot/agorabot.repos
```

Cette commande télécharge automatiquement les dépendances externes nécessaires :

- HuNavSim
- BehaviorTree.CPP
- BehaviorTree.ROS2
- lightsfm
- people
- agorabot_sfm
- etc.
Le paramètre debug est optionel et permet juste d'avoir plus de détails lors de l'import.
---

## Installation des dépendances ROS

```bash
cd ~/ros2_ws

rosdep install --from-paths src --ignore-src -r -y
```

---

## Build

```bash
cd ~/ros2_ws

colcon build --symlink-install

source install/setup.bash
```

---

# Lancement

## Launch normal (3 humains)

Lancez en priorité cette version, plus légère que la version dense (notamment en termes de simulation gazebo).

```bash
ros2 launch agorabot_bringup social_navigation.launch.py
```
Par défaut, le client Gazebo (son interface graphique) s'affiche avec Rviz suite au lancement. Cependant, afin de limiter les ressources nécessaires à la simulation, il est possible d'empêcher l'affichage de gazebo. Pour ce faire, mettez sur False l'argument optionnel (True est équivalent au lancement par défaut). 

```bash
ros2 launch agorabot_bringup social_navigation.launch.py launch_gazebo_gui:=False
```

## Launch variante dense (7 humains)

Une autre version avec 7 humains sur la map est disponible sous réserve de ressources suffisantes.

```bash
ros2 launch agorabot_bringup social_navigation.launch.py scenario agents_house_dense.yaml
```
--- 
## Bug fix spawn humains

En cas de bug où au démarrage tous les humains spawnent au même endroit sur le robot, ce qui arrive parfois, faire le reset complet suivant : 

```bash
pkill -f ros2
pkill -f gazebo
pkill -f gzserver
pkill -f gzclient
pkill -f rviz2
pkill -f python3

ros2 daemon stop
ros2 daemon start

cd ~/ros2_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
```
---


# Fonctionnalités actuelles

## Simulation

Stack complète fonctionnelle :

- Gazebo
- HuNavSim
- Nav2
- RViz
- launch unifié

---

## Navigation sociale dynamique

Le robot :

- récupère les positions et vitesses des humains,
- génère des zones sociales dynamiques,
- injecte des coûts sociaux dans Nav2,
- adapte localement sa navigation.

---

## Social Layer Nav2

Une SocialLayer Nav2 personnalisée a été développée.

Fonctionnalités :

- costmap sociale dynamique,
- proxémie elliptique anisotrope,
- orientation selon la vitesse des humains,
- intégration dans la local_costmap Nav2.

---

## Costmap Filters Nav2

Des keepout filters Nav2 ont été intégrés.

Fonctionnalités :

- définition de zones sociales interdites,
- contraintes spatiales statiques,
- intégration dans global_costmap et local_costmap,
- mask server + filter info server.

Le projet combine donc :

- zones sociales dynamiques (humains),
- zones sociales statiques (costmap filters).

---

## Behavior Tree social

Un comportement social simple a été intégré au BT Nav2.

États actuels :

- NORMAL
- WAIT

Le robot peut temporairement interrompre sa navigation lorsqu’un humain est trop proche.

---

## Recovery behaviors

Des comportements de récupération Nav2 sont utilisés :

- replanning,
- wait,
- retry,
- backoff.

---

## Adaptive velocity

La vitesse du robot peut être réduite localement selon la proximité des humains.

---

## Social Force Models (SFM)

Le projet intègre également un package d'adaptation léger et personnalisé :

```text
agorabot_sfm
```

Ce package regroupe :

- l’intégration des modèles SFM,
- les wrappers ROS2 nécessaires,
- les adaptations spécifiques au projet.

Le repository est automatiquement téléchargé via :

```text
agorabot.repos
```

---

# Structure du projet

```text
agorabot/
├── agorabot_bringup/              # launch principal
├── agorabot_bt_nodes/             # plugins BT personnalisés
├── agorabot_navigation/           # configuration Nav2
├── agorabot_social_layer/         # noeuds Python sociaux
├── agorabot_social_layer_cpp/     # plugin C++ SocialLayer
├── behavior_trees/                # BT XML Nav2
├── config/                        # configs Nav2 / filters
├── maps/                          # masks costmap filters
├── agorabot.repos                 # dépendances ROS2 externes
└── README.md
```

Repositories externes téléchargés automatiquement :

- hunav_sim
- hunav_gazebo_wrapper (fork personnel)
- BehaviorTree.CPP
- BehaviorTree.ROS2
- people
- lightsfm
- agorabot_sfm (package personnel)

---


# Avancement du projet

## Réalisé

- [x] Architecture ROS2
- [x] Intégration Gazebo + HuNavSim
- [x] Navigation Nav2
- [x] Visualisation RViz
- [x] Social costmap dynamique
- [x] SocialLayer Nav2 personnalisée
- [x] Zones sociales elliptiques orientées
- [x] Navigation sociale locale
- [x] Adaptive velocity
- [x] Recovery behaviors Nav2
- [x] Behavior Tree social
- [x] Nav2 Costmap Filters
- [x] Zones sociales statiques
- [x] Intégration SFM
- [x] Master launch file

---

# Travail restant

- amélioration des comportements BT,
- scénarios sociaux complexes,
- améliorer les costmap filters,
- diversification scénarios (e.g. aggresive)
- amélioration trapped scenario,
- tuning navigation sociale,
- intégration MPPI (si possible),
- évaluation expérimentale plus rigoureuse,
- vidéo de démonstration.
