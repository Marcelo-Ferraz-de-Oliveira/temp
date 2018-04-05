import pexpect
from datetime import datetime
smll11=['FLRY3',
'QUAL3',
'ESTC3',
'BRAP4',
'SULA11',
'TIET11',
'TOTS3',
'CVCB3',
'ODPV3',
'MRVE3',
'SAPR4',
'GOAU4',
'HGTX3',
'IGTA3',
'CYRE3',
'BTOW3',
'CPLE6',
'ALUP11',
'MRFG3',
'MGLU3',
'CESP6',
'SMTO3',
'CSMG3',
'MYPK3',
'LINX3',
'DTEX3',
'GRND3',
'POMO4',
'BEEF3',
'ECOR3',
'LIGT3',
'ALPA4',
'VVAR11',
'ALSC3',
'ARZZ3',
'ELPL4',
'MPLU3',
'GOLL4',
'VLID3',
'CGAS5',
'BRPR3',
'EZTC3',
'WIZS3',
'TUPY3',
'RAPT4',
'SLCE3',
'SEER3',
'ABCB4',
'EVEN3',
'AALR3',
'RLOG3',
'MEAL3',
'LEVE3',
'ANIM3',
'QGEP3',
'FESA4',
'MILS3',
'TCSA3',
'DIRR3',
'GFSA3',
'HBOR3',
'JHSF3',
'CARD3',
'RSID3',
'ABCB10']


telconn = pexpect.spawn("telnet datafeed1.cedrofinances.com.br 81")
telconn.logfile_read=open("smll11_"+str(datetime.now().date())+".log","wb")
telconn.delaybeforesend = 0
telconn.expect(".")
telconn.sendline("")
telconn.expect(":")
telconn.sendline("mfogoiania")
telconn.expect(":")
telconn.sendline("102030")
telconn.expect("d")
for ativo in smll11:
        telconn.sendline("gqt "+ativo+" S 50000")
        telconn.expect(":E\r\n")  
    