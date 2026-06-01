# Xray Reality family fallback last run

- UTC: 2026-06-01T19:26:52+00:00
- Workflow run: https://github.com/indila334-lab/lage-bericht/actions/runs/26776900679
- Commit: 0cc88b4f119c71519fe2ccfd9d6f678a02fbd981
- Exit code: 3

```text
LOCAL_WORKFLOW_OK
MODE_REALITY_TCP443_FALLBACK_ONLY
DO_NOT_TOUCH_AMNEZIAWG
Get:1 file:/etc/apt/apt-mirrors.txt Mirrorlist [144 B]
Hit:2 http://azure.archive.ubuntu.com/ubuntu noble InRelease
Hit:6 https://packages.microsoft.com/repos/azure-cli noble InRelease
Get:7 https://packages.microsoft.com/ubuntu/24.04/prod noble InRelease [3600 B]
Get:3 http://azure.archive.ubuntu.com/ubuntu noble-updates InRelease [126 kB]
Get:4 http://azure.archive.ubuntu.com/ubuntu noble-backports InRelease [126 kB]
Get:5 http://azure.archive.ubuntu.com/ubuntu noble-security InRelease [126 kB]
Get:8 https://dl.google.com/linux/chrome-stable/deb stable InRelease [1825 B]
Get:9 https://packages.microsoft.com/ubuntu/24.04/prod noble/main amd64 Packages [163 kB]
Get:10 https://packages.microsoft.com/ubuntu/24.04/prod noble/main armhf Packages [11.6 kB]
Get:11 https://packages.microsoft.com/ubuntu/24.04/prod noble/main arm64 Packages [134 kB]
Get:12 http://azure.archive.ubuntu.com/ubuntu noble-updates/main amd64 Packages [2050 kB]
Get:13 http://azure.archive.ubuntu.com/ubuntu noble-updates/main Translation-en [360 kB]
Get:14 http://azure.archive.ubuntu.com/ubuntu noble-updates/main amd64 Components [177 kB]
Get:15 http://azure.archive.ubuntu.com/ubuntu noble-updates/universe amd64 Packages [1694 kB]
Get:16 http://azure.archive.ubuntu.com/ubuntu noble-updates/universe Translation-en [330 kB]
Get:17 http://azure.archive.ubuntu.com/ubuntu noble-updates/universe amd64 Components [386 kB]
Get:18 http://azure.archive.ubuntu.com/ubuntu noble-updates/restricted amd64 Packages [3278 kB]
Get:19 http://azure.archive.ubuntu.com/ubuntu noble-updates/restricted Translation-en [760 kB]
Get:20 http://azure.archive.ubuntu.com/ubuntu noble-updates/multiverse Translation-en [11.3 kB]
Get:21 http://azure.archive.ubuntu.com/ubuntu noble-updates/multiverse amd64 Components [940 B]
Get:22 http://azure.archive.ubuntu.com/ubuntu noble-backports/main amd64 Components [5772 B]
Get:23 http://azure.archive.ubuntu.com/ubuntu noble-backports/universe amd64 Components [10.5 kB]
Get:24 http://azure.archive.ubuntu.com/ubuntu noble-security/main amd64 Packages [1705 kB]
Get:25 http://azure.archive.ubuntu.com/ubuntu noble-security/main Translation-en [268 kB]
Get:26 http://azure.archive.ubuntu.com/ubuntu noble-security/main amd64 Components [42.4 kB]
Get:27 http://azure.archive.ubuntu.com/ubuntu noble-security/universe amd64 Packages [1193 kB]
Get:28 http://azure.archive.ubuntu.com/ubuntu noble-security/universe Translation-en [230 kB]
Get:29 http://azure.archive.ubuntu.com/ubuntu noble-security/universe amd64 Components [74.2 kB]
Get:30 http://azure.archive.ubuntu.com/ubuntu noble-security/restricted amd64 Packages [3006 kB]
Get:31 http://azure.archive.ubuntu.com/ubuntu noble-security/restricted Translation-en [698 kB]
Get:32 http://azure.archive.ubuntu.com/ubuntu noble-security/multiverse Translation-en [9000 B]
Get:33 https://dl.google.com/linux/chrome-stable/deb stable/main amd64 Packages [1212 B]
Fetched 17.0 MB in 2s (8633 kB/s)
Reading package lists...
Reading package lists...
Building dependency tree...
Reading state information...
sshpass is already the newest version (1.09-1).
0 upgraded, 0 newly installed, 0 to remove and 50 not upgraded.
Warning: Permanently added '91.184.242.59' (ED25519) to the list of known hosts.
SSH_OK
REMOTE_MODE_REALITY_TCP443_FALLBACK_ONLY
AMNEZIAWG_NOT_MODIFIED
CHECK_TCP_443
TCP443_FREE
Get:1 https://download.docker.com/linux/ubuntu noble InRelease [48.5 kB]
Get:2 http://security.ubuntu.com/ubuntu noble-security InRelease [126 kB]
Hit:3 https://ppa.launchpadcontent.net/amnezia/ppa/ubuntu noble InRelease
Hit:4 http://archive.ubuntu.com/ubuntu noble InRelease
Get:5 http://archive.ubuntu.com/ubuntu noble-updates InRelease [126 kB]
Get:6 http://security.ubuntu.com/ubuntu noble-security/main amd64 Packages [1,705 kB]
Get:7 http://security.ubuntu.com/ubuntu noble-security/main Translation-en [268 kB]
Get:8 http://security.ubuntu.com/ubuntu noble-security/main amd64 Components [42.4 kB]
Get:9 http://security.ubuntu.com/ubuntu noble-security/universe amd64 Packages [1,193 kB]
Get:10 http://security.ubuntu.com/ubuntu noble-security/universe Translation-en [230 kB]
Get:11 http://security.ubuntu.com/ubuntu noble-security/universe amd64 Components [74.2 kB]
Get:12 http://archive.ubuntu.com/ubuntu noble-backports InRelease [126 kB]
Get:13 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 Packages [2,050 kB]
Get:14 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 Components [177 kB]
Get:15 http://archive.ubuntu.com/ubuntu noble-updates/universe amd64 Packages [1,694 kB]
Get:16 http://archive.ubuntu.com/ubuntu noble-updates/universe amd64 Components [386 kB]
Get:17 http://archive.ubuntu.com/ubuntu noble-updates/multiverse amd64 Components [940 B]
Get:18 http://archive.ubuntu.com/ubuntu noble-backports/main amd64 Components [5,772 B]
Get:19 http://archive.ubuntu.com/ubuntu noble-backports/universe amd64 Components [10.5 kB]
Fetched 8,265 kB in 1s (5,580 kB/s)
Reading package lists...
Reading package lists...
Building dependency tree...
Reading state information...
curl is already the newest version (8.5.0-2ubuntu10.9).
ca-certificates is already the newest version (20240203).
The following additional packages will be installed:
  libpython3-stdlib libssl3t64 python3-minimal
Suggested packages:
  python3-doc python3-tk python3-venv zip
The following NEW packages will be installed:
  unzip
The following packages will be upgraded:
  libpython3-stdlib libssl3t64 openssl python3 python3-minimal
5 upgraded, 1 newly installed, 0 to remove and 254 not upgraded.
Need to get 3,179 kB of archives.
After this operation, 390 kB of additional disk space will be used.
Get:1 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 python3-minimal amd64 3.12.3-0ubuntu2.1 [27.4 kB]
Get:2 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 python3 amd64 3.12.3-0ubuntu2.1 [23.0 kB]
Get:3 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 libpython3-stdlib amd64 3.12.3-0ubuntu2.1 [10.1 kB]
Get:4 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 libssl3t64 amd64 3.0.13-0ubuntu3.9 [1,941 kB]
Get:5 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 openssl amd64 3.0.13-0ubuntu3.9 [1,002 kB]
Get:6 http://archive.ubuntu.com/ubuntu noble-updates/main amd64 unzip amd64 6.0-28ubuntu4.1 [174 kB]
Fetched 3,179 kB in 0s (14.0 MB/s)
(Reading database ... (Reading database ... 5%(Reading database ... 10%(Reading database ... 15%(Reading database ... 20%(Reading database ... 25%(Reading database ... 30%(Reading database ... 35%(Reading database ... 40%(Reading database ... 45%(Reading database ... 50%(Reading database ... 55%(Reading database ... 60%(Reading database ... 65%(Reading database ... 70%(Reading database ... 75%(Reading database ... 80%(Reading database ... 85%(Reading database ... 90%(Reading database ... 95%(Reading database ... 100%(Reading database ... 86361 files and directories currently installed.)
Preparing to unpack .../python3-minimal_3.12.3-0ubuntu2.1_amd64.deb ...
Unpacking python3-minimal (3.12.3-0ubuntu2.1) over (3.12.3-0ubuntu2) ...
Setting up python3-minimal (3.12.3-0ubuntu2.1) ...
(Reading database ... (Reading database ... 5%(Reading database ... 10%(Reading database ... 15%(Reading database ... 20%(Reading database ... 25%(Reading database ... 30%(Reading database ... 35%(Reading database ... 40%(Reading database ... 45%(Reading database ... 50%(Reading database ... 55%(Reading database ... 60%(Reading database ... 65%(Reading database ... 70%(Reading database ... 75%(Reading database ... 80%(Reading database ... 85%(Reading database ... 90%(Reading database ... 95%(Reading database ... 100%(Reading database ... 86361 files and directories currently installed.)
Preparing to unpack .../python3_3.12.3-0ubuntu2.1_amd64.deb ...
Unpacking python3 (3.12.3-0ubuntu2.1) over (3.12.3-0ubuntu2) ...
Preparing to unpack .../libpython3-stdlib_3.12.3-0ubuntu2.1_amd64.deb ...
Unpacking libpython3-stdlib:amd64 (3.12.3-0ubuntu2.1) over (3.12.3-0ubuntu2) ...
Preparing to unpack .../libssl3t64_3.0.13-0ubuntu3.9_amd64.deb ...
Unpacking libssl3t64:amd64 (3.0.13-0ubuntu3.9) over (3.0.13-0ubuntu3.4) ...
Setting up libssl3t64:amd64 (3.0.13-0ubuntu3.9) ...
(Reading database ... (Reading database ... 5%(Reading database ... 10%(Reading database ... 15%(Reading database ... 20%(Reading database ... 25%(Reading database ... 30%(Reading database ... 35%(Reading database ... 40%(Reading database ... 45%(Reading database ... 50%(Reading database ... 55%(Reading database ... 60%(Reading database ... 65%(Reading database ... 70%(Reading database ... 75%(Reading database ... 80%(Reading database ... 85%(Reading database ... 90%(Reading database ... 95%(Reading database ... 100%(Reading database ... 86361 files and directories currently installed.)
Preparing to unpack .../openssl_3.0.13-0ubuntu3.9_amd64.deb ...
Unpacking openssl (3.0.13-0ubuntu3.9) over (3.0.13-0ubuntu3.4) ...
Selecting previously unselected package unzip.
Preparing to unpack .../unzip_6.0-28ubuntu4.1_amd64.deb ...
Unpacking unzip (6.0-28ubuntu4.1) ...
Setting up unzip (6.0-28ubuntu4.1) ...
Setting up openssl (3.0.13-0ubuntu3.9) ...
Setting up libpython3-stdlib:amd64 (3.12.3-0ubuntu2.1) ...
Setting up python3 (3.12.3-0ubuntu2.1) ...
Processing triggers for libc-bin (2.39-0ubuntu8.3) ...
Processing triggers for man-db (2.12.0-4build2) ...

Running kernel seems to be up-to-date.

Restarting services...
 /etc/needrestart/restart.d/systemd-manager
 systemctl restart packagekit.service ssh.service systemd-journald.service systemd-resolved.service systemd-timesyncd.service systemd-udevd.service udisks2.service

Service restarts being deferred:
 systemctl restart systemd-logind.service

No containers need to be restarted.

User sessions running outdated binaries:
 root @ user manager service: systemd[19265]

No VM guests are running outdated hypervisor (qemu) binaries on this host.
XRAY_INSTALL_START
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
100 31219  100 31219    0     0   326k      0 --:--:-- --:--:-- --:--:--  326k
tput: No value for $TERM and no -T specified
tput: No value for $TERM and no -T specified
tput: No value for $TERM and no -T specified
tput: No value for $TERM and no -T specified
get release list success
get release list success
info: Installing Xray v26.3.27 for x86_64
Downloading Xray archive: https://github.com/XTLS/Xray-core/releases/download/v26.3.27/Xray-linux-64.zip
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
 95 20.1M   95 19.2M    0     0  17.8M      0  0:00:01  0:00:01 --:--:-- 17.8M100 20.1M  100 20.1M    0     0  18.1M      0  0:00:01  0:00:01 --:--:-- 26.9M
ok.
Downloading verification file for Xray archive: https://github.com/XTLS/Xray-core/releases/download/v26.3.27/Xray-linux-64.zip.dgst
ok.
info: Extract the Xray package to /tmp/tmp.wlqxTeXYIy and prepare it for installation.
rm: cannot remove '/etc/systemd/system/xray.service.d/10-donot_touch_multi_conf.conf': No such file or directory
rm: cannot remove '/etc/systemd/system/xray@.service.d/10-donot_touch_multi_conf.conf': No such file or directory
info: Systemd service files have been installed successfully!
warning: The following are the actual parameters for the xray service startup.
warning: Please make sure the configuration file path is correctly set.
# /etc/systemd/system/xray.service
[Unit]
Description=Xray Service
Documentation=https://github.com/xtls
After=network.target nss-lookup.target

[Service]
User=nobody
CapabilityBoundingSet=CAP_NET_ADMIN CAP_NET_BIND_SERVICE
AmbientCapabilities=CAP_NET_ADMIN CAP_NET_BIND_SERVICE
NoNewPrivileges=true
ExecStart=/usr/local/bin/xray run -config /usr/local/etc/xray/config.json
Restart=on-failure
RestartPreventExitStatus=23
LimitNPROC=10000
LimitNOFILE=1000000
RuntimeDirectory=xray
RuntimeDirectoryMode=0755

[Install]
WantedBy=multi-user.target

# /etc/systemd/system/xray.service.d/10-donot_touch_single_conf.conf
# In case you have a good reason to do so, duplicate this file in the same directory and make your customizes there.
# Or all changes you made will be lost!  # Refer: https://www.freedesktop.org/software/systemd/man/systemd.unit.html
[Service]
ExecStart=
ExecStart=/usr/local/bin/xray run -config /usr/local/etc/xray/config.json

installed: /usr/local/bin/xray
installed: /usr/local/share/xray/geoip.dat
installed: /usr/local/share/xray/geosite.dat
installed: /usr/local/etc/xray/config.json
installed: /var/log/xray/
installed: /var/log/xray/access.log
installed: /var/log/xray/error.log
installed: /etc/systemd/system/xray.service
installed: /etc/systemd/system/xray@.service
removed: /tmp/tmp.wlqxTeXYIy
info: Xray v26.3.27 is installed.
You may need to execute a command to remove dependent software: apt purge curl unzip
Created symlink /etc/systemd/system/multi-user.target.wants/xray.service → /etc/systemd/system/xray.service.
info: Enable and start the Xray service
XRAY_INSTALL_DONE
XRAY_CONFIG_BACKED_UP
XRAY_CONFIG_FAMILY_READY
Rules updated
Rules updated (v6)
Firewall not enabled (skipping reload)
TCP443_FIREWALL_RULE_ATTEMPTED
failed
```
