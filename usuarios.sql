-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 15-06-2024 a las 08:26:28
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `usuarios`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `dni` varchar(20) NOT NULL,
  `correo` varchar(255) NOT NULL,
  `codigo` varchar(20) NOT NULL,
  `contraseña` varchar(255) NOT NULL,
  `pc1` int(2) NOT NULL,
  `pc2` int(2) NOT NULL,
  `pc3` int(2) NOT NULL,
  `pc4` int(2) NOT NULL,
  `promedio` float NOT NULL,
  `estado` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `dni`, `correo`, `codigo`, `contraseña`, `pc1`, `pc2`, `pc3`, `pc4`, `promedio`, `estado`) VALUES
(10, 'eliot alderson', '73034606', 'eliot_alderson@gmail.com', '11111111', 'scrypt:32768:8:1$CMZvHPCwCQDD21AB$f690d8ccc9b939bdaac2b341f6fdebca8d944ddca59bf578432132f5bf1bd72a8ae45cfbe7ee62175bfe92851e92b39d57f0e3714f4f82749e9c8d25a70309c3', 12, 10, 20, 11, 13.25, 'Aprobado'),
(11, 'Marcela Anderson', '11232312', 'marcela@gmail.com', '111111', 'scrypt:32768:8:1$8K4g2AlApKgRzCWC$126552f2a339c513101ae0d6cee38a586107ac50be24cb7f7a74148a6e38ec3181bbc9c51a9885ab1e070c853a65943e792d961844aa655a01e96e3fa6ccf646', 20, 12, 8, 14, 13.5, 'Aprobado'),
(13, 'Marcela Anderson Sanchez Rojas', '73034606', 'MarcelaxEliot@gmail.com', '73034606', '223', 12, 11, 13, 15, 12.75, 'Aprobado'),
(14, 'Tony Soprano', '123123', 'tony@gmail.com', '13213', '', 12, 10, 12, 14, 12, 'Aprobado'),
(15, 'Pirtywii', '123123123', 'pirtywii@gmail.com', '1211', '', 12, 10, 9, 8, 9.75, 'Desaprobad'),
(16, 'tony soprano dalto', '123132', 'tonyyy@gmail.com', '1231323', 'scrypt:32768:8:1$tNYhu95eNUZhENPv$0d48aaa82dd883ee09dda6ab599e9f3e2991b08c74785f9d611c44cecd2c157c77609a0370ef93c23d8526f3332d085f7623b7e32bb68f004af0de8cf172bfaf', 12, 10, 13, 15, 12.5, 'Aprobado'),
(17, 'asdasd', 'asdads', 'topny@gmail.com', '123123', 'scrypt:32768:8:1$DFmbzlj57bEVJjCX$5b7ac3996ee731b28894b92f725f75f7f7f4533c3630393064b61c27cd65e22ca1c365022d852235132c1e791cdf35340d133ee971097242d508411c67e54c12', 20, 12, 15, 16, 15.75, 'Aprobado');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`) USING BTREE;

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
