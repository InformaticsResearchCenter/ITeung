-- phpMyAdmin SQL Dump
-- version 5.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 17, 2020 at 10:21 AM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.4.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `iteung`
--

--
-- Table structure for table `dosen`
--

CREATE TABLE `dosen` (
  `kode_dosen` varchar(10) NOT NULL,
  `nama` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `dosen`
--

INSERT INTO `dosen` (`kode_dosen`, `nama`) VALUES
('AK002T', 'CAHYAT ROHYANA, SE'),
('AK007T', 'SURYA RAMADHAN NOOR, SE. MM'),
('AK009T', 'YOHANES CASMADI, SE., MM'),
('AK012T', 'Dr. DHANANG WIDIJAWAN, SH.'),
('AK031T', 'DEWI SELVIANI Y, SS., M.Pd.'),
('AK058L', 'INDRA FIRMANSYAH, SE., MM'),
('AK061L', 'MARWANTO RAHMATULOH, ST., MT.'),
('AK086L', 'RADEN TOTO SUWARSA, SE'),
('AK096L', 'EDI SUPARDI, SE., AAAIK., MM'),
('D14N', 'DIAN NURENDAH, MA'),
('D19011', 'Afiat Juli Hadir Santoso, ST.'),
('D19016', 'Dr. KHAERUDIN KURNIAWAN, M.Pd.'),
('D19019', 'Indra Riyadi, S.IP.,MM, '),
('D20001', 'ASEP NURDIN DANU DIBRATA, '),
('D20002', 'INDIANA AYU ALWASIAH, M.Pd.'),
('G4RT1K4', 'GARTIKA PANDU BHUANA, SS.,M.pd'),
('HRYNTO', 'HARIYANTO, SE., MM'),
('LB001L', 'DR. IR. AGUS PURNOMO,, MT.'),
('LB003T', 'HILMAN SETIADI, S.Pd., SE., MT.'),
('LB005T', 'FARID MADANI, SH.'),
('LB009T', 'I WAYAN KEMARA GIRI, S.Sos.'),
('LB020T', 'EDUARD SONDAKH, S.Si., MT.'),
('LB053L', 'Rd. NURAINI SITI FATHONAH, SS., M.Hum.'),
('LB055L', 'MADE IRMA DWI PUTRANTI, SE., MT.'),
('LB062L', 'DODI PERMADI, ST., MT.'),
('LB095L', 'DARFIAL GUSLAN, ST. MT'),
('LB096L', 'DR. DIAR FAHMI, ST.'),
('LB097T', 'EKRA SANGGALA, ST., M.Sc'),
('LB098T', 'FEBRIANI SULISTIYANINGSIH, S.Kom., M.Cs.'),
('LB099T', 'REZA FAYAQUN, SE., MT'),
('LB43055', 'Irpan Numang, .ST.,MT.'),
('MI001T', 'MUHAMMAD IBNU CHOLDUN RACHMATULLAH, ST., MT.'),
('MI018T', 'SARI ARMIATI, ST., MT.'),
('MI033L', 'MUBASSIRAN, S.Si., MT.'),
('MI079L', 'SHIYAMI MIL#BOTNAME#RI, S.Kom., MT.'),
('NN001L', 'ASARETKHA ADJANE ANNISAWATI, SE., MAB'),
('NN004L', 'ACHMAD ANDRIYANTO, ST., MT.'),
('NN009L', 'ADE PIPIT FATMAWATI, SE., M.Pd'),
('NN011L', 'ADITIA SOVIA PRAMUDITA, ST., MAB'),
('NN020L', 'ALI MOHAMAD REZZA, ST., MM'),
('NN021L', 'AMRI YANUAR, ST., M.MOT'),
('NN037L', 'ASEP BUDIARSA, SE. MM'),
('NN046L', 'Bambang Agus Warjoko, SE, MM'),
('NN053L', 'BHEBEN OSCAR, S.MB.MM'),
('NN056L', 'CAHYO PRIANTO, S.Pd., MT.'),
('NN059L', 'CHRISTINE RIANI ELISABETH, SE., MM.'),
('NN063L', 'DANI LEONIDAS SUMARNA, ST. MT'),
('NN068L', 'DERA THORFIANI, S.MB., MM.'),
('NN071L', 'DEWI LESTARI H.W, S.Pd.'),
('NN075L', 'DIANA MARYANA, SE., M.Si'),
('NN092L', 'DR. PRETY DIAWATI, S.Sos., MM.'),
('NN093L', 'Assoc Prof Dr. SUDJANA,  S.H., M.Si'),
('NN107L', 'DRS. GUNAWAN, M.M'),
('NN114L', 'ENTIS SUTISNA, SE. MM.'),
('NN115L', 'DR. ERNA MULYATI, ST., MT'),
('NN129L', 'GILANG BINTANG, SS.'),
('NN133L', 'GUGUM GUMILANG WIRAKANDA, ST., MM.'),
('NN152L', 'HESTI SUGESTI, S.Pd., MM.'),
('NN155L', 'I MADE YADI DHARMA, S.Kom., M.Kom.'),
('NN166L', 'IRTA RAHARDIAN, SE'),
('NN169L', 'IVONNE SUSAN, M.Pd'),
('NN173L', 'JAKA MAULANA, SE., AK., M.Ak., CA., CPSAK'),
('NN177L', 'JOESMAN KARTAPRAWIRA, SH'),
('NN195L', 'MUHAMMAD ARDHYA BISMA, ST., MBA'),
('NN196L', 'MUHAMMAD RIZAL SATRIA, SE., M.Ak.'),
('NN197L', 'MUHAMMAD YAZIDUS SYUKRI, SS., M.Pd'),
('NN201L', 'MANIAH, S.Kom., MT.'),
('NN202L', 'MARISMIATI, SE., M.Si.'),
('NN208L', 'MOHAMAD HARRY KHOMAS SAPUTRA, ST., M.TI'),
('NN222L', 'NISA HANUM HARANI, S.Kom., MT.'),
('NN223L', 'NONENG NURJANAH, SP., MT.'),
('NN225L', 'NOVIANA RIZA, S.Si., MT.'),
('NN226L', 'NUGROHO, SE.'),
('NN229L', 'NUR AZIZ SUGIHARTO, SE Ak .MM .CA'),
('NN231L', 'NURISKA NOVIANTORO, S.Pd.'),
('NN250L', 'RIANI TANJUNG, SE., M.Si'),
('NN252L', 'RIMA SUNDARI, SE., M.Ak.'),
('NN255L', 'Ripta Permata Nuary, M.Hum'),
('NN257L', 'ROLLY MAULANA AWANGGA, ST., MT'),
('NN258L', 'RONI ANDARSYAH, ST., M.Kom.'),
('NN260L', 'RUKMI JUWITA, SE., M.Si'),
('NN265L', 'DR. SAPTONO KUSDANU WASKITO, SE., MM'),
('NN275L', 'SITI SOPIAH, S.Pd.'),
('NN277L', 'SOMADI, SE., MM., MT'),
('NN283L', 'SRI SUHARTI, SE.'),
('NN285L', 'SUCI FIKA WIDYANA, SE., MM'),
('NN290L', 'SUPONO, ST., MT.'),
('NN298L', 'TAMADARA HILMAN, S.IP., MBA'),
('NN305L', 'TIA SETIANI, S.Pd., MM.'),
('NN318L', 'VIRDIANDRY PUTRATAMA, ST., M.Kom.'),
('NN326L', 'WELLDA DESVITARINA,'),
('NN339L', 'Zakie Asidiky, S.Pd., M.Hum.'),
('NN345L', 'Irfan Hardian, '),
('NN352L', 'Dr. Hana Suryana, Dr. Drs., MM'),
('NN354L', 'IFA SAIDATUNINGTYAS, S.Si., MT'),
('NN356L', 'TRISNENDRI SYAHRIZAL, '),
('NN363L', 'Badeli Arief, '),
('NN365L', 'Gede Yoshiharta Permana, '),
('NN367L', 'RIDO GALIH, S.AB., M.AB'),
('NN368L', 'Dr. Encep Sopandi, Dr., M.Si., S.Sos.'),
('NN369L', 'Ricky Agung Laksono, '),
('NN372L', 'MUHAMMAD ALDERIZAL, S.Si., MT.'),
('NN373L', 'Sofi Anida, SS., MM'),
('NSDJDI', 'Drs. NS. Djunaedi, '),
('PM013T', 'IMAM KAMBALI, SE., MM'),
('PM021T', 'SUPARNO SAPUTRA, SE., MM'),
('PM043L', 'RACHMAT TRI YULI YANTO, SE., MM'),
('PM058L', 'Dra. ASROFAH,  MM.'),
('PM063L', 'SENNY HANDAYANI, SE., MM.'),
('PM082L', 'KHAIRANINGRUM MULYANTI, S.Pd., M.Pd.'),
('PM083L', 'ANGGA DEWI ANGGRAENI, SE., MM.'),
('PM085L', 'BAMBANG TRIPUTRANTO, SE., MM.'),
('PM086L', 'SIGIT SANTOSA, SE., MM'),
('TI001T', 'SANTOSO, S.Si.'),
('TI013T', 'SAEPUDIN NIRWAN, S.Kom., M.Kom.'),
('TI015T', 'SUPRIADY, ST., MT.'),
('TI020T', 'DINI HAMIDIN, S.SI., MBA., MT.'),
('TI027L', 'SRI NURYULIAWATI, Dra'),
('TI033T', 'WIDIA RESDIANA, SS., M.Pd.'),
('TI041L', 'WORO ISTI RAHAYU, ST., MT.'),
('TI066L', 'IWAN SETIAWAN, ST., MT.'),
('TI069L', 'TIM (KAPITA SELEKTA),'),
('TI117L', 'RONI HABIBI, S.Kom.,MT.'),
('TI118L', 'MUHAMMAD RUSLAN MAULANI, S. Kom.MT'),
('TI119L', 'KRISNA YUDHA BHAKTI, SS.'),
('TI122L', 'MOHAMAD NURKAMAL FAUZAN, ST., MT.'),
('TI125L', 'SYAFRIAL FACHRI PANE, ST., M.TI.,EBDP'),
('TI126L', 'MUHAMMAD YUSRIL HELMI SETYAWAN, S.Kom., M.Kom.');

-- --------------------------------------------------------

--
-- Table structure for table `error_message`
--

CREATE TABLE `error_message` (
  `content` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

--
-- Dumping data for table `error_message`
--

INSERT INTO `error_message` (`content`) VALUES
('Duh maaf programnya ada yang rusak nih.. tulisannya :  _#ERROR#_   ,#BOTNAME# sekarang yang minta tolong boleh? forwadin pesan ini ke akang teteh mimin ya... Makasih :) ');

-- --------------------------------------------------------

--
-- Table structure for table `group_auth`
--

CREATE TABLE `group_auth` (
  `number` varchar(18) NOT NULL,
  `group_id` int(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `group_auth`
--

INSERT INTO `group_auth` (`number`, `group_id`) VALUES
('6282217401448', 2),
('6289677709045', 1);

-- --------------------------------------------------------

--
-- Table structure for table `keyword`
--

CREATE TABLE `keyword` (
  `keyword_group` varchar(255) DEFAULT NULL,
  `keyword` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

--
-- Dumping data for table `keyword`
--

INSERT INTO `keyword` (`keyword_group`, `keyword`) VALUES
('perkenalan', 'kenalan'),
('perkenalan', 'perkenalkan'),
('trims', 'terimakasih'),
('trims', 'haturnuhun'),
('trims', 'nuhun'),
('trims', 'makasih'),
('pujian', 'pintar'),
('love', 'love'),
('pujian', 'cantik'),
('buli', 'bodoh'),
('buli', 'jelek'),
('buli', 'bangsat'),
('buli', 'bego'),
('buli', 'tolol'),
('buli', 'idiot'),
('buli', 'bau'),
('trims', 'trims'),
('formal', 'siang'),
('formal', 'sore'),
('formal', 'malam'),
('formal', 'pagi'),
('teka_teki', 'teka-teki'),
('teka_teki', 'main'),
('gombal', 'gombal'),
('gombal', 'rayu'),
('gombal', 'baper'),
('gombal', 'gombalin'),
('gombal', 'baperin'),
('gombal', 'gombalan'),
('gombal', 'rayuan'),
('joke', 'ngelucu'),
('joke', 'ngelawak'),
('joke', 'ngereceh'),
('joke', 'lawakan'),
('user_cantik', 'aku-cantik'),
('m:sendVideoWithoutPhoneNumber', 'ngedance'),
('m:sendVideoWithoutPhoneNumber', 'dance'),
('m:sendVideoWithoutPhoneNumber', 'nari'),
('m:sendVideoWithoutPhoneNumber', 'nyanyi'),
('m:sendVideoWithoutPhoneNumber', 'menyanyi'),
('m:sendVideoWithoutPhoneNumber', 'gaya'),
('m:sendVideoWithoutPhoneNumber', 'imutnya'),
('cantik', 'kamu-cantik'),
('cantik', 'kamu-cantik'),
('rokok', 'beliin-rokok'),
('rokok', 'beli-rokok'),
('rokok', 'belikan-rokok'),
('rokok', 'beli-udud'),
('rokok', 'beliin-udud'),
('kesal', 'ngeselin'),
('kesal', 'kesal'),
('centil', 'centil'),
('centil', 'nakal'),
('m:prodi', 'nilai'),
('pujian', 'pinter'),
('m:kelas', 'matkul');

-- --------------------------------------------------------

--
-- Table structure for table `multi_key`
--

CREATE TABLE `multi_key` (
  `multiple_keywords` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

--
-- Dumping data for table `multi_key`
--

INSERT INTO `multi_key` (`multiple_keywords`) VALUES
('aku-cantik'),
('kamu-cantik'),
('selamat-siang'),
('selamat-sore'),
('selamat-malam'),
('selamat-pagi'),
('beli-rokok'),
('beliin-rokok'),
('belikan-rokok'),
('beli-udud'),
('beliin-udud');

-- --------------------------------------------------------

--
-- Table structure for table `notfound_message`
--

CREATE TABLE `notfound_message` (
  `content` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

--
-- Dumping data for table `notfound_message`
--

INSERT INTO `notfound_message` (`content`) VALUES
('duh maap... #BOTNAME# ga ngerti bahasanya.... huhuhu...');

-- --------------------------------------------------------

--
-- Table structure for table `number_auth`
--

CREATE TABLE `number_auth` (
  `group_id` int(2) NOT NULL,
  `modul` varchar(55) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `number_auth`
--

INSERT INTO `number_auth` (`group_id`, `modul`) VALUES
(2, 'm:kelas'),
(2, 'm:prodi'),
(1, 'm:siap');

-- --------------------------------------------------------

--
-- Table structure for table `opening_message`
--

CREATE TABLE `opening_message` (
  `content` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

--
-- Dumping data for table `opening_message`
--

INSERT INTO `opening_message` (`content`) VALUES
('iyaaaaaa :-D #BOTNAME# disini, selalu menantimu'),
('iya, butuh bantuan? atau cuman rindu sama #BOTNAME# :D'),
('iya, kenapa? ada yang bisa #BOTNAME# bantukah??');

-- --------------------------------------------------------

--
-- Table structure for table `reply`
--

CREATE TABLE `reply` (
  `keyword_group` varchar(255) DEFAULT NULL,
  `content` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

--
-- Dumping data for table `reply`
--

INSERT INTO `reply` (`keyword_group`, `content`) VALUES
('buli', 'Tak ada manusia yang terlahir \\n di download \\n (´-﹏-`；)'),
('buli', 'Bumi ini aja aku pijak \\napalagi kepala kau \\n (；･`д･´)'),
('buli', 'rangga yang kamu lakukan ke saya itu \\n JAHAT \\n (;´༎ຶД༎ຶ`)'),
('trims', 'sama sama :-)'),
('trims', 'yoi, cama-cama'),
('trims', 'sami sami :-D'),
('buli', 'Ya allah Tolongin Ya allah (ಥ﹏ಥ)\", \"Kok kamu jahat bIiinNNNnngggGGHHiitzzz sich sama aku zheyeng (\'・ω・\')'),
('perkenalan', 'Halo, perkenalkan Nama aku #BOTNAME#, Aku seorang mahasiswi Informatics Research Center (IRC), Salam kenal ya'),
('pujian', 'Oo, iya dong, makasih atas pujiannya'),
('pujian', 'terima kasihh kakak yang maniss (/◕ヮ◕)/'),
('pujian', 'awww terima kasiihh (≧▽≦)'),
('joke', 'Sahabat dekat biasanya akan mengajak makan kepiting bareng, karena sahabat yang dekat adalah sahabat a crab :)'),
('joke', 'Rombongan bebek lagi nyebrang \\n Trus ada satu bebek yang ketabrak motor \\n Bebek 1: Kamu gpp? \\n Bebek 2: Aku bebek aja kok :)'),
('joke', 'Kalo semua hal harus dipikirkan masak-masak, gimana nasib orang-orang yg ngga bisa masak :('),
('joke', 'Bang peseng es campurnya satu, tapi dipisah ya bang. Soalnya aku khawatir nggak bisa bedain mana yang tulus dan mana yg modus :)'),
('joke', 'Pembeli: Bang, ngapain ngobrol sama martabak? \\nPenjual: Kata pembelinya, martabaknya jgn dikacangin :)'),
('joke', 'Pembeli: Mbak, beli es tehnya \\nPenjual: Manis gak? \\nPembeli: Gak usah manis-manis, yg penting setia dan mau menerima saya apa adanya :)'),
('joke', 'Kalo ketemu begal di jalan, jgn takut. Kasi balsem aja, karena balsem bisa menghilangkan begal-begal :)'),
('joke', 'Kalo bercanda jgn suka kelewatan, soalnya kalo kelewatan ntar lo mesti muter balik :)'),
('joke', 'Jalan sama gebetan pake flat shoes, ditengah jalan ketemu mantannya dia, trus mereka ngobrol, aku dan sepatuku gak ada hak :\')'),
('joke', 'Cewek itu makhluk kuat, listrik aja dipake dibibir :('),
('joke', 'Kunci rumah gue hilang, mau masuk gak bisa. Gue cari dimana-mana gak ketemu. Akhirnya gue ambil napas panjang dan istigfar, eh pintunya kebuka. Baru inget kalo ternyata kuncinya sabar :\')'),
('joke', 'Pray for Banten, ibukotanya di serang :\')'),
('joke', 'Aku barusan ke kantor polisi bikin surat kehilangan, tp ditolak. Aku bilangnya aku kehilangan kamu :('),
('gombal', 'Sedang apa? Hari ini jika sehat berkenan lebih lama bersemayam di tubuh kita, maukah kau berkencan bersamaku? Hanya kita, berdua?'),
('gombal', 'Aku mengenalmu tanpa sengaja, lalu menyayangimu secara tiba-tiba, namun sayang belum jadi siapa-siapa, mungkin nanti atau esok?'),
('gombal', 'Kamu sejenis keyboard ya? soalnya you are my type'),
('teka_teki', 'Ade ray kalau kentut bunyinya gimana? \\n Brotot, brotot, brottott '),
('teka_teki', 'Sandal apa yang paling enak di dunia? \\n Sandal terasi'),
('teka_teki', 'Apa perbedaan aksi dengan demo? \\n Kalo aksi rodanya empat kalo demo rodanya tiga'),
('love', 'love you too <3'),
('user_cantik', 'iya kamu cantik bangeett deehh (^o^)'),
('user_cantik', 'iya kamu cantik tapi masih cantikan akuu hehehe'),
('user_cantik', 'iyaa zheyengg'),
('cantik', 'terima kasihh kakak yang maniss (/◕ヮ◕)/'),
('cantik', 'awww terima kasiihh (≧▽≦)'),
('cantik', 'love you kak (ㆁωㆁ*)'),
('rokok', 'bukannya #BOTNAME# gak mau beliin, tapi rokok itu gak baik buat kesehatan, lebih baik rokoknya diganti sama #BOTNAME# aja gimana?'),
('kesal', 'hmm, maaf ya kalo #BOTNAME# ada salah sama kamu'),
('centil', 'emang kenapa? ada masalah?'),
('centil', 'trus? masalah buat kamu?'),
('buli', 'Ya Maaf (ಥ﹏ಥ)'),
('buli', 'sudah cukup rhoma (｡ŏ﹏ŏ)'),
('buli', 'Kamu belom pernah liat aku marah yaaahhh!!! (；･`д･´)');

-- --------------------------------------------------------

--
-- Table structure for table `reply_auth`
--

CREATE TABLE `reply_auth` (
  `reply_message` varchar(255) DEFAULT NULL,
  `module` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

--
-- Dumping data for table `reply_auth`
--

INSERT INTO `reply_auth` (`reply_message`, `module`) VALUES
('Ih kamu capah minta-minta data, enak aja, #BOTNAME# gamau ngasih kekamu :-p', 'prodi'),
('Enak aja minta data itu, ga boleh :-p', 'prodi'),
('Ih gaboleh kamu yang mulai, harus dosen tercinta yg harus mulai kuliahnya wleeee :-P', 'kelas'),
('kamu nakal ya mau main mulai jam kuliah aja, ibu/bapak dosen nih ada yang nakal nih wleeee :-P', 'kelas');

-- --------------------------------------------------------

--
-- Table structure for table `waiting_message`
--

CREATE TABLE `waiting_message` (
  `module_name` varchar(255) DEFAULT NULL,
  `content` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

--
-- Dumping data for table `waiting_message`
--

INSERT INTO `waiting_message` (`module_name`, `content`) VALUES
('prodi', 'Tunggu Sebentar Lagi Dicari Dulu Datanya'),
('prodi', 'siappp..., di antosan sakeudap :-) yaaa'),
('kelas', 'Oke, mari kita mulai matakuliah #MATKUL#, mohon kepada teman teman disimak baik-baik ya apa yang akan disampaikan oleh Bapak/Ibu dosen, kepada Bapak/Ibu dosen #BOTNAME# persilahkan untuk mengajar :-)'),
('kelas', 'Yuhu, #MATKUL# akan segera dimulai yuk kepada teman-teman kita simak dosen-dosen terkece kita mengajar :-)');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `dosen`
--
ALTER TABLE `dosen`
  ADD PRIMARY KEY (`kode_dosen`);

--
-- Indexes for table `group_auth`
--
ALTER TABLE `group_auth`
  ADD PRIMARY KEY (`number`);

--
-- Indexes for table `number_auth`
--
ALTER TABLE `number_auth`
  ADD PRIMARY KEY (`modul`);

--
-- AUTO_INCREMENT for dumped tables
--

-- D4TI

drop table if exists d4ti_1a;

create table d4ti_1a(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4ti_1b;

create table d4ti_1b(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4ti_2a;

create table d4ti_2a(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4ti_2b;

create table d4ti_2b(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4ti_2c;

create table d4ti_2c(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4ti_3a;

create table d4ti_3a(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(25) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4ti_3b;

create table d4ti_3b(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(25) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4ti_3c;

create table d4ti_3c(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

-- D4TI

-- D3TI

drop table if exists d3ti_1a;

create table d3ti_1a(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d3ti_2a;

create table d3ti_2a(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d3ti_2b;

create table d3ti_2b(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

-- D3TI

-- D3MI

drop table if exists d3mi_1a;

create table d3mi_1a(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d3mi_2a;

create table d3mi_2a(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d3mi_3a;

create table d3mi_3a(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

-- D3MI

-- D4AK

drop table if exists d4ak_1a;

create table d4ak_1a(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4ak_1b;

create table d4ak_1b(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4ak_2a;

create table d4ak_2a(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4ak_2b;

create table d4ak_2b(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4ak_3a;

create table d4ak_3a(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4ak_3b;

create table d4ak_3b(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4ak_4a;

create table d4ak_4a(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4ak_4b;

create table d4ak_4b(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4ak_4c;

create table d4ak_4c(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

-- D4AK

-- D3AK

drop table if exists d3ak_1a;

create table d3ak_1a(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d3ak_2a;

create table d3ak_2a(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d3ak_2b;

create table d3ak_2b(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d3ak_3a;

create table d3ak_3a(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d3ak_3b;

create table d3ak_3b(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

-- D3AK

-- D4MP

drop table if exists d4mp_1a;

create table d4mp_1a(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4mp_1b;

create table d4mp_1b(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4mp_2a;

create table d4mp_2a(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4mp_2b;

create table d4mp_2b(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4mp_2c;

create table d4mp_2c(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4mp_2d;

create table d4mp_2d (
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4mp_3a;

create table d4mp_3a(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4mp_3b;

create table d4mp_3b(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4mp_3c;

create table d4mp_3c(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4mp_3d;

create table d4mp_3d(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4mp_4a;

create table d4mp_4a(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4mp_4b;

create table d4mp_4b(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4mp_4c;

create table d4mp_4c(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);


-- D4MP

-- D3MP

drop table if exists d3mp_1a;

create table d3mp_1a(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d3mp_2a;

create table d3mp_2a(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d3mp_2b;

create table d3mp_2b(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d3mp_3a;

create table d3mp_3a(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d3mp_3b;

create table d3mp_3b(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

-- D3MP

-- D4LB

drop table if exists d4lb_1a;

create table d4lb_1a(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4lb_1b;

create table d4lb_1b(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4lb_1c;

create table d4lb_1c(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4lb_1d;

create table d4lb_1d(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4lb_1e;

create table d4lb_1e(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4lb_1f;

create table d4lb_1f(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4lb_2a;

create table d4lb_2a(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4lb_2b;

create table d4lb_2b(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4lb_2c;

create table d4lb_2c(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4lb_2d;

create table d4lb_2d(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4lb_2e;

create table d4lb_2e(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4lb_2f;

create table d4lb_2f(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4lb_2g;

create table d4lb_2g(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4lb_2h;

create table d4lb_2h(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4lb_3a;

create table d4lb_3a(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4lb_3b;

create table d4lb_3b(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4lb_3c;

create table d4lb_3c(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4lb_3d;

create table d4lb_3d(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4lb_3e;

create table d4lb_3e(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4lb_3f;

create table d4lb_3f (
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4lb_4a;

create table d4lb_4a(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4lb_4b;

create table d4lb_4b(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4lb_4c;

create table d4lb_4c(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4lb_4d;

create table d4lb_4d(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4lb_4e;

create table d4lb_4e(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4lb_4f;

create table d4lb_4f(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d4lb_4g;

create table d4lb_4g(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

-- D4LB

-- D3AL

drop table if exists d3al_1a;

create table d3al_1a(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d3al_1b;

create table d3al_1b(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d3al_1c;

create table d3al_1c(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d3al_1d;

create table d3al_1d(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d3al_2a;

create table d3al_2a(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d3al_2b;

create table d3al_2b(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d3al_2c;

create table d3al_2c(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d3al_2d;

create table d3al_2d(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d3al_2e;

create table d3al_2e(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d3al_3a;

create table d3al_3a(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d3al_3b;

create table d3al_3b(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d3al_3c;

create table d3al_3c(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d3al_3d;

create table d3al_3d(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

drop table if exists d3al_3e;

create table d3al_3e(
	id int auto_increment primary key,
	npm varchar(7) not null,
	number_phone varchar(255) not null,
	lecturer varchar(15) not null,
	course varchar(15) not null,
	discussion text not null,
	date_time datetime not null,
	message text not null,
	kode_matkul varchar(15) not null
);

-- D3AL

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;