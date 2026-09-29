#!/bin/bash

# Navigate to here:


# FOR US-NR1 (tile h09v04)
lftp -e "
set sftp:connect-program 'ssh -a -x -oPort=2051 -oPreferredAuthentications=password';
open sftp://lewiskunik@ftp.gportal.jaxa.jp;
mirror --verbose --only-newer --include-glob '*_T0409_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2019/07/30/ ./2019/07/30/;
mirror --verbose --only-newer --include-glob '*_T0409_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2019/07/31/ ./2019/07/31/;
bye
"

lftp -e "
set sftp:connect-program 'ssh -a -x -oPort=2051 -oPreferredAuthentications=password';
open sftp://lewiskunik@ftp.gportal.jaxa.jp;
mirror --verbose --only-newer --include-glob '*_T0409_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2019/12/ ./2019/12/;
bye
"

# FOR US-NR1 (tile h09v05)
lftp -e "
set sftp:connect-program 'ssh -a -x -oPort=2051 -oPreferredAuthentications=password';
open sftp://lewiskunik@ftp.gportal.jaxa.jp;
mirror --verbose --only-newer --include-glob '*_T0509_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2019/12/ ./2019/12/;
bye
"

# FOR US-NR1 (tile h10v04)
lftp -e "
set sftp:connect-program 'ssh -a -x -oPort=2051 -oPreferredAuthentications=password';
open sftp://lewiskunik@ftp.gportal.jaxa.jp;
mirror --verbose --only-newer --include-glob '*_T0410_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2018/10/28/ ./2018/10/28/;
mirror --verbose --only-newer --include-glob '*_T0410_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2018/10/29/ ./2018/10/29/;
mirror --verbose --only-newer --include-glob '*_T0410_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2018/10/30/ ./2018/10/30/;
mirror --verbose --only-newer --include-glob '*_T0410_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2018/10/31/ ./2018/10/31/;
bye
"

# FOR OSBS (tile h10v06)
lftp -e "
set sftp:connect-program 'ssh -a -x -oPort=2051 -oPreferredAuthentications=password';
open sftp://lewiskunik@ftp.gportal.jaxa.jp;
mirror --verbose --only-newer --include-glob '*_T0610_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2022/12/26/ ./2022/12/26/;
mirror --verbose --only-newer --include-glob '*_T0610_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2022/12/27/ ./2022/12/27/;
mirror --verbose --only-newer --include-glob '*_T0610_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2022/12/28/ ./2022/12/28/;
mirror --verbose --only-newer --include-glob '*_T0610_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2022/12/29/ ./2022/12/29/;
mirror --verbose --only-newer --include-glob '*_T0610_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2022/12/30/ ./2022/12/30/;
mirror --verbose --only-newer --include-glob '*_T0610_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2022/12/31/ ./2022/12/31/;
bye
"

# FOR Ca-Obs (tile h11v03)
lftp -e "
set sftp:connect-program 'ssh -a -x -oPort=2051 -oPreferredAuthentications=password';
open sftp://lewiskunik@ftp.gportal.jaxa.jp;
mirror --verbose --only-newer --include-glob '*_T0311_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2021/08/ ./2021/08/;
bye
"


lftp -e "
set sftp:connect-program 'ssh -a -x -oPort=2051 -oPreferredAuthentications=password';
open sftp://lewiskunik@ftp.gportal.jaxa.jp;
# mirror --verbose --only-newer --include-glob '*_T0311_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2022/08/25/ ./2022/08/25/;
# mirror --verbose --only-newer --include-glob '*_T0311_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2022/08/26/ ./2022/08/26/;
# mirror --verbose --only-newer --include-glob '*_T0311_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2022/08/27/ ./2022/08/27/;
# mirror --verbose --only-newer --include-glob '*_T0311_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2022/08/28/ ./2022/08/28/;
# mirror --verbose --only-newer --include-glob '*_T0311_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2022/08/29/ ./2022/08/29/;
mirror --verbose --only-newer --include-glob '*_T0311_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2022/08/30/ ./2022/08/30/;
mirror --verbose --only-newer --include-glob '*_T0311_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2022/08/31/ ./2022/08/31/;
bye
"

# FOR US-UMB (tile h12v04)
lftp -e "
set sftp:connect-program 'ssh -a -x -oPort=2051 -oPreferredAuthentications=password';
open sftp://lewiskunik@ftp.gportal.jaxa.jp;
mirror --verbose --only-newer --include-glob '*_T0412_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2019/12/ ./2019/12/;
bye
"


# FOR DEJU (tile h11v02)
lftp -e "
set sftp:connect-program 'ssh -a -x -oPort=2051 -oPreferredAuthentications=password';
open sftp://lewiskunik@ftp.gportal.jaxa.jp;
mirror --verbose --only-newer --include-glob '*_T0211_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2021/08/ ./2021/08/;
bye
"

lftp -e "
set sftp:connect-program 'ssh -a -x -oPort=2051 -oPreferredAuthentications=password';
open sftp://lewiskunik@ftp.gportal.jaxa.jp;
# mirror --verbose --only-newer --include-glob '*_T0211_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2021/07/01/ ./2021/07/01/;
# mirror --verbose --only-newer --include-glob '*_T0211_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2021/07/02/ ./2021/07/02/;
# mirror --verbose --only-newer --include-glob '*_T0211_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2021/07/03/ ./2021/07/03/;
# mirror --verbose --only-newer --include-glob '*_T0211_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2021/07/04/ ./2021/07/04/;
# mirror --verbose --only-newer --include-glob '*_T0211_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2021/07/05/ ./2021/07/05/;
# mirror --verbose --only-newer --include-glob '*_T0211_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2021/07/06/ ./2021/07/06/;
# mirror --verbose --only-newer --include-glob '*_T0211_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2021/07/07/ ./2021/07/07/;
# mirror --verbose --only-newer --include-glob '*_T0211_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2021/07/08/ ./2021/07/08/;
# mirror --verbose --only-newer --include-glob '*_T0211_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2021/07/09/ ./2021/07/09/;
# mirror --verbose --only-newer --include-glob '*_T0211_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2021/07/10/ ./2021/07/10/;
# mirror --verbose --only-newer --include-glob '*_T0211_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2021/07/11/ ./2021/07/11/;
# mirror --verbose --only-newer --include-glob '*_T0211_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2021/07/12/ ./2021/07/12/;
# mirror --verbose --only-newer --include-glob '*_T0211_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2021/07/13/ ./2021/07/13/;
# mirror --verbose --only-newer --include-glob '*_T0211_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2021/07/14/ ./2021/07/14/;
# mirror --verbose --only-newer --include-glob '*_T0211_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2021/07/15/ ./2021/07/15/;
# mirror --verbose --only-newer --include-glob '*_T0211_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2021/07/16/ ./2021/07/16/;
# mirror --verbose --only-newer --include-glob '*_T0211_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2021/07/17/ ./2021/07/17/;
# mirror --verbose --only-newer --include-glob '*_T0211_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2021/07/18/ ./2021/07/18/;
# mirror --verbose --only-newer --include-glob '*_T0211_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2021/07/19/ ./2021/07/19/;
# mirror --verbose --only-newer --include-glob '*_T0211_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2021/07/20/ ./2021/07/20/;
# mirror --verbose --only-newer --include-glob '*_T0211_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2021/07/21/ ./2021/07/21/;
# mirror --verbose --only-newer --include-glob '*_T0211_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2021/07/22/ ./2021/07/22/;
# mirror --verbose --only-newer --include-glob '*_T0211_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2021/07/23/ ./2021/07/23/;
# mirror --verbose --only-newer --include-glob '*_T0211_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2021/07/24/ ./2021/07/24/;
# mirror --verbose --only-newer --include-glob '*_T0211_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2021/07/25/ ./2021/07/25/;
# mirror --verbose --only-newer --include-glob '*_T0211_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2021/07/26/ ./2021/07/26/;
# mirror --verbose --only-newer --include-glob '*_T0211_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2021/07/27/ ./2021/07/27/;
# mirror --verbose --only-newer --include-glob '*_T0211_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2021/07/28/ ./2021/07/28/;
# mirror --verbose --only-newer --include-glob '*_T0211_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2021/07/29/ ./2021/07/29/;
mirror --verbose --only-newer --include-glob '*_T0211_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2021/07/30/ ./2021/07/30/;
mirror --verbose --only-newer --include-glob '*_T0211_L2SG_RSRFQ*.h5' /standard/GCOM-C/GCOM-C.SGLI/L2.LAND.RSRF/3/2021/07/31/ ./2021/07/31/;
bye
"