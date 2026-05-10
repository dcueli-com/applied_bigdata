#!/bin/bash

echo "=========================================="
echo "   SISTEMA DE AUTOMATIZACIÓN HADOOP       "
echo "=========================================="

# 1. Limpiar rastro de ejecuciones anteriores
echo "[1/7] Limpiando entorno..."
hdfs dfs -rm -r /user/root/automation 2>/dev/null

# 2. Crear estructura de carpetas para el proyecto
echo "[2/7] Creando directorios en HDFS..."
hdfs dfs -mkdir -p /user/root/automation/input

# 3. Crear un archivo de texto grande y subirlo
echo "[3/7] Generando archivo de prueba..."
for i in {1..1000}; do echo "Lorem fistrum pecador a gramenawer fistro pecador"; done > chiquito_ipsum.txt

echo "[4/7] Subiendo archivo a HDFS..."
hdfs dfs -put -f chiquito_ipsum.txt /user/root/automation/input/

# 4. Verificar que todo está en su sitio
echo "[4/7] Verificando estructura final..."
hdfs dfs -ls -R /user/root/automation

# 5. Ejecutar el trabajo MapReduce (WordCount)
echo "[6/7] Ejecutando MapReduce WordCount..."
hadoop jar /opt/hadoop-3.2.1/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.2.1.jar wordcount /user/root/automation/input /user/root/automation/logs

echo "=========================================="
echo "[7/7] Proceso finalizado, resultado..."
hdfs dfs -ls -R /user/root/automation/logs
echo "------------------------------------------"
hdfs dfs -cat /user/root/automation/logs/part-r-00000
echo "------------------------------------------"
echo "AUTOMATIZACIÓN COMPLETADA"
echo "=========================================="
