const AWS = require('aws-sdk');
const docClient = new AWS.DynamoDB.DocumentClient();

const params = {
  TableName : 'escaperoom-QuestionsTable8000B8A1-6LFZ1GJM4KI9'
}
function shuffle(array) {
  var currentIndex = array.length, temporaryValue, randomIndex;
  while (0 !== currentIndex) {
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex -= 1;
    temporaryValue = array[currentIndex];
    array[currentIndex] = array[randomIndex];
    array[randomIndex] = temporaryValue;
  }
  return array;
}
async function listItems(){
  try {
    const data = await docClient.scan(params).promise()
    shuffle(data.Items);
    const params2 = {
    TableName : 'escaperoom-GameQuestionsTable8000B8A1-6LFZ1GJM4KI9',
      Key: { "key": "key" },
          UpdateExpression: "set question = :g",
          ExpressionAttributeValues: {
              ":g": data
          }
      }
    docClient.update(params2, function(err, data) {
      if (err) console.log(err);
      else console.log(data);
    });
    console.log(JSON.stringify(data.Items));
    return data;
  } catch (err) {
    return err
  }
}

exports.handler = async (event, context) => {
  try {
    const data = await listItems()

  } catch (err) {
    return { error: err }
  }
}