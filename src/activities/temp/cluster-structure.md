```
Docker Compose
│
├── Hadoop HDFS
│   ├── NameNode
│   │   ├── Contenedor: namenode
│   │   ├── Imagen: bde2020/hadoop-namenode
│   │   ├── Puertos:
│   │   │   ├── 9870 → Web UI HDFS
│   │   │   └── 9000 → Servicio HDFS
│   │   └── Estado: healthy
│   │
│   ├── DataNode1
│   │   ├── Contenedor: datanode1
│   │   ├── Imagen: bde2020/hadoop-datanode
│   │   ├── Puerto:
│   │   │   └── 9864 → Web UI DataNode
│   │   └── Estado: healthy
│   │
│   └── DataNode2
│       ├── Contenedor: datanode2
│       ├── Imagen: bde2020/hadoop-datanode
│       ├── Puerto:
│       │   └── 9865 → Web UI DataNode
│       └── Estado: healthy
│
├── YARN
│   ├── ResourceManager
│   │   ├── Contenedor: resourcemanager
│   │   ├── Puerto:
│   │   │   └── 8088 → Web UI YARN
│   │   └── Estado: healthy
│   │
│   └── NodeManager
│       ├── Contenedor: nodemanager
│       ├── Puerto interno:
│       │   └── 8042
│       └── Estado: healthy
│
├── Hive
│   ├── Hive Server
│   │   ├── Contenedor: hive-server
│   │   ├── Puerto:
│   │   │   └── 10000 → HiveServer2
│   │   └── Estado: running
│   │
│   └── PostgreSQL Metastore
│       ├── Contenedor: db-psql-metastore
│       ├── Puerto:
│       │   └── 5432 → PostgreSQL
│       └── Estado: healthy
│
├── Sqoop
│   ├── Contenedor: sqoop
│   ├── Imagen: dvoros/sqoop
│   └── Estado: running
│
├── MySQL
│   ├── Contenedor: db-mysql-metastore
│   ├── Puerto:
│   │   └── 3307 → MySQL
│   └── Estado: running
│
├── Prometheus
│   ├── Contenedor: prometheus
│   ├── Puerto:
│   │   └── 9090 → Métricas
│   └── Estado: running
│
└── Grafana
    ├── Contenedor: grafana
    ├── Puerto:
    │   └── 3000 → Dashboards
    └── Estado: running
```