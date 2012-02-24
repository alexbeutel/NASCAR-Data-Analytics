-- phpMyAdmin SQL Dump
-- version 3.3.10.4
-- http://www.phpmyadmin.net
--
-- Server version: 5.1.53
-- PHP Version: 5.2.17

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

-- --------------------------------------------------------

--
-- Table structure for table `ContentPages`
--

CREATE TABLE IF NOT EXISTS `ContentPages` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `PackageID` int(11) NOT NULL,
  `LoopID` int(11) DEFAULT NULL,
  `linkHTML` varchar(255) NOT NULL,
  `sectionHeader` varchar(255) NOT NULL,
  `url1` varchar(255) NOT NULL,
  `title1` varchar(255) NOT NULL,
  `url2` varchar(255) NOT NULL,
  `title2` varchar(255) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=66262 ;

-- --------------------------------------------------------

--
-- Table structure for table `Files`
--

CREATE TABLE IF NOT EXISTS `Files` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `ContentID` int(11) NOT NULL,
  `linkHTML` varchar(255) NOT NULL,
  `filetype` varchar(255) NOT NULL,
  `url` varchar(255) NOT NULL,
  `file` longtext,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=89725 ;

-- --------------------------------------------------------

--
-- Table structure for table `LoopPackage`
--

CREATE TABLE IF NOT EXISTS `LoopPackage` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `PID` int(11) NOT NULL,
  `LinkHTML` text NOT NULL,
  `title` varchar(1024) NOT NULL,
  `url` varchar(1024) NOT NULL,
  `title2` varchar(1024) NOT NULL,
  `url2` varchar(1024) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=709 ;

-- --------------------------------------------------------

--
-- Table structure for table `Package`
--

CREATE TABLE IF NOT EXISTS `Package` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Year` int(11) NOT NULL,
  `divHTML` varchar(1024) NOT NULL,
  `linkHTML` varchar(1024) NOT NULL,
  `url1` varchar(255) NOT NULL,
  `title1` varchar(255) NOT NULL,
  `url2` varchar(255) NOT NULL,
  `title2` varchar(255) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=650 ;

-- --------------------------------------------------------

--
-- Table structure for table `Years`
--

CREATE TABLE IF NOT EXISTS `Years` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Year` varchar(255) NOT NULL,
  `URL` varchar(255) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2012 ;
