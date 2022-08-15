-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Aug 15, 2022 at 07:45 PM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `database`
--

-- --------------------------------------------------------

--
-- Table structure for table `contacts`
--

CREATE TABLE `contacts` (
  `sno` int(10) NOT NULL,
  `name` text NOT NULL,
  `email` varchar(20) NOT NULL,
  `phone_num` varchar(12) NOT NULL,
  `msg` text NOT NULL,
  `date` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `contacts`
--

INSERT INTO `contacts` (`sno`, `name`, `email`, `phone_num`, `msg`, `date`) VALUES
(1, 'dark', 'dark@gmail.com', '0011223344', 'sdfsadf', '2022-08-09 03:14:01');

-- --------------------------------------------------------

--
-- Table structure for table `posts`
--

CREATE TABLE `posts` (
  `sno` int(11) NOT NULL,
  `title` text NOT NULL,
  `slug` text NOT NULL,
  `content` varchar(120) NOT NULL,
  `date` datetime NOT NULL DEFAULT current_timestamp(),
  `img_file` varchar(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `posts`
--

INSERT INTO `posts` (`sno`, `title`, `slug`, `content`, `date`, `img_file`) VALUES
(2, 'this is my second post', 'second-post', 'This is my second post ajshdfkjhsakfjhaskjmxncbvncxcvnz,xmnvm,zxncvxmnzc.v,ha;dhguyhafsjkafhsdmnfsmndfbslajgfdkja', '2022-08-09 18:18:05', 'about-bg.jpg'),
(3, 'this is my third post', 'third-post', 'This is my third post ajshdfkjhsakfjhaskjmxncbvncxcvnz,xmnvm,zxncvxmnzc.v,ha;dhguyhafsjkafhsdmnfsmndfbslajgfdkjasg', '2022-08-09 18:18:05', 'post-bg.jpg'),
(4, 'this is my 4th post', 'fourth-post', 'ajshdfiuy afjhkasjfiasufkjsakfhjsafuiayfjkhkfjjkashfasuyjfhakjsfkn,mnvxzkjhvzxhvjkhzjkxhvkj', '2022-08-09 18:19:17', 'post-bg.jpg'),
(5, 'this is fifth', 'fifth post', 'ajshdfiuy afjhkasjfiasufkjsakfhjsafuiayfjkhkfjjkashfasuyjfhakjsfkn,mnvxzkjhvzxhvjkhzjkxhvkj', '2022-08-09 18:19:17', 'post-bg.jpg');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `contacts`
--
ALTER TABLE `contacts`
  ADD PRIMARY KEY (`sno`);

--
-- Indexes for table `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`sno`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `contacts`
--
ALTER TABLE `contacts`
  MODIFY `sno` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `posts`
--
ALTER TABLE `posts`
  MODIFY `sno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
