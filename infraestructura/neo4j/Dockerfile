FROM neo4j:3.0

MAINTAINER Adolfo De Unánue

RUN sed -i -e 's/#dbms.security.auth_enabled=false/dbms.security.auth_enabled=false/g' /var/lib/neo4j/conf/neo4j.conf
RUN sed -i -e 's/import=import/import=\/home\/fdc\/fuga-de-cerebros\/import/g' /var/lib/neo4j/conf/neo4j.conf

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["neo4j"]

