# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 23:07:53 2020

@author: rolly
"""
from module import kelas
from numba import jit
import pandas as pd
import config
import pymysql

@jit(nopython=True)
def auth(data):
    if kelas.getKodeDosen(data[0]) == '':
        ret=False
    else:
        ret=True
    return ret

@jit(nopython=True)
def replymsg(num,msg):
    kodedosen=msg.split(' ')[-1].upper()
    df=getDataframe()
    df=selectTahunID(df,'20191')
    df=selectKodeDosen(df,kodedosen)
    return toString(df)

@jit(nopython=True)
def dbConnect():
    db=pymysql.connect(user=config.siap_db_user, password=config.siap_db_password, database=config.siap_db_name, host=config.siap_db_host)
    return db

@jit(nopython=True)
def getDataframe():
    db=dbConnect()
    sql="select `jdl`.`DosenID` AS `DosenID`,(case when (substr(`jdl`.`ProdiID`,2,2) = 13) then 'D3TI' when (substr(`jdl`.`ProdiID`,2,2) = 14) then 'D4TI' when (substr(`jdl`.`ProdiID`,2,2) = 23) then 'D3MI' when (substr(`jdl`.`ProdiID`,2,2) = 33) then 'D3AK' when (substr(`jdl`.`ProdiID`,2,2) = 34) then 'D4AK' when (substr(`jdl`.`ProdiID`,2,2) = 43) then 'D3MB' when (substr(`jdl`.`ProdiID`,2,2) = 44) then 'D4MB' when (substr(`jdl`.`ProdiID`,2,2) = 53) then 'D3LB' when (substr(`jdl`.`ProdiID`,2,2) = 54) then 'D4LB' end) AS `ProdiID`,`dsn`.`Nama` AS `nama_dosen`,`jdl`.`JadwalID` AS `JadwalID`,`jdl`.`MKKode` AS `MKKode`,`jdl`.`Nama` AS `Nama`,`jdl`.`TahunID` AS `TahunID`,(case when (`jdl`.`NamaKelas` = 1) then 'A' when (`jdl`.`NamaKelas` = 2) then 'B' when (`jdl`.`NamaKelas` = 3) then 'C' when (`jdl`.`NamaKelas` = 4) then 'D' when (`jdl`.`NamaKelas` = 5) then 'E' when (`jdl`.`NamaKelas` = 6) then 'F' when (`jdl`.`NamaKelas` = 7) then 'G' when (`jdl`.`NamaKelas` = 8) then 'H' when (`jdl`.`NamaKelas` = 9) then 'I' end) AS `NamaKelas`,`jdl`.`Final` AS `Final`,(select count(`krs`.`MhswID`) from `simak_trn_krs` `krs` where (`krs`.`JadwalID` = `jdl`.`JadwalID`)) AS `JmlMhs`,(select count(`krs`.`MhswID`) from `simak_trn_krs` `krs` where ((`krs`.`JadwalID` = `jdl`.`JadwalID`) and (`krs`.`UAS` <> '0'))) AS `JmlGrade`,(((select count(`krs`.`MhswID`) from `simak_trn_krs` `krs` where ((`krs`.`JadwalID` = `jdl`.`JadwalID`) and (`krs`.`UAS` <> '0'))) / (select count(`krs`.`MhswID`) from `simak_trn_krs` `krs` where (`krs`.`JadwalID` = `jdl`.`JadwalID`))) * 100) AS `Presentase` from (`simak_trn_jadwal` `jdl` join `simak_mst_dosen` `dsn`) where (`jdl`.`DosenID` = `dsn`.`Login`) order by `dsn`.`Nama`,`ProdiID`,`jdl`.`Nama`,`jdl`.`NamaKelas`"
    with db:
        df = pd.read_sql(sql, con=db)
    return df

@jit(nopython=True)
def selectTahunID(df,tahunid):
    df=df[df['TahunID']==tahunid]
    return df

@jit(nopython=True)
def selectKodeDosen(df,kodedosen):
    df=df[df['DosenID']==kodedosen]
    return df[['Nama','NamaKelas','Final','Presentase']].reset_index(drop=True)

@jit(nopython=True)
def toString(df):
    return df.to_string()