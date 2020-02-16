#!/bin/bash
addgroup -g $PGID $GROUP
adduser -D -H -G $USERNAME -s /bin/false -u $PUID $USERNAME
echo -e "$PASSWORD\n$PASSWORD" | smbpasswd -a -s -c /config/smb.conf $USERNAME

if [ ! -e /config/smb.conf ]; then

  # Write the global default settings for the SMB config
  cat > /config/smb.conf <<EOL
[global]
    netbios name = $SERVERNAME
    workgroup = WORKGROUP
    server string = Samba %v in an Alpine Linux Docker container
    security = user
    guest ok = yes
    guest account = $USERNAME
    read only = no
    create mask = 0777
    directory mask = 0777
    map to guest = bad user

    # disable printing services
    load printers = no
    printing = bsd
    printcap name = /dev/null
    disable spoolss = yes

EOL


  # Write the per share settings for the SMB config
  for SHARE in ${SHARES[@]}; do
    if [ -d ${SHARE} ]; then
      NAME=`basename $SHARE`

      cat >> /config/smb.conf <<EOL

[$NAME]
    comment = $NAME
    path = ${SHARE}
    read only = no
    guest ok = yes
    #write list = $USERNAME
EOL
    else
      echo $SHARE is not a valid directory to share
    fi
  done

  chown $USERNAME:$USERNAME /config/smb.conf
fi

# Start the SMB services
smbd -F -S -s /config/smb.conf &
nmbd -F -S -s /config/smb.conf

