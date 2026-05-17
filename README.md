# AgoraBot — Navigation Sociale ROS2

## Présentation

AgoraBot est un projet de navigation sociale basé sur ROS2, Nav2 et HuNavSim.

L’objectif est de développer un robot mobile capable de naviguer dans un environnement humain dynamique en respectant des contraintes sociales : distance interpersonnelle, évitement naturel, adaptation du comportement, etc.

Le projet intègre :

- ROS2 Humble
- Nav2
- Gazebo
- HuNavSim
- Costmaps sociales dynamiques
- Behavior Trees (BT)

---

# Fonctionnalités actuelles

## Simulation

Stack complète fonctionnelle :

- Gazebo
- HuNavSim
- Nav2
- RViz
- master launch file

---

## Navigation sociale

Le robot :

- récupère les positions et vitesses des humains,
- génère des zones sociales dynamiques,
- injecte des coûts sociaux dans Nav2,
- adapte localement sa navigation.

---

## Social Layer Nav2

Une vraie SocialLayer Nav2 personnalisée a été développée.

Fonctionnalités :

- costmap sociale dynamique,
- proxémie elliptique anisotrope,
- orientation selon la vitesse des humains,
- intégration directe dans la local_costmap Nav2.

---

## Behavior Tree social

Un premier comportement social a été intégré dans le BT Nav2.

États actuels :

- NORMAL
- WAIT

Le robot peut temporairement interrompre sa navigation lorsqu’un humain est trop proche.

---

# Structure du projet

```text
agorabot/
├── agorabot_bringup/              # master launch files
├── agorabot_bt/                   # anciens éléments BT / expérimentation
├── agorabot_bt_nodes/             # plugins BT Nav2 personnalisés
├── agorabot_navigation/           # configuration navigation
├── agorabot_sim/                  # éléments de simulation
├── agorabot_social_layer/         # noeuds Python sociaux
├── agorabot_social_layer_cpp/     # plugin C++ SocialLayer Nav2
├── behavior_trees/                # BT XML Nav2
├── config/                        # fichiers de configuration
├── docs/                          # documentation
├── launch/                        # launch files secondaires
├── worlds/                        # mondes Gazebo
└── README.md
```

---

# Dépendances

## ROS2

- ROS2 Humble
- Nav2
- behaviortree_cpp_v3
- Gazebo Classic
- HuNavSim

Installation typique :

```bash
sudo apt install ros-humble-nav2*
sudo apt install ros-humble-navigation2
sudo apt install ros-humble-behaviortree-cpp-v3
sudo apt install ros-humble-gazebo-ros-pkgs
```

---

# Build

```bash
cd ~/ros2_ws

colcon build --symlink-install

source install/setup.bash
```

---

# Launch

```bash
ros2 launch agorabot_bringup social_navigation.launch.py
```

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
- [x] Intégration BT sociale basique
- [x] Master launch file

---

# Travail restant

- amélioration des comportements sociaux,
- ralentissement dynamique,
- contournement intelligent,
- comportements BT avancés,
- intégration MPPI,
- évaluation expérimentale.


