/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 100144
 Source Host           : localhost:3306
 Source Schema         : wanda

 Target Server Type    : MySQL
 Target Server Version : 100144
 File Encoding         : 65001

 Date: 02/03/2020 06:53:51
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `group_auth`;
CREATE TABLE `group_auth`  (
  `number` varchar(18)  NOT NULL,
  `group_id` int(2) NOT NULL,
  PRIMARY KEY(`number`)
);

INSERT INTO `group_auth` VALUES('+62 822-1740-1448', 2), ('+62 896-7770-9045', 1);

DROP TABLE IF EXISTS `number_auth`;
CREATE TABLE `number_auth`  (
  `group_id` int(2) NOT NULL,
  `modul` varchar(255) NOT NULL,
  PRIMARY KEY(`modul`)
);

INSERT INTO `number_auth` VALUES(1, 'm:siap'), (2, 'm:prodi');

-- ----------------------------
-- Table structure for error_message
-- ----------------------------
DROP TABLE IF EXISTS `error_message`;
CREATE TABLE `error_message`  (
  `content` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of error_message
-- ----------------------------
INSERT INTO `error_message` VALUES ('Duh maaf programnya ada yang rusak nih.. tulisannya :  _#ERROR#_   ,#BOTNAME# sekarang yang minta tolong boleh? forwadin pesan ini ke akang teteh mimin ya... Makasih :) ');

-- ----------------------------
-- Table structure for keyword
-- ----------------------------
DROP TABLE IF EXISTS `keyword`;
CREATE TABLE `keyword`  (
  `keyword_group` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `keyword` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of keyword
-- ----------------------------
INSERT INTO `keyword` VALUES ('perkenalan', 'kenalan');
INSERT INTO `keyword` VALUES ('perkenalan', 'perkenalkan');
INSERT INTO `keyword` VALUES ('trims', 'terimakasih');
INSERT INTO `keyword` VALUES ('trims', 'haturnuhun');
INSERT INTO `keyword` VALUES ('trims', 'nuhun');
INSERT INTO `keyword` VALUES ('trims', 'makasih');
INSERT INTO `keyword` VALUES ('pujian', 'pintar');
INSERT INTO `keyword` VALUES ('love', 'love');
INSERT INTO `keyword` VALUES ('pujian', 'cantik');
INSERT INTO `keyword` VALUES ('buli', 'bodoh');
INSERT INTO `keyword` VALUES ('buli', 'jelek');
INSERT INTO `keyword` VALUES ('buli', 'bangsat');
INSERT INTO `keyword` VALUES ('buli', 'bego');
INSERT INTO `keyword` VALUES ('buli', 'tolol');
INSERT INTO `keyword` VALUES ('buli', 'idiot');
INSERT INTO `keyword` VALUES ('buli', 'bau');
INSERT INTO `keyword` VALUES ('trims', 'trims');
INSERT INTO `keyword` VALUES ('formal', 'siang');
INSERT INTO `keyword` VALUES ('formal', 'sore');
INSERT INTO `keyword` VALUES ('formal', 'malam');
INSERT INTO `keyword` VALUES ('formal', 'pagi');
INSERT INTO `keyword` VALUES ('teka_teki', 'teka-teki');
INSERT INTO `keyword` VALUES ('teka_teki', 'main');
INSERT INTO `keyword` VALUES ('gombal', 'gombal');
INSERT INTO `keyword` VALUES ('gombal', 'rayu');
INSERT INTO `keyword` VALUES ('gombal', 'baper');
INSERT INTO `keyword` VALUES ('gombal', 'gombalin');
INSERT INTO `keyword` VALUES ('gombal', 'baperin');
INSERT INTO `keyword` VALUES ('gombal', 'gombalan');
INSERT INTO `keyword` VALUES ('gombal', 'rayuan');
INSERT INTO `keyword` VALUES ('joke', 'ngelucu');
INSERT INTO `keyword` VALUES ('joke', 'ngelawak');
INSERT INTO `keyword` VALUES ('joke', 'ngereceh');
INSERT INTO `keyword` VALUES ('joke', 'lawakan');
INSERT INTO `keyword` VALUES ('user_cantik', 'aku-cantik');
INSERT INTO `keyword` VALUES ('m:sendVideoWithoutPhoneNumber', 'ngedance');
INSERT INTO `keyword` VALUES ('m:sendVideoWithoutPhoneNumber', 'dance');
INSERT INTO `keyword` VALUES ('m:sendVideoWithoutPhoneNumber', 'nari');
INSERT INTO `keyword` VALUES ('m:sendVideoWithoutPhoneNumber', 'nyanyi');
INSERT INTO `keyword` VALUES ('m:sendVideoWithoutPhoneNumber', 'menyanyi');
INSERT INTO `keyword` VALUES ('m:sendVideoWithoutPhoneNumber', 'gaya');
INSERT INTO `keyword` VALUES ('m:sendVideoWithoutPhoneNumber', 'imutnya');
INSERT INTO `keyword` VALUES ('cantik', 'kamu-cantik');
INSERT INTO `keyword` VALUES ('cantik', 'kamu-cantik');
INSERT INTO `keyword` VALUES ('rokok', 'beliin-rokok');
INSERT INTO `keyword` VALUES ('rokok', 'beli-rokok');
INSERT INTO `keyword` VALUES ('rokok', 'belikan-rokok');
INSERT INTO `keyword` VALUES ('rokok', 'beli-udud');
INSERT INTO `keyword` VALUES ('rokok', 'beliin-udud');
INSERT INTO `keyword` VALUES ('kesal', 'ngeselin');
INSERT INTO `keyword` VALUES ('kesal', 'kesal');
INSERT INTO `keyword` VALUES ('centil', 'centil');
INSERT INTO `keyword` VALUES ('centil', 'nakal');
INSERT INTO `keyword` VALUES ('m:prodi', 'nilai');
INSERT INTO `keyword` VALUES ('pujian', 'pinter');

-- ----------------------------
-- Table structure for multi_key
-- ----------------------------
DROP TABLE IF EXISTS `multi_key`;
CREATE TABLE `multi_key`  (
  `multiple_keywords` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of multi_key
-- ----------------------------
INSERT INTO `multi_key` VALUES ('aku-cantik');
INSERT INTO `multi_key` VALUES ('kamu-cantik');
INSERT INTO `multi_key` VALUES ('selamat-siang');
INSERT INTO `multi_key` VALUES ('selamat-sore');
INSERT INTO `multi_key` VALUES ('selamat-malam');
INSERT INTO `multi_key` VALUES ('selamat-pagi');
INSERT INTO `multi_key` VALUES ('beli-rokok');
INSERT INTO `multi_key` VALUES ('beliin-rokok');
INSERT INTO `multi_key` VALUES ('belikan-rokok');
INSERT INTO `multi_key` VALUES ('beli-udud');
INSERT INTO `multi_key` VALUES ('beliin-udud');

-- ----------------------------
-- Table structure for notfound_message
-- ----------------------------
DROP TABLE IF EXISTS `notfound_message`;
CREATE TABLE `notfound_message`  (
  `content` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of notfound_message
-- ----------------------------
INSERT INTO `notfound_message` VALUES ('duh maap... #BOTNAME# ga ngerti bahasanya.... huhuhu...');

-- ----------------------------
-- Table structure for opening_message
-- ----------------------------
DROP TABLE IF EXISTS `opening_message`;
CREATE TABLE `opening_message`  (
  `content` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of opening_message
-- ----------------------------
INSERT INTO `opening_message` VALUES ('iyaaaaaa :-D #BOTNAME# disini, selalu menantimu');
INSERT INTO `opening_message` VALUES ('iya, butuh bantuan? atau cuman rindu sama #BOTNAME# :D');
INSERT INTO `opening_message` VALUES ('iya, kenapa? ada yang bisa #BOTNAME# bantukah??');

-- ----------------------------
-- Table structure for reply
-- ----------------------------
DROP TABLE IF EXISTS `reply`;
CREATE TABLE `reply`  (
  `keyword_group` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `content` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of reply
-- ----------------------------
INSERT INTO `reply` VALUES ('buli', 'Tak ada manusia yang terlahir \\n di download \\n (´-﹏-`；)');
INSERT INTO `reply` VALUES ('buli', 'Bumi ini aja aku pijak \\napalagi kepala kau \\n (；･`д･´)');
INSERT INTO `reply` VALUES ('buli', 'rangga yang kamu lakukan ke saya itu \\n JAHAT \\n (;´༎ຶД༎ຶ`)');
INSERT INTO `reply` VALUES ('trims', 'sama sama :-)');
INSERT INTO `reply` VALUES ('trims', 'yoi, cama-cama');
INSERT INTO `reply` VALUES ('trims', 'sami sami :-D');
INSERT INTO `reply` VALUES ('buli', 'Ya allah Tolongin Ya allah (ಥ﹏ಥ)\", \"Kok kamu jahat bIiinNNNnngggGGHHiitzzz sich sama aku zheyeng (\'・ω・\')');
INSERT INTO `reply` VALUES ('perkenalan', 'Halo, perkenalkan Nama aku #BOTNAME#, Aku seorang mahasiswi Informatics Research Center (IRC), Salam kenal ya');
INSERT INTO `reply` VALUES ('pujian', 'Oo, iya dong, makasih atas pujiannya');
INSERT INTO `reply` VALUES ('pujian', 'terima kasihh kakak yang maniss (/◕ヮ◕)/');
INSERT INTO `reply` VALUES ('pujian', 'awww terima kasiihh (≧▽≦)');
INSERT INTO `reply` VALUES ('joke', 'Sahabat dekat biasanya akan mengajak makan kepiting bareng, karena sahabat yang dekat adalah sahabat a crab :)');
INSERT INTO `reply` VALUES ('joke', 'Rombongan bebek lagi nyebrang \\n Trus ada satu bebek yang ketabrak motor \\n Bebek 1: Kamu gpp? \\n Bebek 2: Aku bebek aja kok :)');
INSERT INTO `reply` VALUES ('joke', 'Kalo semua hal harus dipikirkan masak-masak, gimana nasib orang-orang yg ngga bisa masak :(');
INSERT INTO `reply` VALUES ('joke', 'Bang peseng es campurnya satu, tapi dipisah ya bang. Soalnya aku khawatir nggak bisa bedain mana yang tulus dan mana yg modus :)');
INSERT INTO `reply` VALUES ('joke', 'Pembeli: Bang, ngapain ngobrol sama martabak? \\nPenjual: Kata pembelinya, martabaknya jgn dikacangin :)');
INSERT INTO `reply` VALUES ('joke', 'Pembeli: Mbak, beli es tehnya \\nPenjual: Manis gak? \\nPembeli: Gak usah manis-manis, yg penting setia dan mau menerima saya apa adanya :)');
INSERT INTO `reply` VALUES ('joke', 'Kalo ketemu begal di jalan, jgn takut. Kasi balsem aja, karena balsem bisa menghilangkan begal-begal :)');
INSERT INTO `reply` VALUES ('joke', 'Kalo bercanda jgn suka kelewatan, soalnya kalo kelewatan ntar lo mesti muter balik :)');
INSERT INTO `reply` VALUES ('joke', 'Jalan sama gebetan pake flat shoes, ditengah jalan ketemu mantannya dia, trus mereka ngobrol, aku dan sepatuku gak ada hak :\')');
INSERT INTO `reply` VALUES ('joke', 'Cewek itu makhluk kuat, listrik aja dipake dibibir :(');
INSERT INTO `reply` VALUES ('joke', 'Kunci rumah gue hilang, mau masuk gak bisa. Gue cari dimana-mana gak ketemu. Akhirnya gue ambil napas panjang dan istigfar, eh pintunya kebuka. Baru inget kalo ternyata kuncinya sabar :\')');
INSERT INTO `reply` VALUES ('joke', 'Pray for Banten, ibukotanya di serang :\')');
INSERT INTO `reply` VALUES ('joke', 'Aku barusan ke kantor polisi bikin surat kehilangan, tp ditolak. Aku bilangnya aku kehilangan kamu :(');
INSERT INTO `reply` VALUES ('gombal', 'Sedang apa? Hari ini jika sehat berkenan lebih lama bersemayam di tubuh kita, maukah kau berkencan bersamaku? Hanya kita, berdua?');
INSERT INTO `reply` VALUES ('gombal', 'Aku mengenalmu tanpa sengaja, lalu menyayangimu secara tiba-tiba, namun sayang belum jadi siapa-siapa, mungkin nanti atau esok?');
INSERT INTO `reply` VALUES ('gombal', 'Kamu sejenis keyboard ya? soalnya you are my type');
INSERT INTO `reply` VALUES ('teka_teki', 'Ade ray kalau kentut bunyinya gimana? \\n Brotot, brotot, brottott ');
INSERT INTO `reply` VALUES ('teka_teki', 'Sandal apa yang paling enak di dunia? \\n Sandal terasi');
INSERT INTO `reply` VALUES ('teka_teki', 'Apa perbedaan aksi dengan demo? \\n Kalo aksi rodanya empat kalo demo rodanya tiga');
INSERT INTO `reply` VALUES ('love', 'love you too <3');
INSERT INTO `reply` VALUES ('user_cantik', 'iya kamu cantik bangeett deehh (^o^)');
INSERT INTO `reply` VALUES ('user_cantik', 'iya kamu cantik tapi masih cantikan akuu hehehe');
INSERT INTO `reply` VALUES ('user_cantik', 'iyaa zheyengg');
INSERT INTO `reply` VALUES ('cantik', 'terima kasihh kakak yang maniss (/◕ヮ◕)/');
INSERT INTO `reply` VALUES ('cantik', 'awww terima kasiihh (≧▽≦)');
INSERT INTO `reply` VALUES ('cantik', 'love you kak (ㆁωㆁ*)');
INSERT INTO `reply` VALUES ('rokok', 'bukannya wanda gak mau beliin, tapi rokok itu gak baik buat kesehatan, lebih baik rokoknya diganti sama wanda aja gimana?');
INSERT INTO `reply` VALUES ('kesal', 'hmm, maaf ya kalo wanda ada salah sama kamu');
INSERT INTO `reply` VALUES ('centil', 'emang kenapa? ada masalah?');
INSERT INTO `reply` VALUES ('centil', 'trus? masalah buat kamu?');
INSERT INTO `reply` VALUES ('buli', 'Ya Maaf (ಥ﹏ಥ)');
INSERT INTO `reply` VALUES ('buli', 'sudah cukup rhoma (｡ŏ﹏ŏ)');
INSERT INTO `reply` VALUES ('buli', 'Kamu belom pernah liat aku marah yaaahhh!!! (；･`д･´)');

-- ----------------------------
-- Table structure for waiting_message
-- ----------------------------
DROP TABLE IF EXISTS `waiting_message`;
CREATE TABLE `waiting_message`  (
  `module_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `content` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of waiting_message
-- ----------------------------
INSERT INTO `waiting_message` VALUES ('prodi', 'Tunggu Sebentar Lagi Dicari Dulu Datanya');
INSERT INTO `waiting_message` VALUES ('prodi', 'siappp..., di antosan sakeudap :-) yaaa');

-- ----------------------------
-- Table structure for waiting_message
-- ----------------------------
DROP TABLE IF EXISTS `reply_auth`;
CREATE TABLE `reply_auth`  (
  `reply_message` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of reply_auth
-- ----------------------------
INSERT INTO `reply_auth` VALUES ('Ih kamu capah minta-minta data, enak aja, #BOTNAME# gamau ngasih kekamu :-p');
INSERT INTO `reply_auth` VALUES ('Enak aja minta data itu, ga boleh :-p');

SET FOREIGN_KEY_CHECKS = 1;
