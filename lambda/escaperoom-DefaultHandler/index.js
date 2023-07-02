const AWS = require('aws-sdk');

      exports.handler = async function (event, context) {
        let connectionInfo;
        let connectionId = event.requestContext.connectionId;
      
        const callbackAPI = new AWS.ApiGatewayManagementApi({
          apiVersion: '2018-11-29',
          endpoint:
            event.requestContext.domainName + '/' + event.requestContext.stage,
        });
      
        try {
          connectionInfo = await callbackAPI
            .getConnection({ ConnectionId: event.requestContext.connectionId })
            .promise();
        } catch (e) {
          console.log(e);
        }
      
        connectionInfo.connectionID = connectionId;
        
        var lambda = new AWS.Lambda();
        
        var eventBody = event.body;
          if (eventBody == "mainScreen") {
            const lambda_payload = {
            "requestContext": {
              "domainName": "z7kur16zgb.execute-api.eu-central-1.amazonaws.com",
              "stage": "production"
            },
            "body": "{\"message\":\"MainScreen\"}"
          };
          var lambdaParams = {
              FunctionName: 'escaperoom-SendMessageHandlerDFBBCD6B-YQfevSlei6XW',
              InvocationType: 'RequestResponse',
              Payload: JSON.stringify(lambda_payload),
            };
          lambda.invoke(lambdaParams, function(err, data) {
          if (err) console.log(err, err.stack); // an error occurred
          else     console.log(data);           // successful response
          });
          eventBody = "pong mainScreen";
        }
        if (eventBody == "touchScreen") {
          const lambda_payload = {
            "requestContext": {
              "domainName": "z7kur16zgb.execute-api.eu-central-1.amazonaws.com",
              "stage": "production"
            },
            "body": "{\"message\":\"TouchScreen\"}"
          };
          var lambdaParams = {
              FunctionName: 'escaperoom-SendMessageHandlerDFBBCD6B-YQfevSlei6XW',
              InvocationType: 'RequestResponse',
              Payload: JSON.stringify(lambda_payload),
            };
          lambda.invoke(lambdaParams, function(err, data) {
          if (err) console.log(err, err.stack); // an error occurred
          else     console.log(data);           // successful response
          });
          eventBody = "pong touchScreen";
        }

        await callbackAPI
          .postToConnection({
            ConnectionId: event.requestContext.connectionId,
            Data:
              //'Use the sendmessage route to send a message. Your info:' +
              eventBody,
              //'Keep Alive Message Received'
          })
          .promise();
      
        return {
          statusCode: 200,
        };
      };