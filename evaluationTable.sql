-- Table flagEvaluation
CREATE TABLE flagEvaluation(
    timestamp TIMESTAMP PRIMARY KEY,
    idAlgo VARCHAR(255),
    flagConfirmed BOOLEAN NOT NULL,
    tqc VARCHAR(255),
    inProcess BOOLEAN,
    postFab BOOLEAN
);

-- Table algoEvaluation
CREATE TABLE algoEvaluation(
    timestamp TIMESTAMP PRIMARY KEY,
    idAlgo VARCHAR(255),
    tqc VARCHAR(255) NOT NULL,
    qScore FLOAT NOT NULL,
    costScore FLOAT,
    timeFrameScore FLOAT,
    reliabilityScore FLOAT,
    flagConfirmed BOOLEAN NOT NULL
);

-- Table prodEvaluationData
CREATE TABLE prodEvaluationData (
    timestamp TIMESTAMP PRIMARY KEY,
    idAlgo VARCHAR(255),
    tqc VARCHAR(255) NOT NULL,
    qScore FLOAT NOT NULL,
    flagConfirmed BOOLEAN NOT NULL,
    evaluation TEXT,
    evaluationConfirmed BOOLEAN
    interventionScore FLOAT
    interventionLevel VARCHAR(255)
);

-- Table evaluationFormData
CREATE TABLE evaluationFormData (
    timestamp TIMESTAMP PRIMARY KEY,
    tqc VARCHAR(255) NOT NULL,
    intervention TEXT NOT NULL,
    interventionQuality TEXT NOT NULL
);

-- Table algoTqc
CREATE TABLE algoTqc (
    id SERIAL PRIMARY KEY,
    idAlgo VARCHAR(255),
    tqc1 VARCHAR(255),
    tqc2 VARCHAR(255),
    tqc3 VARCHAR(255)
);

-- Table algoData
CREATE TABLE algoData (
    id SERIAL PRIMARY KEY,
    algo VARCHAR(255),
    type VARCHAR(255) NOT NULL,
    infos TEXT
);

-- Table scoreThreshold
CREATE TABLE scoreThreshold (
    id SERIAL PRIMARY KEY,
    algo VARCHAR(255),
    tqc VARCHAR(255) NOT NULL,
    qScore FLOAT NOT NULL,
    iScoreLow FLOAT NOT NULL,
    iScoreHigh FLOAT NOT NULL
);
