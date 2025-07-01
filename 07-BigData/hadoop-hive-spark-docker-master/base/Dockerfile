FROM ubuntu:22.04

RUN sed -i -e "s|http://archive.ubuntu.com|http://jp.archive.ubuntu.com|g" /etc/apt/sources.list \
 && apt-get -qq update  \
 && DEBIAN_FRONTEND=noninteractive apt-get -qq install --no-install-recommends \
      sudo \
      openjdk-8-jdk \
      curl \
      gnupg \
      procps \
      maven \
      git \
      python3\
      python3-dev\
      python3-pip\
      python3-setuptools\
      python3-wheel\
      python3-venv\
      python-is-python3\
      coreutils \
      libc6-dev \
      netcat-openbsd \
 && rm -rf /var/lib/apt/lists/*

ARG USERNAME=jupyter
ARG GROUPNAME=jupyter
ARG UID=1001
ARG GID=1001

RUN echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
 && chmod 0440 /etc/sudoers.d/$USERNAME \
 && groupadd -g $GID $GROUPNAME \
 && useradd -m -s /bin/bash -u $UID -g $GID $USERNAME

USER $USERNAME

ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/

# Hadoop
ARG HADOOP_VERSION=3.3.6
ARG HADOOP_URL=https://www.apache.org/dist/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz
ENV HADOOP_HOME=/opt/hadoop

RUN set -x \
 && curl -fsSL https://archive.apache.org/dist/hadoop/common/KEYS -o /tmp/hadoop-KEYS \
 && sudo mkdir $HADOOP_HOME  \
 && sudo chown $USERNAME:$GROUPNAME -R $HADOOP_HOME \
 && curl -fsSL $HADOOP_URL -o /tmp/hadoop.tar.gz \
 && curl -fsSL $HADOOP_URL.asc -o /tmp/hadoop.tar.gz.asc \
 && tar -xf /tmp/hadoop.tar.gz -C $HADOOP_HOME --strip-components 1 \
 && mkdir $HADOOP_HOME/logs \
 && rm /tmp/hadoop*
 #  && gpg --import /tmp/hadoop-KEYS \
#  && gpg --verify /tmp/hadoop.tar.gz.asc \

ENV HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
ENV PATH=$HADOOP_HOME/sbin:$HADOOP_HOME/bin:$PATH
ENV LD_LIBRARY_PATH=$HADOOP_HOME/lib/native:$LD_LIBRARY_PATH

# Spark
ARG SPARK_VERSION=3.3.1
ARG SPARK_URL=https://archive.apache.org/dist/spark/spark-$SPARK_VERSION/spark-$SPARK_VERSION-bin-hadoop3.tgz
ENV SPARK_HOME=/opt/spark

RUN set -x \
 && curl -fsSL https://archive.apache.org/dist/spark/KEYS -o /tmp/spark-KEYS  \
 && sudo mkdir $SPARK_HOME \
 && sudo chown $USERNAME:$GROUPNAME -R $SPARK_HOME \
 && curl -fsSL $SPARK_URL -o /tmp/spark.tgz \
 && curl -fsSL $SPARK_URL.asc -o /tmp/spark.tgz.asc \
 && tar -xf /tmp/spark.tgz -C $SPARK_HOME --strip-components 1 \
 && rm /tmp/spark* \
 && curl -fsSL https://jdbc.postgresql.org/download/postgresql-42.3.2.jar -o $SPARK_HOME/jars/postgresql-42.3.2.jar
#  && gpg --import /tmp/spark-KEYS \
#  && gpg --verify /tmp/spark.tgz.asc \

ENV PYTHONHASHSEED=1
ENV PYSPARK_PYTHON=python3
ENV SPARK_CONF_DIR=$SPARK_HOME/conf
ENV PATH=$SPARK_HOME/sbin:$SPARK_HOME/bin:$PATH

ARG KAFKA_CONNECTOR_VERSION=3.3.1
ARG SCALA_VERSION=2.12

RUN curl -fsSL https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/${KAFKA_CONNECTOR_VERSION}/spark-sql-kafka-0-10_2.12-${KAFKA_CONNECTOR_VERSION}.jar -o $SPARK_HOME/jars/spark-sql-kafka-0-10_2.12-${KAFKA_CONNECTOR_VERSION}.jar \
    && curl -fsSL https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.3.1/kafka-clients-3.3.1.jar -o $SPARK_HOME/jars/kafka-clients-3.3.1.jar \
    && curl -fsSL https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.11.1/commons-pool2-2.11.1.jar -o $SPARK_HOME/jars/commons-pool2-2.11.1.jar \
    && curl -fsSL https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/${SPARK_VERSION}/spark-token-provider-kafka-0-10_2.12-${SPARK_VERSION}.jar -o $SPARK_HOME/jars/spark-token-provider-kafka-0-10_2.12-${SPARK_VERSION}.jar \
    && curl -fsSL https://repo1.maven.org/maven2/org/apache/spark/spark-network-common_2.12/${SPARK_VERSION}/spark-network-common_2.12-${SPARK_VERSION}.jar -o $SPARK_HOME/jars/spark-network-common_2.12-${SPARK_VERSION}.jar \
    && curl -fsSL https://repo1.maven.org/maven2/org/apache/spark/spark-streaming-kafka-0-10_${SCALA_VERSION}/${SPARK_VERSION}/spark-streaming-kafka-0-10_${SCALA_VERSION}-${SPARK_VERSION}.jar
# Hive
ARG HIVE_VERSION=3.1.3
ARG HIVE_URL=https://archive.apache.org/dist/hive/hive-$HIVE_VERSION/apache-hive-$HIVE_VERSION-bin.tar.gz
ENV HIVE_HOME=/opt/hive

RUN set -x \
 && curl -fsSL https://archive.apache.org/dist/hive/KEYS -o /tmp/hive-KEYS  \
 && sudo mkdir $HIVE_HOME \
 && sudo chown $USERNAME:$GROUPNAME -R $HIVE_HOME \
 && curl -fsSL $HIVE_URL -o /tmp/hive.tar.gz \
 && curl -fsSL $HIVE_URL.asc -o /tmp/hive.tar.gz.asc \
 && tar -xf /tmp/hive.tar.gz -C $HIVE_HOME --strip-components 1 \
 && rm /tmp/hive*
#  && gpg --import /tmp/hive-KEYS \
#  && gpg --verify /tmp/hive.tar.gz.asc \

#RUN sudo rm $HIVE_HOME/lib/guava-*.jar \
# && sudo cp $HADOOP_HOME/share/hadoop/hdfs/lib/guava-*.jar $HIVE_HOME/lib/
#RUN mv /opt/hive/lib/log4j-slf4j-impl-2.6.2.jar /opt/hive/lib/log4j-slf4j-impl-2.6.2.jar.bak

ENV HIVE_CONF_DIR=$HIVE_HOME/conf
ENV PATH=$HIVE_HOME/sbin:$HIVE_HOME/bin:$PATH

# Config
COPY --chown=$USERNAME:$GROUPNAME conf/core-site.xml $HADOOP_CONF_DIR/
COPY --chown=$USERNAME:$GROUPNAME conf/hdfs-site.xml $HADOOP_CONF_DIR/
COPY --chown=$USERNAME:$GROUPNAME conf/yarn-site.xml $HADOOP_CONF_DIR/
COPY --chown=$USERNAME:$GROUPNAME conf/mapred-site.xml $HADOOP_CONF_DIR/
COPY --chown=$USERNAME:$GROUPNAME conf/workers $HADOOP_CONF_DIR/
COPY --chown=$USERNAME:$GROUPNAME conf/spark-defaults.conf $SPARK_CONF_DIR/
COPY --chown=$USERNAME:$GROUPNAME conf/log4j.properties $SPARK_CONF_DIR/
COPY --chown=$USERNAME:$GROUPNAME conf/hive-site.xml $HIVE_CONF_DIR/

RUN ln $HADOOP_CONF_DIR/workers $SPARK_CONF_DIR/ \
 && ln $HIVE_CONF_DIR/hive-site.xml $SPARK_CONF_DIR/

# RUN mkdir -p /tmp/tez \
#      && curl -fsSL https://archive.apache.org/dist/tez/KEYS -o /tmp/tez-KEYS \
#      && curl -fsSL https://archive.apache.org/dist/tez/0.9.2/apache-tez-0.9.2-bin.tar.gz -o /tmp/tez.tar.gz \
#      && curl -fsSL https://archive.apache.org/dist/tez/0.9.2/apache-tez-0.9.2-bin.tar.gz.asc -o /tmp/tez.tar.gz.asc \
#      && tar -xf /tmp/tez.tar.gz -C /tmp/tez --strip-components 1 \
#      && rm /tmp/tez.tar.gz \
#      && gpg --import /tmp/tez-KEYS \
#      # && gpg --verify /tmp/tez.tar.gz.asc \
#      && cp -r /tmp/tez/* $HADOOP_HOME/share/hadoop/yarn/ \
#      && rm -rf /tmp/tez*

     # Tez
# ARG TEZ_VERSION=0.10.4
# ENV TEZ_HOME=/opt/tez
# ENV TEZ_CONF_DIR=/opt/tez/conf

# RUN set -x \
#     && sudo mkdir -p $TEZ_HOME \
#     && sudo chown $USERNAME:$GROUPNAME -R $TEZ_HOME \
#     && curl -fsSL https://archive.apache.org/dist/tez/$TEZ_VERSION/apache-tez-$TEZ_VERSION-bin.tar.gz -o /tmp/tez.tar.gz \
#     && tar -xf /tmp/tez.tar.gz -C $TEZ_HOME --strip-components 1 \
#     && rm /tmp/tez.tar.gz \
#     && cd $TEZ_HOME \
#     && tar -czf tez.tar.gz lib conf \
#     && sudo mkdir -p $HADOOP_HOME/share/hadoop/tez \
#     && sudo cp tez.tar.gz $HADOOP_HOME/share/hadoop/tez/ \
#     && sudo cp tez.tar.gz $HADOOP_HOME/share/hadoop/yarn/ \
#     && mkdir -p $TEZ_CONF_DIR
    
# # ENV HADOOP_CLASSPATH=${HADOOP_CLASSPATH}:${TEZ_HOME}/lib/*:${TEZ_HOME}/conf
# ENV HADOOP_CLASSPATH=${HADOOP_CLASSPATH}:${TEZ_HOME}/lib/*:${TEZ_CONF_DIR}:${HADOOP_HOME}/share/hadoop/tools/lib/*
# ENV TEZ_JARS=${TEZ_HOME}
# ENV TEZ_CONF_DIR=${TEZ_HOME}/conf

# Add tez-site.xml configuration
# COPY --chown=$USERNAME:$GROUPNAME conf/tez-site.xml $TEZ_CONF_DIR/

# Entry point
COPY entrypoint.sh /usr/local/sbin/entrypoint.sh
RUN sudo chmod a+x /usr/local/sbin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]