import 'dotenv/config';

import { SQSClient, SendMessageCommand } from "@aws-sdk/client-sqs";
import {  } from "@aws-sdk/client-sns";

const sqs = new SQSClient({
  region: process.env.AWS_REGION,
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID as string,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY as string,
  },
});

async function produceMessage(): Promise<void> {
  try {
    const data = await sqs.send(
      new SendMessageCommand({
        QueueUrl: process.env.SQS_QUEUE_URL as string,
        MessageBody: JSON.stringify({
          assetId: '1'
        }),
      })
    )
    
    console.log("Message sended!", data.MessageId);
  } catch (err) {
    console.error(err);
  }
}

produceMessage();