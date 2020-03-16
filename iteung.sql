-- phpMyAdmin SQL Dump
-- version 5.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 16, 2020 at 01:04 PM
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

-- --------------------------------------------------------

--
-- Table structure for table `d4ti_3a`
--

CREATE TABLE `d4ti_3a` (
  `id` int(11) NOT NULL,
  `npm` varchar(7) NOT NULL,
  `number_phone` varchar(255) NOT NULL,
  `lecturer` varchar(15) NOT NULL,
  `course` varchar(15) NOT NULL,
  `discussion` text NOT NULL,
  `date_time` datetime NOT NULL,
  `message` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `d4ti_3a`
--

INSERT INTO `d4ti_3a` (`id`, `npm`, `number_phone`, `lecturer`, `course`, `discussion`, `date_time`, `message`) VALUES
(395, '1184047', '+62 822-1740-1448', 'nn255ll', 'database 1', 'pengenalan database', '2020-03-16 18:21:55', ''),
(396, '1184047', '+62 822-1740-1448', 'nn255ll', 'database 1', 'pengenalan database', '2020-03-16 18:21:59', 'wekwek'),
(397, '1174006', '+62 896-7770-9045', 'nn255ll', 'database 1', 'pengenalan database', '2020-03-16 18:22:10', 'rwrw'),
(398, '1174006', '+62 896-7770-9045', 'nn255ll', 'database 1', 'pengenalan database', '2020-03-16 18:22:15', 'hhh'),
(399, '1174006', '+62 896-7770-9045', 'nn255ll', 'database 1', 'pengenalan database', '2020-03-16 18:22:17', 'rwrw'),
(400, '1184047', '+62 822-1740-1448', 'nn255ll', 'database 1', 'pengenalan database', '2020-03-16 18:22:36', 'rwrw'),
(401, '1184047', '+62 822-1740-1448', 'nn255ll', 'database 1', 'pengenalan database', '2020-03-16 18:22:36', 'iiteung matkul database 1 selesai'),
(402, '1184047', '+62 822-1740-1448', 'nn255ll', 'database 1', 'pengenalan database', '2020-03-16 18:31:21', ''),
(403, '1184047', '+62 822-1740-1448', 'nn255ll', 'database 1', 'pengenalan database', '2020-03-16 18:31:32', 'iiteung matkul database 1 selesai'),
(404, '1184047', '+62 822-1740-1448', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:32:55', ''),
(405, '1184047', '+62 822-1740-1448', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:32:59', 'wiu wiu'),
(406, '1184047', '+62 822-1740-1448', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:33:09', 'iiteung matkul kecerdasan buatan selesai'),
(407, '1184047', '+62 822-1740-1448', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:42:52', ''),
(408, '1184047', '+62 822-1740-1448', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:43:01', 'iiteung matkul kecerdasan buatan selesai'),
(409, '1184047', '+62 822-1740-1448', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:43:41', ''),
(410, '1174006', '+62 896-7770-9045', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:43:44', 'mama'),
(411, '1184047', '+62 822-1740-1448', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:43:44', 'mama'),
(412, '1184047', '+62 822-1740-1448', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:43:44', 'kakaka'),
(413, '1184047', '+62 822-1740-1448', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:43:46', 'jsnwndjjxnd'),
(414, '1184047', '+62 822-1740-1448', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:43:47', 'mamwmsjmx'),
(415, '1174006', '+62 896-7770-9045', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:43:49', 'mini'),
(416, '1184047', '+62 822-1740-1448', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:43:52', 'ayo mulai'),
(417, '1174006', '+62 896-7770-9045', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:43:54', 'tetew'),
(418, '1184047', '+62 822-1740-1448', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:43:54', 'crot crot'),
(419, '1174006', '+62 896-7770-9045', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:43:58', 'crot crot'),
(420, '1174006', '+62 896-7770-9045', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:43:59', 'ayo pak'),
(421, '1174006', '+62 896-7770-9045', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:44:06', 'saya udh masuk'),
(422, '1184047', '+62 822-1740-1448', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:44:09', 'iiteung matkul kecerdasan buatan selesai'),
(423, '1184047', '+62 822-1740-1448', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:45:23', ''),
(424, '1184047', '+62 822-1740-1448', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:45:26', 'yo'),
(425, '1174006', '+62 896-7770-9045', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:45:28', '5555'),
(426, '1184047', '+62 822-1740-1448', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:45:29', 'kita mulai yo'),
(427, '1174006', '+62 896-7770-9045', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:45:30', '4444'),
(428, '1184047', '+62 822-1740-1448', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:45:31', '4444'),
(429, '1184047', '+62 822-1740-1448', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:45:31', 'yoyo'),
(430, '1174006', '+62 896-7770-9045', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:45:32', '33333'),
(431, '1184047', '+62 822-1740-1448', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:45:33', 'masuk yo'),
(432, '1174006', '+62 896-7770-9045', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:45:37', 'iya'),
(433, '1184047', '+62 822-1740-1448', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:45:43', 'iya'),
(434, '1184047', '+62 822-1740-1448', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:45:43', 'iiteung matkul kecerdasan buatan selesai'),
(435, '1184047', '+62 822-1740-1448', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:47:46', ''),
(436, '1174006', '+62 896-7770-9045', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:47:49', ''),
(437, '1174006', '+62 896-7770-9045', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:47:49', 'i have to be honest with the people'),
(438, '1184047', '+62 822-1740-1448', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:47:49', 'kakakxm'),
(439, '1184047', '+62 822-1740-1448', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:47:50', 'akakaka'),
(440, '1184047', '+62 822-1740-1448', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:47:53', 'hehe'),
(441, '1174006', '+62 896-7770-9045', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:47:53', 'i no longer have a job'),
(442, '1184047', '+62 822-1740-1448', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:47:54', 'waw'),
(443, '1184047', '+62 822-1740-1448', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:47:58', 'iteung'),
(444, '1174006', '+62 896-7770-9045', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:48:02', 'i am not sure if you are aware of this but i am interested in the job'),
(445, '1184047', '+62 822-1740-1448', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:48:04', 'i am not sure if you are aware of this but i am interested in the job'),
(446, '1184047', '+62 822-1740-1448', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:48:04', 'woi iteung'),
(447, '1184047', '+62 822-1740-1448', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:48:17', 'iiteung matkul kecerdasan buatan selesai'),
(448, '1184047', '+62 822-1740-1448', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:49:33', ''),
(449, '1184047', '+62 822-1740-1448', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:49:37', 'yok mare'),
(450, '1174006', '+62 896-7770-9045', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:49:51', 'yok mare'),
(451, '1174006', '+62 896-7770-9045', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:49:52', 'i am not sure if you are aware of this'),
(452, '1174006', '+62 896-7770-9045', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:49:52', 'i have to go to work'),
(453, '1174006', '+62 896-7770-9045', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:49:58', 'i will try to get a hold of you'),
(454, '1184047', '+62 822-1740-1448', 'nn257l', 'database 1', 'kecerdasan buatan yg dibuat buat oleh manusia hehe', '2020-03-16 18:49:59', 'iiteung matkul kecerdasan buatan selesai');

-- --------------------------------------------------------

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
('NN257L', 'Rolly Maulana Awangga S.T.,M.T.');

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
  `modul` varchar(255) NOT NULL
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
('rokok', 'bukannya wanda gak mau beliin, tapi rokok itu gak baik buat kesehatan, lebih baik rokoknya diganti sama wanda aja gimana?'),
('kesal', 'hmm, maaf ya kalo wanda ada salah sama kamu'),
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
-- Indexes for table `d4ti_3a`
--
ALTER TABLE `d4ti_3a`
  ADD PRIMARY KEY (`id`);

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

--
-- AUTO_INCREMENT for table `d4ti_3a`
--
ALTER TABLE `d4ti_3a`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=455;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
