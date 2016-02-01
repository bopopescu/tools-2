CREATE TABLE history_ips(
  id	INT AUTO_INCREMENT,
  ip	VARCHAR(32) NOT NULL UNIQUE,
  detect_count INT DEFAULT 0,
  available_count INT DEFAULT 0,
  PRIMARY KEY (id)
) Engine=InnoDB;

CREATE TABLE available_ips(
  id	INT AUTO_INCREMENT,
  ip	VARCHAR(32) NOT NULL UNIQUE,
  available_time datetime,
  delay INT DEFAULT 0,
  PRIMARY KEY (id)
) Engine=InnoDB;
