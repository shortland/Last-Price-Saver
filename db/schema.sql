SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

CREATE DATABASE IF NOT EXISTS `last_price_saver` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `last_price_saver`;
--
-- Database: `last_price_saver`
--

-- --------------------------------------------------------

--
-- Table structure for table `last_price`
--

CREATE TABLE IF NOT EXISTS `last_price` (
  `idn` bigint(20) NOT NULL AUTO_INCREMENT,
  `timestamped` bigint(20) NOT NULL,
  `timestamp_milli` bigint(20) NOT NULL,
  `symbol` varchar(6) NOT NULL,
  `price` float NOT NULL,
  `json` text NOT NULL,
  PRIMARY KEY (`idn`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
