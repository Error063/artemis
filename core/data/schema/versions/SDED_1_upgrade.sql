CREATE TABLE ongeki_user_gacha (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    user INT NOT NULL,
    gachaId INT NOT NULL,
    totalGachaCnt INT DEFAULT 0,
    ceilingGachaCnt INT DEFAULT 0,
    selectPoint INT DEFAULT 0,
    useSelectPoint INT  DEFAULT 0,
    dailyGachaCnt INT DEFAULT 0,
    fiveGachaCnt INT DEFAULT 0,
    elevenGachaCnt INT DEFAULT 0,
    dailyGachaDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT ongeki_user_gacha_uk UNIQUE (user, gachaId),
    CONSTRAINT ongeki_user_gacha_ibfk_1 FOREIGN KEY (user) REFERENCES aime_user (id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE ongeki_user_gacha_supply (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    user INT NOT NULL,
    cardId INT NOT NULL,
    CONSTRAINT ongeki_user_gacha_supply_uk UNIQUE (user, cardId),
    CONSTRAINT ongeki_user_gacha_supply_ibfk_1 FOREIGN KEY (user) REFERENCES aime_user (id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE ongeki_static_gachas (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    version INT NOT NULL,
    gachaId INT NOT NULL,
    gachaName VARCHAR(255) NOT NULL,
    kind INT NOT NULL,
    type INT DEFAULT 0,
    isCeiling BOOLEAN DEFAULT 0,
    maxSelectPoint INT DEFAULT 0,
    ceilingCnt INT DEFAULT 10,
    changeRateCnt1 INT DEFAULT 0,
    changeRateCnt2 INT DEFAULT 0,
    startDate TIMESTAMP DEFAULT '2018-01-01 00:00:00.0',
    endDate TIMESTAMP DEFAULT '2038-01-01 00:00:00.0',
    noticeStartDate TIMESTAMP DEFAULT '2018-01-01 00:00:00.0',
    noticeEndDate TIMESTAMP DEFAULT '2038-01-01 00:00:00.0',
    convertEndDate TIMESTAMP DEFAULT '2038-01-01 00:00:00.0',
    CONSTRAINT ongeki_static_gachas_uk UNIQUE (version, gachaId, gachaName)
);

CREATE TABLE ongeki_static_gacha_cards (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    gachaId INT NOT NULL,
    cardId INT NOT NULL,
    rarity INT NOT NULL,
    weight INT DEFAULT 1,
    isPickup BOOLEAN DEFAULT 0,
    isSelect BOOLEAN DEFAULT 1,
    CONSTRAINT ongeki_static_gacha_cards_uk UNIQUE (gachaId, cardId)
);


CREATE TABLE ongeki_static_cards (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    version INT NOT NULL,
    cardId INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    charaId INT NOT NULL,
    nickName VARCHAR(255), 
    school VARCHAR(255) NOT NULL,
    attribute VARCHAR(5) NOT NULL,
    gakunen VARCHAR(255) NOT NULL,
    rarity INT NOT NULL,
    levelParam VARCHAR(255) NOT NULL,
    skillId INT NOT NULL,
    choKaikaSkillId INT NOT NULL,
    cardNumber VARCHAR(255),
    CONSTRAINT ongeki_static_cards_uk UNIQUE (version, cardId)
) CHARACTER SET utf8mb4;

CREATE TABLE ongeki_user_print_detail (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user INT NOT NULL,
    cardId INT NOT NULL,
    cardType INT DEFAULT 0,
    printDate TIMESTAMP NOT NULL,
    serialId VARCHAR(20) NOT NULL,
    placeId INT NOT NULL,
    clientId VARCHAR(11) NOT NULL,
    printerSerialId VARCHAR(20) NOT NULL,
    isHolograph BOOLEAN DEFAULT 0,
    isAutographed BOOLEAN DEFAULT 0,
    printOption1 BOOLEAN DEFAULT 1,
    printOption2 BOOLEAN DEFAULT 1,
    printOption3 BOOLEAN DEFAULT 1,
    printOption4 BOOLEAN DEFAULT 1,
    printOption5 BOOLEAN DEFAULT 1,
    printOption6 BOOLEAN DEFAULT 1,
    printOption7 BOOLEAN DEFAULT 1,
    printOption8 BOOLEAN DEFAULT 1,
    printOption9 BOOLEAN DEFAULT 1,
    printOption10 BOOLEAN DEFAULT 0,
    FOREIGN KEY (user) REFERENCES aime_user(id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT ongeki_user_print_detail_uk UNIQUE (serialId)
) CHARACTER SET utf8mb4;