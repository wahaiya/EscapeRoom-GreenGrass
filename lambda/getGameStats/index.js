const AWS = require('aws-sdk');
const docClient = new AWS.DynamoDB.DocumentClient();

const failedGamesParams = {
  TableName : 'escaperoom-GamesTable8000B8A1-6LFZ1GJM4KI9',
  Select: "COUNT",
  FilterExpression: 'completedTime <> :notCompleted',
  ExpressionAttributeValues: { ':notCompleted': 99999  }
};

async function countFailedGames(){
  try {
    const data = await docClient.scan(failedGamesParams).promise();
    return data;
  } catch (err) {
    return err;
  }
}

const passedGamesParams = {
  TableName : 'escaperoom-GamesTable8000B8A1-6LFZ1GJM4KI9',
  Select: "COUNT",
  FilterExpression: 'completedTime = :notCompleted',
  ExpressionAttributeValues: { ':notCompleted': 99999  }
};

async function countPassedGames(){
  try {
    const data = await docClient.scan(passedGamesParams).promise();
    return data;
  } catch (err) {
    return err;
  }
}

const playedGamesParams = {
  TableName : 'escaperoom-GamesTable8000B8A1-6LFZ1GJM4KI9',
  Select: "COUNT"
};

async function countPlayedGames(){
  try {
    const data = await docClient.scan(playedGamesParams).promise();
    return data;
  } catch (err) {
    return err;
  }
}

const avgTTEParams = {
  TableName : 'escaperoom-GamesTable8000B8A1-6LFZ1GJM4KI9',
  Select: "ALL_ATTRIBUTES",
  FilterExpression: 'completedTime <> :notCompleted',
  ExpressionAttributeValues: { ':notCompleted': 99999  }
};

async function avgTimeToEscape(){
  try {
    const data = await docClient.scan(avgTTEParams).promise();
    //console.log(data.Items[0].completedTime);
    let average = 0;
    for (let i = 0; i < data.Count; i++) {
      average = average + data.Items[i].completedTime;
    }
    average = Math.round(average / data.Count)
    return average;
  } catch (err) {
    return err;
  }
}

exports.handler = async (event, context) => {
  try {
    const failedGames = await countFailedGames();
    const passedGames = await countPassedGames();
    const playedGames = await countPlayedGames();
    const timeToEscape = await avgTimeToEscape();
    var body = new Object();
    body.passed_games = passedGames.Count;
    body.failed_games = failedGames.Count;
    body.played_games = playedGames.Count;
    body.timeToEscape = timeToEscape;
    const response = {
        statusCode: 200,
        body: JSON.stringify(body),
        'headers': { 
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, PUT, GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With'
        }
    };
    return response;
  } catch (err) {
    return { error: err }
  }
}