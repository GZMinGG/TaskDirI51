FROM alpine:latest 
ENV SERVERNAME docker-samba 
ENV USERNAME samba
ENV GROUP samba
ENV PASSWORD samba
ENV SHARES /shares
ENV PUID 1100
ENV PGID 1100
RUN apk --no-cache add samba samba-common-tools bash && mkdir /init-config /config /shares
COPY run.sh /
VOLUME /config
EXPOSE 137 138 139 445
CMD ["/run.sh"]
