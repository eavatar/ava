FROM eavatar/basebox
MAINTAINER sampot <sam@eavatar.com>

ADD dist/ava /ava
RUN chown -R ava:ava /ava
EXPOSE 5000 5443
# ENTRYPOINT ["/ava/ava"]
CMD ["/ava/ava", "run"]