-- Dump for MySQL 5.X

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema petdb
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `petdb` ;

-- -----------------------------------------------------
-- Schema petdb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `petdb` DEFAULT CHARACTER SET utf8mb4 ;
USE `petdb` ;

-- -----------------------------------------------------
-- Table `petdb`.`pets`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `petdb`.`pets` ;

CREATE TABLE IF NOT EXISTS `petdb`.`pets` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `species` VARCHAR(45) NOT NULL,
  `gender` CHAR(1) NOT NULL,
  `birthday` DATE NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- -----------------------------------------------------
-- Data for table `petdb`.`pets`
-- -----------------------------------------------------
START TRANSACTION;
USE `petdb`;
INSERT INTO `petdb`.`pets` (`id`, `name`, `species`, `gender`, `birthday`) VALUES (1, 'Fritz', 'dog', 'm', '2016-12-03');
INSERT INTO `petdb`.`pets` (`id`, `name`, `species`, `gender`, `birthday`) VALUES (2, 'Sweety', 'cat', 'w', '2015-06-23');
INSERT INTO `petdb`.`pets` (`id`, `name`, `species`, `gender`, `birthday`) VALUES (3, 'Tequila', 'parakeet', 'w', '2017-01-05');
INSERT INTO `petdb`.`pets` (`id`, `name`, `species`, `gender`, `birthday`) VALUES (4, 'Rambo', 'parakeet', 'm', NULL);
INSERT INTO `petdb`.`pets` (`id`, `name`, `species`, `gender`, `birthday`) VALUES (5, 'Smokey', 'cat', 'm', '2016-01-17');
INSERT INTO `petdb`.`pets` (`id`, `name`, `species`, `gender`, `birthday`) VALUES (6, 'Missy', 'dog', 'w', '2013-03-09');
INSERT INTO `petdb`.`pets` (`id`, `name`, `species`, `gender`, `birthday`) VALUES (7, 'Uni-🙈', 'monkey', 'm', '2014-04-01');

COMMIT;
