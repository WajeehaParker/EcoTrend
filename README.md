# EcoTrend

This is a docker based project that consumes redis and spark containers for applying machine learning techniques to the data.
For running the redis and spark project, just go to the main folder of EcoTrend and write 'docker-compose up'. This will create and start 4 containers (redis, data_injestion, spark-master and spark_ml)

We also intend to add HIVE to it for analytics. This is a work in progress.

We have also added the visualization for this project through streamlit. Right now the visualization is not attached to the docker-compose file. We are working on it. In the meantime, you can run the visualization separately by running 'Data Visualization > BDA_DB.py' file.

The video description of this project could be found at: https://youtu.be/njmnryi4z1A
