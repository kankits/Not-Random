FROM silkeh/clang:14-buster

ARG DEBIAN_FRONTEND=noninteractive

# Update
RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y vim git bison flex libreadline-dev make zlib1g zlib1g-dev pgcli

RUN wget --content-disposition https://ftp.postgresql.org/pub/source/v12.0/postgresql-12.0.tar.gz && tar -zxf postgresql-12.0.tar.gz && cp -r postgresql-12.0 /opt/postgresql

RUN apt-get install -y python3 python3-dev python3-pip

COPY Not-Random/requirements.txt ./

RUN pip3 install -r requirements.txt

WORKDIR "/opt/postgresql"

ENV CC=/usr/bin/clang

RUN ./configure && \
	make && \
	su && \
	make install

RUN	useradd -ms /bin/bash  postgres && \
	mkdir /usr/local/pgsql/data && \
	chown postgres /usr/local/pgsql/data

USER postgres

RUN echo "export PATH=$PATH:/usr/local/pgsql/bin" > /home/postgres/.bashrc

