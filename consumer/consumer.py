#!/usr/bin/env python
import faust
import time
import os
import asyncio
import httpx

TOPIC_INPUT = os.environ['TOPIC_INPUT']
TOPIC_OUTPUT = os.environ['TOPIC_OUTPUT']
INTERNAL_KAFKA_ADDR = os.environ['INTERNAL_KAFKA_ADDR']
KEY = 'prediction'
SENTIMENT_SERVICE_URL = os.environ['SENTIMENT_SERVICE_URL']

time.sleep(15) #wait to finish starting

app = faust.App(KEY, broker=INTERNAL_KAFKA_ADDR)

class MovieReview(faust.Record, serializer='json'):
    review_id: str
    content: str

input_kafka_topic = app.topic(TOPIC_INPUT, value_type=MovieReview)

output_kafka_topic = app.topic(TOPIC_OUTPUT)




@app.agent(channel=input_kafka_topic)
async def process(reviews: faust.Stream[MovieReview]) -> None:
    async for review in reviews:
        print(review)
        body = {
            "review": review.content
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{SENTIMENT_SERVICE_URL}/sentiment", json=body)
            # print(response.json())
            data = response.json()
            result = {
                'review_id': review.review_id,
                'content': review.content,
                'sentiment': data['sentiment_result']
            }
            print(result)
            await output_kafka_topic.send(value=result)
            await asyncio.sleep(1)





if __name__ == '__main__':
    app.main()