CREATE TABLE qq_no(
  id                    INT AUTO_INCREMENT,
  qq_qun				VARCHAR(32) NOT NULL,
  qq_no					VARCHAR(32) NOT NULL,
  apply_count           INT DEFAULT 0,
  PRIMARY KEY (id)
) Engine=InnoDB;
